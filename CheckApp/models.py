from django.db import models
from UserApp.models import User

class CheckModel(models.Model):
    status = models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    seriya_raqam = models.IntegerField(unique=True)
    fiskal_raqam = models.CharField(unique=True,max_length=14)
    fiskal_belgi = models.IntegerField(unique=True)
    check_raqam = models.IntegerField(unique=True)
    korxona_nomi = models.CharField(max_length=40,null=True)
    money = models.IntegerField(default=None)


    def __str__(self):
        return str(self.fiskal_raqam)


# Create your models here.
