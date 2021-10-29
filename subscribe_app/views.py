import re
from subscribe_app.models import Razorpay_Detail, Subscribe_Plan, User, User_Profile
from .serializer import  RegisterSerializer,LoginSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import  api_view, permission_classes,authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json

import environ
import razorpay
from rest_framework.response import Response

import environ
env = environ.Env()
environ.Env.read_env()

class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class StartPaymentApiView(GenericAPIView):
    authentication_classes = [JWTAuthentication,]
    def post(self,request):
        amount = request.data['amount']
        user = request.user
        user_email = user.email
        user_obj = User.objects.get(email=user_email)
        sub_plan = Subscribe_Plan.objects.get(subscibe_plan='30days')
        if sub_plan.amount != float(amount):
            return Response({'message':'Please enter correct amount for this plan'})
        client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
        payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
        
        user_profile = User_Profile.objects.create(user=user_obj,sub_plan=sub_plan,order_id=payment['id'])
        razorpay_obj = Razorpay_Detail.objects.create(user=user_obj,payment_id = payment['id'],amount=amount)
        data = {
            'payment':payment,
            'order_id':user_profile.order_id
        }
        return Response(data)


from datetime import datetime,timedelta, timezone



class HandlePaymentApivie(GenericAPIView):
    def post(self,request):
        raz_pay_id = request.data['azorpay_payment_id']
        order_id = request.data['razorpay_order_id']
        raz_signature = request.data['razorpay_signature']
        value = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature}

        client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
        check = client.utility.verify_payment_signature(value)
        if check is not None:
            print("Redirect to error url or error page")
            return Response({'error': 'Something went wrong'})
        user= request.user
        user_profile = User_Profile.objects.get(order_id=order_id,user=user)
        user_profile.is_subscribed = True
        user_profile.subscribe_date = datetime.now()
        user_profile.expiry_date = datetime.now()+ timedelta(days=30)
        user_profile.save()
        razorpay_obj = Razorpay_Detail.objects.get(user=user,payment_id=order_id)
        razorpay_obj.success_status  = True
        razorpay_obj.save()
        return Response({'message':'Payment Successful'})


class CancelSubscription(GenericAPIView):
    authentication_classes = [JWTAuthentication,]
    def get(self,request):
        user = request.user
        if user.is_manager == True:
            user_obj = User_Profile.objects.get(user=user)
            if user_obj.expiry_date == datetime.now():
                user_obj.is_subscribed =  False
                user_obj.save()
                return Response({'message':'It will expired Today'})
            if user_obj.is_subscribed == True:
                avail_days = (datetime.now(timezone.utc) - user_obj.subscribe_date).days
                if avail_days >= 0:
                    return Response({'message':"You don't have any left days"})
                user_obj.is_cancel = True
                user_obj.cancel_date = datetime.now()
                print(user_obj.subscribe_date)
                user_obj.left_day = (datetime.now(timezone.utc) - user_obj.subscribe_date).days
                print(user_obj.left_day)
                user_obj.save()
                return Response({'message':'You have canceled your Subscription Successfully'})
            return Response({'message':"You haven't Subscribe yet"})
        return Response({'message':"You don't have the permission to cancel"})

class ResumeSubcription(GenericAPIView):
    authentication_classes = [JWTAuthentication,]
    def get(self,request):
        user = request.user
        user_obj = User_Profile.objects.get(user=user)
        print(user_obj.left_day)
        if user.is_cancel == False:
            return Response({'message':"You didn't cancel the plan or don't have any active plan"})
        if user_obj.left_day == 0:
            return Response({'message':"You don't have any left days"})
        user_obj.expiry_date = datetime.now(timezone.utc)+ timedelta(days=int(user_obj.left_day))
        user_obj.is_cancel = False
        user_obj.left_day = 0
        user_obj.save()
        return Response({'message':'You have resume your subscription successfully'})





        