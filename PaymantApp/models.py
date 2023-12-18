from django.db import models
from UserApp.models import User

class CardUser(models.Model):
    card_holder = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.IntegerField(default=8600,unique=True)
    money = models.IntegerField(default=0)
    expired_date = models.DateTimeField()

    def __str__(self):
        return str(self.card_holder)

# Create your models here.
