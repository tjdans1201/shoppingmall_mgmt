from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CouponCreateSerializer
from .models import CouponCode, CouponHistory

# Create your views here.


class CouponsAPI(APIView):
    def post(self, request):
        """
        쿠폰 생성
        coupon_type에 따라 쿠폰 종류가 다름
        1: 배송비 정액 할인
        2: 상품가 %할인
        3: 상품가 정액 할인
        """
        try:
            request_body = request.data
            coupon_code = CouponCode.objects.filter(coupon_code = request_body["coupon_code"])
            if len(coupon_code)>0:
                return Response(
                        {"message": "이미 존재하는 쿠폰 코드입니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            # % 할인 쿠폰일 경우, 100을 초과하지 못함
            if request_body["coupon_type"] == 2:
                if request_body["amount"] > 100:
                    return Response(
                        {"message": "리퀘스트 에러가 발생하였습니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            # 쿠폰 등록
            serializer = CouponCreateSerializer(data=request_body)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "쿠폰이 등록되었습니다."}, status=status.HTTP_201_CREATED
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

    def get(self, request):
        """
        모든 쿠폰의 사용내역을 조회
        """
        try:
            # 모든 쿠폰사용내역 조회
            coupon_history = CouponHistory.objects.all()
            coupon_history_list = []
            for i in coupon_history:
                coupon_history_list.append(
                    {
                        "id": i.id,
                        "actual_discount_amount": i.discount_amount,
                        "coupon_type": i.used_coupon.coupon_type.type,
                        "coupon_code": i.used_coupon.coupon_code,
                        "coupon_id": i.used_coupon_id,
                        "discount": i.used_coupon.amount,
                    }
                )
            return Response({"coupon_history_list": coupon_history_list})
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CouponAPI(APIView):
    """
    해당 쿠폰의 총 사용횟수와 총 할인액을 조회
    """

    def get(self, request, id):
        try:
            history = CouponHistory.objects.filter(used_coupon=id)
            total_discount = 0
            count = 0
            # 해당 쿠폰의 사용횟수를 구함
            if len(history) > 0:
                count = len(history)
            # 해당 쿠폰의 총 할인액을 구함
            for i in history:
                total_discount += i.discount_amount
            return Response(
                {"count": count, "total_discount": total_discount},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "서버 에러가 발생하였습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
