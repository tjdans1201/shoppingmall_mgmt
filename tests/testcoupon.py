from django.test import TestCase
from rest_framework.test import APIClient
from coupon.models import CouponCode, CouponHistory, CouponType
import os
import pandas as pd
# Create your tests here.

curDir = os.path.dirname(os.path.normpath(__file__))
# 더미데이터 생성
def set_dummy():
    df = pd.read_csv(curDir + "/dummy/coupon_type_list.csv")
    dict_df = df.to_dict("records")
    coupon_types = [
        CouponType(
            id=x["id"],
            type=x["type"],
        )
        for x in dict_df
    ]
    CouponType.objects.bulk_create(coupon_types)
    print("finish")

def set_dummy_history():
    df = pd.read_csv(curDir + "/dummy/coupon_history.csv")
    dict_df = df.to_dict("records")
    coupon_historys = [
        CouponHistory(
            id=x["id"],
            discount_amount=x["discount_amount"],
            used_coupon_id=x["used_coupon_id"]
        )
        for x in dict_df
    ]
    CouponHistory.objects.bulk_create(coupon_historys)
    print("finish")

class TestCoupon(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        pass

    def test_create_coupon(self):
        print("start set_dummy")
        set_dummy()
        print(CouponType.objects.all())
        # 쿠폰 등록 테스트
        print("-----------------------------------------")
        print("start_test_create_coupon")
        client = APIClient()
        # case_1 : % 할인 쿠폰을 등록할때 할인율이 100이 넘는 경우
        result = client.post(
            "/api/coupons",
            {
                "coupon_type": 2,
                "amount": 1000,
                "coupon_code": "testcode",
            },
            format="json",
        )
        exp = {"message": "리퀘스트 에러가 발생하였습니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)

        # case_2 : 정상 등록
        result = client.post(
            "/api/coupons",
            {
                "coupon_type": 1,
                "amount": 1000,
                "coupon_code": "testcode",
            },
            format="json",
        )
        exp = {"message": "쿠폰이 등록되었습니다."}
        print(result)
        print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.data, exp)

        # case_3 : 쿠폰 코드 중복
        result = client.post(
            "/api/coupons",
            {
                "coupon_type": 3,
                "amount": 1000,
                "coupon_code": "testcode",
            },
            format="json",
        )
        exp = {"message": "이미 존재하는 쿠폰 코드입니다."}
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)

    def test_get_coupons_history(self):
        set_dummy_history()
        # 쿠폰 등록 테스트
        print("-----------------------------------------")
        print("start_test_get_coupons_history")
        client = APIClient()
        # case_1 정상 케이스
        result = client.get(
            "/api/coupons"
        )
        # exp = {"message": "리퀘스트 에러가 발생하였습니다."}
        print(result.data)
        print(result)
        self.assertEqual(result.status_code, 400)
        # self.assertEqual(result.data, exp)