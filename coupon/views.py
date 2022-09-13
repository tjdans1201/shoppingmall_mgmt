from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CouponCode
from .serializers import CouponCreateSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
import requests
import json
# Create your views here.

class CouponsAPI(APIView):
    def post(self, request):
        try:
            request_body = request.data
            # % 할인 쿠폰일 경우, 100을 초과하지 못함
            if request_body["coupon_type"] == 2:
                if request_body["amount"] > 100:
                    return Response(
                    {"message": "리퀘스트 에러가 발생하였습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
            )  
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

