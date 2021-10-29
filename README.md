# subscriptionapp

Main aim of this project is to provide suscription app for one month to user.
If the user is manager then he can cancel the subscription and resume the subscription.
Here I'm using Razorpay for payment accecpting.

projrct_flow :---

create a project by using(django-admin startproject project_name)
create a virtualenv
activate virtualenv
install django by using pip
install all the modules required for this project by using (pip3 install -r requirements.txt)

Then create the app by using(python3 manage.py startapp app_name)

add the app_name in settings.py 
after that run
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver

