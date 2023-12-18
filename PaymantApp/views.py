from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status

from .serializers import CardSRL, AddmoneySRL,QrCodeScanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import CardUser
#fpdf
from fpdf import FPDF


# Create your views here.

class Add_Card(APIView):
    queryset = CardUser.objects.all()
    serializer_class = CardSRL

    @swagger_auto_schema(request_body=CardSRL)
    def post(self, request):
        serializer = CardSRL(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG": "Card Created"})
        else:
            return Response(serializer.errors)


class AddMoneyView(APIView):
    @swagger_auto_schema(request_body=AddmoneySRL)

    def post(self, request):
        card_number = request.data.get("card_number")
        money = request.data.get("money")
        filtr_card = CardUser.objects.all().filter(card_number=card_number)
        print(filtr_card)
        for i in filtr_card:
            user_puli = i.money
        hamma_pul = user_puli + money
        updater = CardUser.objects.all().filter(card_number=card_number).update(money=hamma_pul)
        return Response({"message": "ok"})
    #


davlat_korxonalari = [
    "Tatu",
    "Qushbegi hotel",
    "Mars IT ",
    "Akfa",
    "Korzika",
    "Rivera",
    "Chanel",
    "Makro",
    "Mobiuz",
    "Uzbektelecom",
    "Uzmobile",
    "Ucell",
    "Beeline",
    "Perfectum Mobile",
    "Uzonline",
    "Uzinfocom",
    "Uzpakhtasanoat",
    "Uzdonmahsulot",
    "Uzdoninvest",
    "Mars IT",
    "Uzavtosanoat",
    "Akfa Medline",
    "Tatu",
    "Uztransgaz",
    "Uztrans",
    "Havo Yollari",
    "Oftob medline",
    "Kapitalbank",
    "GM",
    "BYD",
    "KIA",
    "Sanata",
    "Chery",
]

from CheckApp.models import CheckModel
from CheckApp.serializers import CheckSerializer, CreateCheckSRL
import random

import qrcode
class CheckView(APIView):
    @swagger_auto_schema(request_body=CreateCheckSRL)
    def post(self, request):
        user = request.data.get('user')
        money = request.data.get('money')
        user_money = CardUser.objects.all().filter(card_holder=int(user))
        for i in user_money:
            if i.money >= money:
                qolgan_pul = i.money - money
                update = CardUser.objects.all().filter(card_holder=user).update(money=qolgan_pul)
                seriya_raqam = random.randint(10000, 99999)
                fiksal_raqam = ''
                for i in range(14):
                    fiksal_raqam += str(random.randint(1, 9))
                fiksal_belgi = ""
                for i in range(6):
                    fiksal_belgi += str(random.randint(1, 9))
                check_raqam = ""
                for i in range(10):
                    check_raqam += str(random.randint(1, 9))

                create = CheckModel.objects.create(user_id=int(user), money=money, seriya_raqam=seriya_raqam,
                                                   fiskal_raqam=fiksal_raqam, fiskal_belgi=int(fiksal_belgi),
                                                   check_raqam=int(check_raqam))
                create.save()
                print("Saqlandi")
                qrcode_data = f"http://164.92.99.180:8000/pay/pay/cashback/{fiksal_raqam}/"
                img = qrcode.make(qrcode_data)
                img.save(f"uploads/{fiksal_raqam}_qr.png")

                cashback = money / 100

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                pdf.cell(200, 10, txt="Check raqami: " + str(check_raqam), ln=1, align="C")
                pdf.cell(200, 10, txt="Seriya raqami: " + str(seriya_raqam), ln=1, align="C")
                pdf.cell(200, 10, txt="Fiskal raqami: " + str(fiksal_raqam), ln=1, align="C")
                pdf.cell(200, 10, txt="Fiskal belgi: " + str(fiksal_belgi), ln=1, align="C")
                pdf.cell(200, 10, txt="Korxona nomi: " + random.choice(davlat_korxonalari), ln=1, align="C")
                pdf.cell(200, 10, txt="Xaridor: " + str(user), ln=1, align="C")
                pdf.cell(200, 10, txt="Tovar narxi: " + str(money), ln=1, align="C")
                pdf.cell(200, 10, txt="Cashback: " + str(cashback), ln=1, align="C")
                # pdf.output(f"uploads/check{fiksal_belgi}.pdf")
                #save to pdf qrcode png
                pdf.image(f"uploads/{fiksal_raqam}_qr.png", x=80 - 10, y=80, w=80)
                pdf.output(f"uploads/check{fiksal_belgi}.pdf")
                # return Response({"MSG": "OK"}, status=status.HTTP_200_OK)
                #in response show pdf file
                with open(f"uploads/check{fiksal_belgi}.pdf", 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="uploads/check{fiksal_belgi}.pdf"'
                    return response




            else:

                return Response({"MSG": "else"})

from UserApp.models import CashBackUser
class QrCodeScanView(APIView):
    def get(self, request, fiskal_raqam):
        check_filter= CheckModel.objects.all().filter(fiskal_raqam=int(fiskal_raqam),status=1)
        print(check_filter)
        if check_filter:
            for i in check_filter:
                pul = i.money
                odam = i.user_id
                for i in CashBackUser.objects.all().filter(user_id=odam):
                    cashback = i.money
                update = CashBackUser.objects.all().filter(user_id=odam).update(money=cashback+int(pul)*0.01)
                one_time_use = CheckModel.objects.all().filter(fiskal_raqam=fiskal_raqam).update(status=0)
                return Response({"Qoshilgan cashback summasi": int(pul)*0.01,"Umumiy pul miqdori":cashback+int(pul)*0.01}, status=status.HTTP_200_OK)

        else:#
            return Response({"MSG": "Bu fiskal raqam allaqachon ishlatilgan"}, status=status.HTTP_400_BAD_REQUEST)





