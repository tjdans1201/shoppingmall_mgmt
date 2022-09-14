from django.test import TestCase
from rest_framework.test import APIClient
from coupon.models import CouponCode, CouponHistory, CouponType
from order.models import Delivery, DeliveryCost, ContryCode
from unittest import mock
import os
import pandas as pd
import json

# Create your tests here.


curDir = os.path.dirname(os.path.normpath(__file__))
# 더미데이터 생성(coupon_type)
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


# 더미데이터 생성(delivery_cost)
def set_dummy_delivery_cost():
    df = pd.read_csv(curDir + "/dummy/delivery_cost.csv")
    dict_df = df.to_dict("records")
    delivery_costs = [
        DeliveryCost(
            id=x["id"],
            quantity=x["quantity"],
            Australia=x["Australia"],
            Brazil=x["Brazil"],
            Canada=x["Canada"],
            China=x["China"],
            France=x["France"],
            Germany=x["Germany"],
            Hong_kong=x["Hong_kong"],
            Indonesia=x["Indonesia"],
            Japan=x["Japan"],
            Malaysia=x["Malaysia"],
            New_Zealand=x["New_Zealand"],
            Philippines=x["Philippines"],
            Russia=x["Russia"],
            Singapore=x["Singapore"],
            Spain=x["Spain"],
            Taiwan=x["Taiwan"],
            Thailand=x["Thailand"],
            UK=x["UK"],
            USA=x["USA"],
            Vietnam=x["Vietnam"],
            Cambodia=x["Cambodia"],
            Laos=x["Laos"],
            Macao=x["Macao"],
            Mongolia=x["Mongolia"],
            Myanmar=x["Myanmar"],
            Bangladesh=x["Bangladesh"],
            Bhutan=x["Bhutan"],
            Brunei_Darussala=x["Brunei_Darussala"],
            India=x["India"],
            Maldives=x["Maldives"],
            Nepal=x["Nepal"],
            Sri_Lanka=x["Sri_Lanka"],
            Albania=x["Albania"],
            Armenia=x["Armenia"],
            Austria=x["Austria"],
            Azerbaijan=x["Azerbaijan"],
            Bahrain=x["Bahrain"],
            Belarus=x["Belarus"],
            Belgium=x["Belgium"],
            Bulgaria=x["Bulgaria"],
            Bosnia_And_Herzegovina=x["Bosnia_And_Herzegovina"],
            Croatia=x["Croatia"],
            Cyprus=x["Cyprus"],
            Czech_Rep=x["Czech_Rep"],
            Denmark=x["Denmark"],
            Estonia=x["Estonia"],
            Finland=x["Finland"],
            Georgia=x["Georgia"],
            Greece=x["Greece"],
            Hungary=x["Hungary"],
            Iran=x["Iran"],
            Ireland=x["Ireland"],
            Israel=x["Israel"],
            Jordan=x["Jordan"],
            Kazakhstan=x["Kazakhstan"],
            Latvia=x["Latvia"],
            Luxembourg=x["Luxembourg"],
            Macedonia=x["Macedonia"],
            Netherlands=x["Netherlands"],
            Norway=x["Norway"],
            Oman=x["Oman"],
            Pakistan=x["Pakistan"],
            Poland=x["Poland"],
            Portugal=x["Portugal"],
            Qatar=x["Qatar"],
            Romania=x["Romania"],
            Saudi_Arabia=x["Saudi_Arabia"],
            Slovakia=x["Slovakia"],
            Slovenia=x["Slovenia"],
            Sweden=x["Sweden"],
            Switzerland=x["Switzerland"],
            Turke=x["Turkey"],
            Ukraine=x["Ukraine"],
            United_Arab_Emirates=x["United_Arab_Emirates"],
            Uzbekistan=x["Uzbekistan"],
            Algeria=x["Algeria"],
            Antiless_Netherlands=x["Antiless_Netherlands"],
            Argentina=x["Argentina"],
            Botswana=x["Botswana"],
            Cape_Verde=x["Cape_Verde"],
            Chile=x["Chile"],
            Costa_Rica=x["Costa_Rica"],
            Cuba=x["Cuba"],
            Djibouti=x["Djibouti"],
            Dominican_Republic=x["Dominican_Republic"],
            Ecuador=x["Ecuador"],
            Egypt=x["Egypt"],
            Eritrea=x["Eritrea"],
            Ethiopia=x["Ethiopia"],
            Fiji=x["Fiji"],
            Kenya=x["Kenya"],
            Lesotho=x["Lesotho"],
            Mauritius=x["Mauritius"],
            Mexico=x["Mexico"],
            Morocco=x["Morocco"],
            Mozambique=x["Mozambique"],
            Nigeria=x["Nigeria"],
            Panama=x["Panama"],
            Peru=x["Peru"],
            Rwanda=x["Rwanda"],
            Tanzania=x["Tanzania"],
            Tunisia=x["Tunisia"],
            Zambia=x["Zambia"],
            South_Korea=x["South_Korea"],
        )
        for x in dict_df
    ]
    DeliveryCost.objects.bulk_create(delivery_costs)
    print("delivery_cost finish")


