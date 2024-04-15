from django.db import models
from myapp.models import *
from django.utils import timezone
from datetime  import timedelta
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class Truckpartner(models.Model):
	t_name = models.CharField(max_length = 50)
	t_email = models.EmailField(unique=True , max_length = 50)
	t_contact = models.CharField(max_length = 11)
	t_password = models.CharField(max_length = 50)
	t_rcnumber = models.CharField(max_length = 10)
	t_aadharcard_details = models.CharField(max_length = 12 , unique = True)
	t_pancard_details = models.CharField(max_length = 10 , unique = True)
	t_drivinglicence_details = models.CharField(max_length = 15 , unique = True)
	t_picture = models.ImageField(default="profile/default-picture.png",upload_to="profile/")
	status = models.BooleanField(default = False)
	on_work = models.BooleanField(default = False)
	#=========================================================================================
	#====================================================================================
	package_type = models.CharField(max_length=20,null=True)
	price = models.PositiveIntegerField(null=True)
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(null = True)
	truck_type = models.CharField(max_length=20,null = True)
      
	def __str__(self):
		return self.t_name 
	
class Rides(models.Model):
	truckpartner = models.ForeignKey(Truckpartner,on_delete = models.CASCADE, null = True)
	total_trip = models.PositiveIntegerField(default = 0 , null = True)
	start_time = models.DateTimeField(null = True)
	expiry_time = models.DateTimeField(null = True)
	today_earning = models.PositiveBigIntegerField(default = 0, null = True)
	total_earning = models.PositiveBigIntegerField(default = 0, null = True)

	def __str__(self):
	    return self.truckpartner.t_name	
	
class Transactions(models.Model):
	truckpartner = models.ForeignKey(Truckpartner,on_delete=models.CASCADE , null = True)
	rides = models.ForeignKey(Rides,on_delete=models.CASCADE , null = True)
	account_holder_name = models.CharField(max_length = 20)
	account_number = models.PositiveIntegerField()
	ifsc_code = models.CharField(max_length=11)
	date = models.DateField(default = timezone.now)
	amount = models.PositiveBigIntegerField(default = 0)

	def __str__(self):
		return self.truckpartner.t_name  

class Contacts(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	number = models.CharField(max_length=50)
	message = models.TextField(max_length=1000)
	
	def __str__(self):
		return self.name	
