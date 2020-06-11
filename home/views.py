import jwt, json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Advisor, Booked_Call
from user.models import UserProfile
from .serializers import advisorSerializer, callSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def homeView(request):
    return render(request, 'home/index.html')

@api_view(['POST'])
@login_required
def addAdvisor(request):
    """
    Add advisor like:
    {
        "name": "__advisor_name__",
        "url" : "__photo_url__"
    }
    """
    if request.user.is_admin:
        if request.method == 'POST':
            name = request.data['name']
            url= request.data['url']
            if url is not None and name is not None:
                advisor = Advisor(name=name, url=url)
                advisor.save()
                return Response([{"Success":"Advisor Added"}], status=200)
            else:
                return Response([{"Error":"Send all fields"}], status=400)
    else:
        return Response([{"Error":"You are not admin"}], status=401)

@api_view(['POST'])
def loginView(request):
    """
    Send login data like:
    {
        "email": "__user_email__",
        "password" : "__user_password__"
    }
    """
    if request.method=='POST':
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            resp = {'token':token, 'user_id':user.pk}

            return Response([resp], status=200)
        else:
            return HttpResponse([{'Error':"Authentication failed"}], status=401)

@api_view(['POST'])
def registerView(request):
    """
    Send user data like:
    {
        "first_name": "_first_name__",
        "last_name" : "__last_name__",
        "email": "__user_email__",
        "password" : "__user_password__"
    }
    """
    if request.method == 'POST':
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        password = request.data['password']

        if first_name is not None and last_name is not None and email is not None and password is not None:

            user = UserProfile.objects.create_user(first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            resp = {'token':token, 'user_id':user.pk}

            return Response([resp], status=200)
        else:
            return HttpResponse([{'Error':"Bad Request"}], status=400)

@login_required
@api_view(['GET'])
def getAdvisors(request, user_id):
    if request.method == 'GET':
        if request.user.pk == user_id:
            advisors = Advisor.objects.all()
            serializer = advisorSerializer(advisors, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response([{"Error":"You are not current user"}], status=403)

@login_required
@api_view(['POST'])
def bookCall(request, user_id, advisor_id):
    """
    Send call booking data like:
    {
        "date_time": "_date_time__"
    }
    """
    if request.method == 'POST':
        if request.user.pk == user_id:
            user = UserProfile.objects.get(pk=user_id)
            advisor = Advisor.objects.get(pk=advisor_id)
            date_time = request.data['date_time']

            call = Booked_Call(user=user, advisor=advisor, date_time=date_time)
            call.save()

            return Response([{'Success':"Call Booked"}], status=200)

@login_required
@api_view(['GET'])
def getAllCalls(request, user_id):
    if request.method == 'GET':
        if request.user.pk == user_id:
            user = UserProfile.objects.get(pk=user_id)
            calls = Booked_Call.objects.all().filter(user=user)
            resp = []
            for obj in calls:
                call = {}
                call["call_id"] = obj.pk
                call["advisor"] = {
                    "id": obj.advisor.pk,
                    "name": obj.advisor.name,
                    "photo_url": obj.advisor.url
                }
                call["booking_time"] = obj.date_time
                resp.append(call)

            return Response(resp, status=200)
        else:
            return Response([{"Error":"You are not current user"}], status=403)
