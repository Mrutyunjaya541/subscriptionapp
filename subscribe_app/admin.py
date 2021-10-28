from django.contrib import admin

# Register your models here.
from .models import User,User_Profile,Subscribe_Plan,Razorpay_Detail

admin.site.register(User)
admin.site.register(User_Profile)
admin.site.register(Subscribe_Plan)
admin.site.register(Razorpay_Detail)