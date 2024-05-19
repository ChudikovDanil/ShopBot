import yookassa
from yookassa import Payment
import uuid
from app import database as db
import os

yookassa.Configuration.account_id = os.getenv('ACCOUNT_ID')
yookassa.Configuration.secret_key = os.getenv('PAYMENT_TOKEN')


def create(chat_id, user_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            'value': db.total_sum(user_id),
            'currency': "RUB"
        },
        'payment_method_data': {
            'type': 'bank_card'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://t.me/Black_21_JackBot'
        },
        'capture': True,
        'metadata': {
            'chat_id' : chat_id
        },
        'description':{
            'Описнаие товара'
        }
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id
