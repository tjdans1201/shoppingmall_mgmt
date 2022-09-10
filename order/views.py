from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Delivery, DeliveryCost, ContryCode
from .serializers import DeliverySerializer
from rest_framework.generics import get_object_or_404
import requests
import json

# Create your views here.


class OrderAPI(APIView):
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
            else:
                return Response(
                    {"message": "리퀘스트 에러가 발생하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request_body["delivery_cost"] = delivery_cost
            # 배송비 + 제품가격 합산
            # 주문자 국가가 한국이 아닐 경우, 환율을 적용하여 합산
            request_body["total_price"] = (
                delivery_cost + (request_body["price"] * 1200)
                if buyr_country_code != "KR"
                else delivery_cost + request_body["price"]
            )
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
