# shoppingmall_mgmt
----------
## 개발기간
#### 2022-09-08 ~ 2022-09-14

## 프로젝트 설명
 - 제품 쇼핑몰 관리 페이지의 backend 개발
 - 주문 내역 열람 및 검색 필터 적용
 - 쿠폰의 발급과 적용
 - 각 쿠폰의 사용 횟수와 총 할인액 계산
 - 배송 상태 업데이트
 - 달러 단위의 배송비는 현재 환율로 적용해서 계산
 
## 사용된 기술
 - **Back-End** : Python, Django, Django REST framework, postgresql
 
## ERD
<img width="196" alt="erd" src="https://user-images.githubusercontent.com/57758265/190105211-07cd9e59-db9b-42b9-8fa3-7a1ad4953d5c.png">

## API_DOCS

### 주문 리스트 조회
- 주문 상태, 시작일자, 종료일자, 주문자명으로 검색이 가능하다

API URL

GET api/orders
#### Query_param
|명칭|변수명|형식|비고|
|:------:|:------:|:------:|:------:|
|시작일자|start_date|str|"yyyy-mm-dd"|
|종료일자|end_date|str|"yyyy-mm-dd"|
|주문자명|buyr_name|str||
|결제정보|pay_state|str||

#### Response_body
|명칭|변수명|형식|비고|
|:------:|:------:|:------:|:------:|
|주문내역 리스트|order_list|dictionary[]||
|id|id|int||
|주문자명|buyr_name|str||
|주문일자|date|str|"yyyy-mm-dd"|
|수량|quantity|int||
|구매가격|price|float||
|배송비|delivery_cost|float||
|구매 도시|buyr_city|str||
|구매 국가|buyr_country|str||
|구매자 우편번호|buyr_zipx|str||
|결제 상태|pay_state|int||
|배송 상태|delivery_state|int||
|사용 쿠폰|used_coupon_code|int||



