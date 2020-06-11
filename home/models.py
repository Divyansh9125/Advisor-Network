from django.db import models
from user.models import UserProfile

class Advisor(models.Model):
    """
    This model class stores the advisor data:
    1. Advisor's name
    2. Advisor's Photo URL
    """
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Booked_Call(models.Model):
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=False)