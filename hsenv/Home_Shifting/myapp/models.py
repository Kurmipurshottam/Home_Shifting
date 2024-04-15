from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=40)
    uemail = models.EmailField()
    ucontact = models.CharField(max_length=15)
    upassword = models.CharField(max_length=40)
    

    def __str__(self):
        return  self.uname + " || " + self.uemail   
    
class Booking(models.Model):
    ORDERSTATUS = (("house-type","house-type"),("Booking","Booking"),("payment-status","payment-status"),("on-the-way","on-the-way"),("cancel","Cancle"),("finish","finish process"))
    htype = models.CharField(max_length=40,null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    bname = models.CharField(max_length=40)
    movefrom = models.TextField(max_length=40)
    moveto = models.TextField(max_length=40)    
    state = models.CharField(max_length=40)
    zipcode = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=20,choices = ORDERSTATUS,default="Booking")
    statuscheck = models.BooleanField(default = False)

     # Add flags for statuses
    house_type_active = models.BooleanField(default=False)
    booking_active = models.BooleanField(default=False)
    payment_status_active = models.BooleanField(default=False)
    on_the_way_active = models.BooleanField(default=False)
    cancel_active = models.BooleanField(default=False)
    finish_active = models.BooleanField(default=False)

    def get_all_processes(self):
        return [status[0] for status in self.ORDERSTATUS]
    
    def save(self, *args, **kwargs):
        # Set flags based on the current status
        current_status = self.status
        self.house_type_active = current_status == 'house-type'
        self.booking_active = current_status == 'Booking'
        self.payment_status_active = current_status == 'payment-status'
        self.on_the_way_active = current_status == 'on-the-way'
        self.cancel_active = current_status == 'cancel'
        self.finish_active = current_status == 'finish'

        super().save(*args, **kwargs)

    def __str__(self):
        return  self.bname + " || " + self.htype    
    
class Contact(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	number = models.CharField(max_length=50)
	message = models.TextField(max_length=1000)
	
	def __str__(self):
		return self.name   