#### HTTP status code
| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상종료 |
| 500 | Internal Server Error | 서버 에러가 발생하였습니다. | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "order_list": [
        {
            "id": 1,
            "date": "2022-09-14",
            "pay_state": "결제대기",
            "quantity": 1,
            "price": 110000.0,
            "delivery_cost": 36000.0,
            "total_price": 146000.0,
            "buyr_city": "mumbai",
            "buyr_country": "KR",
            "buyr_zipx": "aa11",
            "delivery_num": null,
            "delivery_state": "배송대기중",
            "buyr_name": "yun",
            "used_coupon_code": null
        }
	]
}
```

2) 500

```json
{
    "Message": "서버 에러가 발생하였습니다."
}
```

###  주문 등록
- 주문상태를 등록한다.
- 제품 가격, 배송비, 총비용은 국가가 한국일 경우 원화, 그 외 국가는 달러로 변환한다.
- 쿠폰을 사용하면 각 쿠폰의 타입에 맞게 배송비 할인, 상품가 정액 할인, 상품가 %할인을 적용할 수 있다.

API URL

POST api/orders

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|주문자명|buyr_name|str||
|수량|quantity|int||
|구매가격|price|float||
|구매 도시|buyr_city|str||
|구매 국가|buyr_country|str||
|구매자 우편번호|buyr_zipx|str||
|쿠폰 코드|coupon_code|str||


Request Example

```json
{"buyr_name":"yun","buyr_country":"IN", "buyr_city":"mumbai", "buyr_zipx":"aa11", "quantity":1, "price":110,"coupon_code":"firstcoupona"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | 주문이 등록되었습니다. | 정상종료 |
| 400 | Request Error | "해당 쿠폰이 없습니다.","리퀘스트 에러가 발생했습니다” | Request Body 문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "주문이 등록되었습니다."
}
```

2) 400

```json
{
    "message": "해당 쿠폰이 없습니다."
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```

### 결제상태 수정
- 해당 주문정보의 결제상태를 수정한다.

API URL

PUT /api/orders/update/pay_state/<int:id>

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 결제상태 | pay_state | str |  |

Request Example

```json
{"pay_state":"결제완료"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | “결제상태가 수정되었습니다.” | 정상종료 |
| 400 | Request Error | "리퀘스트 에러가 발생했습니다.” | Request Body 문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "결제상태가 수정되었습니다."
}
```

2) 400

```json
{
    "message": "리퀘스트 에러가 발생했습니다.”
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```

### 배송상태 수정
- 해당 주문정보의 배송상태를 수정한다.

API URL

PUT /api/orders/update/delivery_state/<int:id>

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| 배송상태 | delivery_state | str |  |

Request Example

```json
{"pay_state":"배송완료"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | “배송상태가 수정되었습니다.” | 정상종료 |
| 400 | Request Error | "리퀘스트 에러가 발생했습니다.” | Request Body 문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "배송상태가 수정되었습니다."
}
```

2) 400

```json
{
    "message": "리퀘스트 에러가 발생했습니다.”
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```

###  쿠폰코드 등록
- 쿠폰코드를 등록한다.
- 쿠폰타입은 1:배송비 할인, 2: %할인, 3: 정액 할인으로 지정가능하다.
- 할인금액은 원화를 기준으로 한다.

API URL

POST api/coupons

Request Body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
|쿠폰타입|coupon_type|int||
|할인률/할인금액|amount|int||
|쿠폰코드|coupon_code|str||


Request Example

```json
{"coupon_type":1, "amount":1000, "coupon_code":"firstcoupon"}
```

Response_body

| 명칭 | 변수명 | 형태 | 비고 |
| --- | --- | --- | --- |
| message | message | str |  |

HTTP status code

| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | 쿠폰이 등록되었습니다. | 정상종료 |
| 400 | Request Error |"이미 존재하는 쿠폰 코드입니다.","리퀘스트 에러가 발생했습니다” | Request Body 문제 |
| 500 | Internal Server Error | "서버 에러가 발생하였습니다.” | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "message": "쿠폰이 등록되었습니다."
}
```

2) 400

```json
{
    "message": "이미 존재하는 쿠폰 코드입니다."
}
```

3) 500

```json
{
    "message": "서버 에러가 발생하였습니다."
}
```

### 쿠폰 사용 내역 조회
- 모든 쿠폰의 사용 내역을 조회한다

API URL

GET api/coupons

#### Response_body
|명칭|변수명|형식|비고|
|:------:|:------:|:------:|:------:|
|사용내역 리스트|coupon_history_list|dictionary[]||
|id|id|int||
|실할인액|actual_discount_amount|float|원화 기준|
|쿠폰 타입|coupon_type|str||
|쿠폰 코드|coupon_code|str||
|쿠폰 id|coupon_id|int||
|할인율/할인액|discount|int|원화 |



#### HTTP status code
| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상종료 |
| 500 | Internal Server Error | 서버 에러가 발생하였습니다. | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "coupon_history_list": [
        {
            "id": 1,
            "actual_discount_amount": 1000.0,
            "coupon_type": "delivery_discount",
            "coupon_code": "testcode",
            "coupon_id": 1,
            "discount": 1000
        }
    ]
}
```

2) 500

```json
{
    "Message": "서버 에러가 발생하였습니다."
}
```

### 지정 쿠폰의 사용횟수, 총 할인액 조회
- 지정된 쿠폰의 총 사용횟수 및 총 할인액을 조회한다.

API URL

GET api/coupons

#### Response_body
|명칭|변수명|형식|비고|
|:------:|:------:|:------:|:------:|
|총 사용횟수|count|int||
|총 할인금액|total_discount|float||


#### HTTP status code
| HTTP status | AppErrors | 메시지 | 설명 |
| --- | --- | --- | --- |
| 200 | - | - | 정상종료 |
| 500 | Internal Server Error | 서버 에러가 발생하였습니다. | API 내부 에러 발생 |

Response Example

1) 200

```json
{
    "count": 1,
    "total_discount": 1000.0
}
```

2) 500

```json
{
    "Message": "서버 에러가 발생하였습니다."
}
```


## Unit test
- 각 API에 대해 유닛테스트 실행(7개)
<img width="461" alt="화면 캡처 2022-09-07 144024" src="https://user-images.githubusercontent.com/57758265/190106342-35866266-972f-4918-9079-3cdcdd670fb6.png">


