import razorpay
from django.conf import settings


def get_razorpay_client():
    # return razorpay.Client(auth=("rzp_test_sYDXizFjDxb4Vw", "mWbFEV0lUB2Mzp71x57wZSw2"))

    RZP_KEY_ID = settings.RAZORPAY_KEY_ID
    RZP_SECRET_KEY = settings.RAZORPAY_SECRET_KEY
    print(RZP_KEY_ID)
    print(RZP_SECRET_KEY)

    rzp_client = razorpay.Client(auth=(RZP_KEY_ID, RZP_SECRET_KEY))
    print(rzp_client)
    return rzp_client


def is_razorpay_payment_order_successful(order_id):
    order_response = get_razorpay_client().order.fetch(order_id=order_id)
    return order_response.get("status") in ["paid"]


def create_razorpay_payment_order(amount, currency):
    return get_razorpay_client().order.create(
        data={
            "amount": int(int(amount)),
            "currency": currency,
        }
    )


def verify_razorpay_payment_completion(**kwargs):
    client = get_razorpay_client()
    razorpay_order_id = kwargs.get("razorpay_order_id")
    razorpay_payment_id = kwargs.get("razorpay_payment_id")
    razorpay_signature = kwargs.get("razorpay_signature")

    params_dict = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }
    return client.utility.verify_payment_signature(params_dict)
