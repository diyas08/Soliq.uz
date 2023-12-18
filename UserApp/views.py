from django.shortcuts import render
from .serializers import  UserSerializer,Login_SRL
from .models import User
from rest_framework.response import  Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class RegistrationView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        phone = request.data.get("phone")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.filter(phone=phone).first()
            if user:
                access = AccessToken.for_user(user)
                refresh = RefreshToken.for_user(user)
                print(f"{access}\n{refresh}")
                return Response({
                    "DATA": serializer.data,
                    "ACCESS": str(access),
                    "REFRESH": str(refresh)
                })
        return Response(serializer.errors)
    #



class Login(APIView):
# Create your views here.
    queryset = User.objects.all()
    serializer_class = Login_SRL
    @swagger_auto_schema(request_body=Login_SRL)
    def post(self,request):
        name=request.data.get('name')
        password=request.data.get('password')
        user = User.objects.all().filter(name=name,password=password)
        return Response({"MSG":"SUCCSESS"})

class LogOut(APIView):
    def get(self,request,pk):
        user=User.objects.all().filter(id=pk).first()
        if user:
            refresh=RefreshToken.for_user(user)
            return Response({"REFRESH TOKEN":str(refresh)})
        else:
            return Response({"ERRORS":"TOKEN ERROR"})



