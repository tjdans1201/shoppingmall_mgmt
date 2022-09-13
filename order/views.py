from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Delivery, DeliveryCost, ContryCode
from .serializers import DeliverySerializer, DeliveryListSerializer, DeliveryUpdateSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
import requests
import json

# Create your views here.

def get_exchange_rate():
    exchange_rate = 0
    # dunamu API로부터 현재 원/달러 환율 취득
    response = requests.get("https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD")
    exchange_rate = response.json()[0]["basePrice"]
    return exchange_rate


class OrderAPI(APIView):
    def get(self, request):
        """
        제품 주문 내역 열람
        - 주문 내역 검색
        - 주문 상태, 시작 일자, 종료일자에 따른 필터
        - 주문자명으로 검색

        Returns:
            200 : {order_list : []}
            500 : {"message" : "서버 에러가 발생하였습니다."}
        """
        try:
            # 검색 조건이 있는 경우
            if request.query_params:
                q= Q()
                query_param = request.query_params
                # 각 검색 조건이 있을때마다 where 조건 추가
                # 시작 일자 필터
                if "start_date" in query_param:
                    q.add(Q(date__gte=query_param["start_date"]),q.AND)
                # 종료 일자 필터
                if "end_date" in query_param:
                    q.add(Q(date__lte=query_param["end_date"]),q.AND)
                # 주문 상태 필터
                if "pay_state" in query_param:
                    q.add(Q(pay_state=query_param["pay_state"]),q.AND)
                # 주문자명 필터
                if "buyr_name" in query_param:
                    q.add(Q(buyr_name=query_param["buyr_name"]),q.AND)
                order_list = Delivery.objects.filter(q).order_by("-date")
            # 검색 조건이 없는 경우
            else:
                order_list = Delivery.objects.all().order_by("-date")
            serializer = DeliveryListSerializer(order_list, many=True)
            return Response({"order_list": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        주문정보 등록
        args :
            request.data: {"buyr_name":str,"buyr_country":str, "buyr_city":str, "buyr_zipx":str, "quantity":int, "price":int}
            ex) {"buyr_name":"kim","buyr_country":"IN", "buyr_city":"mumbai", "buyr_zipx":"aa11", "quantity":1, "price":150}
        Returns:
            201 : {"message" : "주문이 등록되었습니다"}
            400 : {"message" : "리퀘스트 에러가 발생하였습니다."}
            500 : {"message" : "서버 에러가 발생하였습니다."}
        """
        try:
            request_body = request.data
            # 배송비 계산
            buyr_country_code = request_body["buyr_country"]
            order_quantity = request_body["quantity"]
            # 입력받은 국가 코드로 국가명 취득
            country_name = ContryCode.objects.filter(country_code=buyr_country_code)
            if country_name:
                # 배송비 테이블에서 수량과 국가명으로 배송비 취득
                delivery_cost = DeliveryCost.objects.filter(quantity=order_quantity)[
                    0
                ].__dict__[str(country_name[0].country_name)]
                # 한국이 아닐 경우 달러 적용(환율 적용)
                if buyr_country_code != "KR":
                    # 외부 API로 부터 현재 환율 취득
                    exchange_rate = get_exchange_rate()
                    delivery_cost = round(delivery_cost/exchange_rate,2)
            else:
                return Response(
                    {"message": "리퀘스트 에러가 발생하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request_body["delivery_cost"] = delivery_cost

            # 배송비 + 제품가격 합산
            # 주문자 국가가 한국이 아닐 경우, 환율을 적용하여 달러로 합산
            request_body["total_price"] = delivery_cost + request_body["price"]
            serializer = DeliverySerializer(data=request_body)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "주문이 등록되었습니다."}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": "리퀘스트 에러가 발생하였습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@api_view(["PUT"])
def update_pay_state(request,id):
    try:
        request_body = request.data
        delivery=Delivery.objects.get(id=id)
        delivery.pay_state = request_body["pay_state"]
        if delivery.pay_state == "결제취소":
            delivery.delivery_state = "배송취소"
        serializer = DeliveryUpdateSerializer(delivery, data=request_body)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {"message": "결제정보가 수정되었습니다."}, status=status.HTTP_200_OK
                )
        return Response(
            {"message": "리퀘스트 에러가 발생하였습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(e)
        return Response(
            {"message": "서버 에러가 발생하였습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["PUT"])
def update_delivery_state(request,id):
    try:
        request_body = request.data
        delivery=Delivery.objects.get(id=id)
        delivery.pay_state = request_body["delivery_state"]
        serializer = DeliveryUpdateSerializer(delivery, data=request_body)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {"message": "배송정보가 수정되었습니다."}, status=status.HTTP_200_OK
                )
        return Response(
            {"message": "리퀘스트 에러가 발생하였습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(e)
        return Response(
            {"message": "서버 에러가 발생하였습니다."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )