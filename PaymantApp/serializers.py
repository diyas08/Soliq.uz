from rest_framework.serializers import ModelSerializer
from .models import CardUser

from CheckApp.models import CheckModel
class CardSRL(ModelSerializer):
    class Meta:
        model = CardUser
        fields = '__all__'


class AddmoneySRL(ModelSerializer):
    class Meta:
        model = CardUser
        fields = ('card_number','money')

class QrCodeScanSerializer(ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ('fiskal_raqam',)



