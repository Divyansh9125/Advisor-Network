from rest_framework import serializers
from .models import Advisor, Booked_Call

class advisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = '__all__'

class callSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booked_Call
        fields = ['advisor.name', ]