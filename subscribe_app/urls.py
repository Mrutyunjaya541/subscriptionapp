from django.urls import path
from .views import RegisterApiView,LoginApiView,StartPaymentApiView,HandlePaymentApivie,CancelSubscription,ResumeSubcription

urlpatterns = [
    path('register/',RegisterApiView.as_view(),name='register'),
    path('login/',LoginApiView.as_view(),name='register'),
    path('start_payment/',StartPaymentApiView.as_view(),name='start_payment'),
    path('handle_payment/',HandlePaymentApivie.as_view(),name='handle_payment'),
    path('cancel_sub/',CancelSubscription.as_view(),name='cancel_sub'),
    path('resume_sub/',ResumeSubcription.as_view(),name='resume_sub')
]