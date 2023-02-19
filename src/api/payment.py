import uuid

from yookassa import Configuration, Payment

Configuration.configure('986248',
                        'test_yo4bdHFqpaqfX4sAbpZTl0yQs21ohsjLgBUi9HUm_Sw')


def create_payment():
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": "22222.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://localhost:8000/docs"
        },
        "description": "Заказ №72"
    }, idempotence_key)

    # get confirmation url
    confirmation_url = payment.confirmation.confirmation_url
    global token_payment
    token_payment = confirmation_url.split('=')[1]
    return confirmation_url


token_payment = ''


def check_if_successful_payment():
    payment_id = token_payment
    payment = Payment.find_one(payment_id)
    try:
        if payment.status == 'succeeded':
            return True
    except KeyError:
        return False
    return False
