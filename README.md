# subscriptionapp

Main aim of this project is to provide suscription app for one month to user.
If the user is manager then he can cancel the subscription and resume the subscription.
Here I'm using Razorpay for payment accecpting.

projrct_flow :---

- create a virtual environment 
- install django
- install django rest framework
- django-admin startproject <project name>
- django admin startapp <app name>
- 	add the app to settings.py in installed apps
- 	add views in app from views.py
- 	map this view to urls.py (using url mapping or include function)

- make all the models 
- 	python manage.py migrate
- 	register the changes in model: python manage.py makemigrations <app name>
- 	python manage.py migrate
- 	register your models in admin.py file of that application
- 	create superuser to get access to admin interface
  
 - Start django-server
  -- python manage.py runserver
  
 Here I'm integrating Razorpay for accepting payment from the user.
  Here you find 2 urls for payment profile
  one for starting payment.
  and another one for handling the payment.
  
If you are a manager the you will able to cancel or resume your subscription.
  For manager access you need to request the admin to give manager access.
  Admin will give you the manager access.
  
For Signup you need:-
  
  Email,first_name,last_name,dob,address,comapny and password

For login you need :-
  
  Email and password
  
For manager access contact to admin:-