# 더미데이터 생성(country_code)
def set_dummy_country_code():
    df = pd.read_csv(curDir + "/dummy/country_code.csv")
    dict_df = df.to_dict("records")
    country_codes = [
        ContryCode(
            country_idx=x["country_idx"],
            country_code=x["country_code"],
            country_dcode=x["country_dcode"],
            country_name=x["country_name"],
        )
        for x in dict_df
    ]
    ContryCode.objects.bulk_create(country_codes)


# 더미데이터 생성(coupon_code)
def set_dummy_coupon():
    df = pd.read_csv(curDir + "/dummy/coupon_code.csv")
    dict_df = df.to_dict("records")
    coupons = [
        CouponCode(
            id=x["id"],
            amount=x["amount"],
            coupon_code=x["coupon_code"],
            coupon_type_id=x["coupon_type_id"],
        )
        for x in dict_df
    ]
    CouponCode.objects.bulk_create(coupons)


# 더미데이터 생성(delivery)
def set_dummy_delivery():
    df = pd.read_csv(curDir + "/dummy/delivery.csv")
    dict_df = df.to_dict("records")
    deliverys = [
        Delivery(
            id=x["id"],
            date=x["date"],
            pay_state=x["pay_state"],
            quantity=x["quantity"],
            price=x["price"],
            buyr_city=x["buyr_city"],
            buyr_country=x["buyr_country"],
            buyr_zipx=x["buyr_zipx"],
            vccode=x["vccode"],
            delivery_state=x["delivery_state"],
            delivery_num=x["delivery_num"],
            delivery_cost=x["delivery_cost"],
            total_price=x["total_price"],
            buyr_name=x["buyr_name"],
            used_coupon_code_id=x["used_coupon_code_id"],
        )
        for x in dict_df
    ]
    Delivery.objects.bulk_create(deliverys)


# # 환율 요청 mock
# def call_exchange_rate_success(url, timeout=None, status_code=None):
#     class MockResponse:
#         def __init__(self, url, content, status_code):
#             self.url = url
#             self.content = content.encode()
#             self.status_code = status_code

#     return MockResponse(
#         url,
#         json.dumps(
#             [{'code': 'FRX.KRWUSD', 'currencyCode': 'USD', 'currencyName': '달러', 'country': '미국', 'name': '미국 (KRW/USD)', 'date': '2022-09-14', 'time': '13:47:29', 'recurrenceCount': 424, 'basePrice': 1390.6, 'openingPrice': 1374.8, 'highPrice': 1395.3, 'lowPrice': 1374.8, 'change': 'RISE', 'changePrice': 0.6, 'cashBuyingPrice': 1414.93, 'cashSellingPrice': 1366.27, 'ttBuyingPrice': 1377.0, 'ttSellingPrice': 1404.2, 'tcBuyingPrice': None, 'fcSellingPrice': None, 'exchangeCommission': 4.6954, 'usDollarRate': 1.0, 'high52wPrice': 1395.3, 'high52wDate': '2022-09-14', 'low52wPrice': 1164.2, 'low52wDate': '2021-10-26', 'currencyUnit': 1, 'provider': '하나은행', 'timestamp': 1663130850584, 'id': 79, 'modifiedAt': '2022-09-14T04:47:31.000+0000', 'createdAt': '2016-10-21T06:13:34.000+0000', 'signedChangePrice': 0.6, 'changeRate': 0.0004316547, 'signedChangeRate': 0.0004316547}]
#         ),
#         200,
#     )


class TestCoupon(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = APIClient()
        set_dummy()
        set_dummy_coupon()
        set_dummy_delivery_cost()
        set_dummy_country_code()

    def test_create_order(self):
        print("start set_dummy")
        print(CouponType.objects.all())
        # 주문 등록 테스트
        print("-----------------------------------------")
        print("start_test_create_coupon")
        client = APIClient()
        # case_1 : 주문 등록(쿠폰 적용하지 않음), 해외
        result = client.post(
            "/api/orders",
            {
                "buyr_name": "yun",
                "buyr_country": "IN",
                "buyr_city": "mumbai",
                "buyr_zipx": "aa11",
                "quantity": 1,
                "price": 100,
                "coupon_code": "",
            },
            format="json",
        )
        exp = {"message": "주문이 등록되었습니다."}
        delivery = Delivery.objects.get(id=1)
        restored_exp = {
            "id": 1,
            "buyr_name": "yun",
            "buyr_country": "IN",
            "buyr_city": "mumbai",
            "buyr_zipx": "aa11",
            "quantity": 1,
            "price": 100,
            "used_coupon_code_id": None,
        }
        restored = {
            "id": delivery.id,
            "buyr_name": delivery.buyr_name,
            "buyr_country": delivery.buyr_country,
            "buyr_city": delivery.buyr_city,
            "buyr_zipx": delivery.buyr_zipx,
            "quantity": delivery.quantity,
            "price": delivery.price,
            "used_coupon_code_id": delivery.used_coupon_code_id,
        }
        print(delivery)
        print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.data, exp)
        self.assertEqual(restored, restored_exp)

        # case_2 : 주문 등록(쿠폰 적용하지 않음), 국내
        result = client.post(
            "/api/orders",
            {
                "buyr_name": "yun",
                "buyr_country": "KR",
                "buyr_city": "incheon",
                "buyr_zipx": "21082",
                "quantity": 1,
                "price": 10000,
                "coupon_code": "",
            },
            format="json",
        )
        exp = {"message": "주문이 등록되었습니다."}
        delivery = Delivery.objects.get(id=2)
        restored_exp = {
            "id": 2,
            "buyr_name": "yun",
            "buyr_country": "KR",
            "buyr_city": "incheon",
            "buyr_zipx": "21082",
            "quantity": 1,
            "price": 10000.0,
            "used_coupon_code_id": None,
            "delivery_cost": 36000,
        }
        restored = {
            "id": delivery.id,
            "buyr_name": delivery.buyr_name,
            "buyr_country": delivery.buyr_country,
            "buyr_city": delivery.buyr_city,
            "buyr_zipx": delivery.buyr_zipx,
            "quantity": delivery.quantity,
            "price": delivery.price,
            "used_coupon_code_id": delivery.used_coupon_code_id,
            "delivery_cost": delivery.delivery_cost,
        }
        print(delivery)
        print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.data, exp)
        self.assertEqual(restored, restored_exp)

        # case_3 : 존재하지 않는 쿠폰 적용
        result = client.post(
            "/api/orders",
            {
                "buyr_name": "yun",
                "buyr_country": "KR",
                "buyr_city": "incheon",
                "buyr_zipx": "21082",
                "quantity": 1,
                "price": 10000,
                "coupon_code": "aaaaaa",
            },
            format="json",
        )
        exp = {"message": "해당 쿠폰이 없습니다."}
        print(delivery)
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data, exp)

        # case_4 : 주문 등록(배송비 1000원 할인 쿠폰 적용), 국내
        result = client.post(
            "/api/orders",
            {
                "buyr_name": "yun",
                "buyr_country": "KR",
                "buyr_city": "incheon",
                "buyr_zipx": "21082",
                "quantity": 1,
                "price": 10000,
                "coupon_code": "testcode1",
            },
            format="json",
        )
        exp = {"message": "주문이 등록되었습니다."}
        delivery = Delivery.objects.get(id=3)
        restored_exp = {
            "id": 3,
            "buyr_name": "yun",
            "buyr_country": "KR",
            "buyr_city": "incheon",
            "buyr_zipx": "21082",
            "quantity": 1,
            "price": 10000.0,
            "used_coupon_code_id": 1,
            "delivery_cost": 35000,
        }
        restored = {
            "id": delivery.id,
            "buyr_name": delivery.buyr_name,
            "buyr_country": delivery.buyr_country,
            "buyr_city": delivery.buyr_city,
            "buyr_zipx": delivery.buyr_zipx,
            "quantity": delivery.quantity,
            "price": delivery.price,
            "used_coupon_code_id": delivery.used_coupon_code_id,
            "delivery_cost": delivery.delivery_cost,
        }
        print(delivery)
        print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(result.data, exp)
        self.assertEqual(restored, restored_exp)
        history = CouponHistory.objects.get(id=1)
        coupon_history_exp = {"id": 1, "discount_amount": 1000, "used_coupon_id": 1}
        coupon_history = {
            "id": history.id,
            "discount_amount": history.discount_amount,
            "used_coupon_id": history.used_coupon_id,
        }
        self.assertEqual(coupon_history, coupon_history_exp)

    def test_get_order_list(self):
        print("-----------------------------------------")
        print("start_test_get_coupons_history")
        set_dummy_delivery()
        test_1 = Delivery.objects.get(id=2)
        test_1.date = "2022-09-15"
        test_1.save()
        test_2 = Delivery.objects.get(id=3)
        test_2.date = "2022-09-16"
        test_2.save()
        test_3 = Delivery.objects.get(id=4)
        test_3.date = "2022-09-17"
        test_3.save()
        client = APIClient()
        # case_1 검색 조건이 없는 경우
        result = client.get("/api/orders")
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["order_list"]), 4)

        # case_2 날짜 지정(2022-09-14~2022-09-15)
        result = client.get("/api/orders?start_date=2022-09-14&end_date=2022-09-15")
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["order_list"]), 2)

        # case_3 결제상태 지정("결제완료")
        result = client.get("/api/orders?pay_state=결제완료")
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["order_list"]), 3)

        # case_4 주문자명 지정("test")
        result = client.get("/api/orders?buyr_name=test")
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.data["order_list"]), 1)

    def test_update_pay_state(self):
        set_dummy_delivery()
        print("-----------------------------------------")
        print("start_test_get_coupons_history")
        client = APIClient()
        # case_1 결제 대기에서 결제 완료로 변경
        result = client.put(
            "/api/orders/update/pay_state/4",
            {"pay_state": "결제완료"},
            format="json",
        )
        print(result)
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"message": "결제정보가 수정되었습니다."})
        delivery = Delivery.objects.get(id=4)
        self.assertEqual(delivery.pay_state, "결제완료")

    def test_update_delivery_state(self):
        set_dummy_delivery()
        print("-----------------------------------------")
        print("start_def test_update_delivery_state(self)")
        client = APIClient()
        # case_1 배송준비중에서 배송완료로 변경
        result = client.put(
            "/api/orders/update/delivery_state/4",
            {"delivery_state": "배송완료"},
            format="json",
        )
        print(result)
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {"message": "배송정보가 수정되었습니다."})
        delivery = Delivery.objects.get(id=4)
        self.assertEqual(delivery.pay_state, "배송완료")
