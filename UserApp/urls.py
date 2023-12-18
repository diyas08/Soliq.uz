from django.urls import path
from .views import Login, RegistrationView,LogOut

urlpatterns=[
    path('login/' ,  Login.as_view()),
    path('register/', RegistrationView.as_view()),
    path("Logout/<int:pk>/",LogOut.as_view())
]

