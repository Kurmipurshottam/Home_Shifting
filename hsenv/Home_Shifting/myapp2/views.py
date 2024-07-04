from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random
import requests
from django.conf import settings
from django.urls import reverse
import razorpay
from datetime import datetime, timedelta
from myapp.models import *

# Create your views here.
def delivery_signup(request):
    if request.POST:
        print(">>>>>>>>>>>page lode")
        try:
            print("=================Email Already exists===================")
            truckpartner = Truckpartner.objects.get(t_email=request.POST['email'])
            print(">>>>>>>>>>>>>>>>Email Already Exist!!!!")
            msg = "Email Already Exist !!!!!"
            messages.error(request, msg)
            return redirect('delivery_signup')
        except Truckpartner.DoesNotExist:
            if request.POST['password'] == request.POST['confirm_password']:
                try:
                    truckpartner = Truckpartner.objects.create(
                        t_name=request.POST['name'],
                        t_aadharcard_details=request.POST['aadhaar_card'],
                        t_pancard_details=request.POST['pan_card'],
                        t_drivinglicence_details=request.POST['driving_licence'],
                        t_rcnumber=request.POST['rc_number'],
                        t_contact=request.POST['contact'],
                        t_email=request.POST['email'],
                        t_password=request.POST['password'],
                    )
                    print(truckpartner.t_name)
                    msg = "Your Registration Done ...."
                    print("============", msg)
                    messages.success(request, msg)
                    return render(request, "packages_details.html")
                except IntegrityError as e:
                    if 'UNIQUE constraint failed' in str(e):
                        msg = "Pan Card details already exist!"
                        messages.error(request, msg)
                    else:
                        msg = "An error occurred during registration. Please try again."
                        messages.error(request, msg)
                    return redirect('delivery_signup')
            else:
                pmsg = "Password and Confirm Password Do Not Match !!!"
                messages.error(request, pmsg)
                return redirect('delivery_signup')
    else:
        return render(request, 'delivery_signup.html')

def delivery_login(request):
    if request.POST:
        try:
            print("check password and email")
            truckpartner=Truckpartner.objects.get(t_email = request.POST['email'],t_password = request.POST['pass'])
            print("hello")
            if truckpartner.razorpay_payment_id:
                request.session['email'] = truckpartner.t_email
                request.session['name'] = truckpartner.t_name
                request.session['contact'] = truckpartner.t_contact
                request.session['password'] = truckpartner.t_password
                request.session['picture'] = truckpartner.t_picture.url
                truckpartner.status = True
                truckpartner.save()
                print('login status truck',truckpartner.status)
                print("true")
                print(">>>>>>>>>session start : ",request.session['email'])
                print(">>>>>>>>>>>> login successfully >>>>>>>>>>>>>>>>>...")
                msg = "login successfully"
                messages.success(request,msg)
                return redirect('delivery_index')  
            else:
                msg = "Package Purches First"
                messages.error(request,msg)
                return render(request,"packages.html")
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            print(msg)
            return redirect('delivery_login')
    else:
        return render(request,"delivery_login.html")

    
def delivery_logout(request):
    if request.session['email']:
        truck=Truckpartner.objects.get(t_email=request.session['email'])
        truck.status=False
        print(truck.status)
        truck.save()
        print("========================================")
        del request.session['email']
        del request.session['name']
        del request.session['password']
        del request.session['contact']
        del request.session['picture']
        msg="Logout successfully"
        messages.success(request,msg)
        return redirect('delivery_signup')

def delivery_forget(request):
    # return render(request,"delivery_forget.html")
    if request.POST:
        try:
            print("====================================page loade =======================================")
            truckpartner = Truckpartner.objects.get(t_contact = request.POST['contact'])
            mobile = request.POST['contact']
            otp = random.randint(1000,9999)
            print(type(otp))

            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {
                           "authorization":"49df8FP3OhnqKAuB6OcTLAAEMmfB23tmRFHiDFZRZ7zrpONWyuhl6B3wFteN",
                           "variables_values":str(otp),
                           "route":"otp",
                           "numbers":mobile
                        }

            headers = {
                'cache-control': "no-cache"
               }

            response = requests.request("GET", url, headers=headers, params=querystring)
            msg = "Otp Sent Successfully"
            messages.success(request,msg)
            print(msg)
            print(response.text)
            request.session['mobile']=mobile
            request.session['otp']=otp
            return render(request,'delivery_otp.html')
        except Exception as e:
                print(e)
                print("===========except page loade==============")
                msg = "invalid Phone Number  !!!"
                messages.error(request,msg)
                return render(request,"delivery_forget.html")
    else:
        print("==============================else part run ====================================")
        return render(request,"delivery_forget.html")

def delivery_otp(request):
    if request.method=="POST":     
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        print(type(otp))
        print(type(uotp))
        
        if otp==uotp:
          print("Hello")
          del request.session['otp']
          msg="Otp Verify Successfully"
          messages.success(request,msg)
          return render(request,"delivery_reset_password.html")
        else:
          msg = "Invalid Otp"
          print(msg)
          messages.error(request,msg)
          return render(request,"delivery_otp.html")
    else:
        return render(request,"delivery_otp.html")    

def delivery_reset(request):
     print("=========== resetpage page hello===============")
     if request.POST:
         print("=========== request page hello===============")
         try:
            print("===========hello===============")
            truckpartner = Truckpartner.objects.get(t_contact = request.session['mobile'])
            if request.POST['new_password']==request.POST['cnew_password']:
                print("===========1  hello===============")
                truckpartner.t_password =request.POST['cnew_password']
                truckpartner.save()
                msg="password Reset Successfully"
                messages.success(request,msg)
                return  redirect('delivery_login')
            else:
                msg="password And Confirm Password Does Not Match"
                messages.error(request,msg)
                return redirect('delivery_reset_password')
         except  Exception as e:
             print(e)
     else: 
         return render(request,'delivery_reset-password.html')

def delivery_change_password(request):
    try:
        print("page load")
        if request.method == 'POST':
            print("post request")
            email = request.session['email']
            if email:
                truckpartner = Truckpartner.objects.get(t_email=email)
                if truckpartner.t_password == request.POST['old_password']:
                    if request.POST['new_password'] == request.POST['cnew_password']:
                        truckpartner.t_password = request.POST['cnew_password']
                        truckpartner.save()
                        messages.success(request, "Password changed successfully. Please login with your new password.")
                        return redirect('delivery_logout')
                    else:
                        msg = "New Password and Confirm New Password do not match..."
                        messages.error(request, msg)
                        return redirect('delivery_change_password')
                else:
                    msg1 = "Current Password does not match!"
                    messages.error(request, msg1)
                    return redirect('delivery_change_password')
            else:
                msg1 = "User not logged in!"
                messages.error(request, msg1)
                return redirect('delivery_login')
        else:
            print("page load, but not a POST request")
            return render(request, 'delivery_change_password.html')
    except Exception as e:
        print(e)
        print("Exception occurred while changing password")
        msg1 = "An error occurred while changing password. Please try again later."
        messages.error(request, msg1)
        return redirect('delivery_change_password')

def delivery_mywallet(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
        ride = Rides.objects.get(truckpartner = truckpartner)
        print("============",ride)
        transactions = Transactions.objects.filter(truckpartner = truckpartner)
        a = 0
        for i in transactions:
            a += i.amount
        
        print("============",transactions)
        current_datetime = timezone.now()

        if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
            ride.today_earning = 0
            ride.save()

        return render(request,'delivery_mywallet.html',{'ride':ride,'transactions':transactions,'a':a})
    except Exception as e:
        print(e)
        return render(request,'delivery_mywallet.html')


def delivery_index(request):
    try:
        uemail = request.session.get('uemail')
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
        truckpartner = Truckpartner.objects.get(t_email=request.session['email'])
        if truckpartner.status == True:
            if booking.statuscheck == False:
                if booking.status != 'finish' and booking.status != 'cancel':
                    uemail = request.session.get('uemail')
                    user = get_object_or_404(User, uemail=uemail)
                    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
                    if booking.htype in ['2 BHK'] and truckpartner.package_type in ['silver', 'gold','platinum']:
                        return render(request, "delivery_index.html", {'user': user, "booking": booking, "truckpartner": truckpartner})
                    elif booking.htype in ['1 BHK'] and truckpartner.package_type in ['silver','platinum']:
                        return render(request, "delivery_index.html", {'user': user, "booking": booking, "truckpartner": truckpartner})
                    elif booking.htype in ['3 BHK'] and truckpartner.package_type in ['gold','platinum']:
                        return render(request, "delivery_index.html", {'user': user, "booking": booking, "truckpartner": truckpartner})
                    elif booking.htype in ['4 BHK'] and truckpartner.package_type == 'platinum':
                        return render(request, "delivery_index.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
                else:
                    return render(request, "delivery_index.html")
            else:
                return render(request, "delivery_index.html")
        else:
            return render(request, "delivery_index.html")

    except:
        pass
    return render(request,"delivery_index.html")

def accept(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
        
        uemail = request.session.get('uemail')
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

        truckpartner.on_work = True
        truckpartner.save()

        booking.statuscheck = True
        booking.save()

        uemail = request.session.get('uemail')
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
        print("------------------",booking.finish_active)
        return render(request,"accept.html",{'user':user , "booking":booking})
    except Exception as e:
        print('============---------------',e)
        pass
    return render(request,"delivery_index.html")
        
    
def reject(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
    truckpartner.on_work = False
    truckpartner.save()
    reject_status=False
    if truckpartner.on_work == False:
        reject_status=True
        msg="Ride Rejected Successfully"
        messages.success(request,msg)
        return render(request,"delivery_index.html",{'reject_status':reject_status})
    else:
        msg="Ride Rejected Failed"
        messages.error(request,msg)
        return redirect('delivery_index')

def finishride(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
    truckpartner.on_work = False
    
    uemail = request.session.get('uemail')
    user = get_object_or_404(User, uemail=uemail)
    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
    booking.statuscheck = False
    booking.status = 'finish'
    truckpartner.save()
    booking.save()

    #----------------------------------------------------
    uemail = request.session.get('email')
    user = get_object_or_404(User, uemail=uemail)
    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
    

    ride = Rides.objects.get(truckpartner = truckpartner)
    if ride.today_earning == 0:
        ride.start_time =  timezone.now()
        ride.expiry_time = ride.start_time + timedelta(days=1)
        ride.save()

    current_datetime = timezone.now()

    if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
        ride.today_earning = 0
        ride.save()

        # Update total_trip and total_earning
    ride.total_trip += 1
    ride.today_earning += booking.price
    ride.total_earning += booking.price
    ride.save()

    print("------------------------------",booking.finish_active)
    return redirect('delivery_index')

def delivery_profile(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
    ride = Rides.objects.get(truckpartner = truckpartner)
    print("555555555555555555555555555555555555555555555555555555555555555555555555555",ride)
    try:
        current_datetime = timezone.now()
        if ride.expiry_time is not None:
            if current_datetime >= ride.expiry_time:
                    # If last ride was more than 24 hours ago, reset today's earnings to 0
                ride.today_earning = 0
                ride.save()
            print(ride.today_earning)
            return render(request,'delivery_profile.html',{"truckpartner":truckpartner , 'ride':ride})
        else:
            return render(request,'delivery_profile.html',{"truckpartner":truckpartner , 'ride':ride})
    except:
        return render(request,'delivery_profile.html',{"truckpartner":truckpartner , 'ride':ride})
  
def delivery_contact(request):
    if request.POST:
        contact = Contacts.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            number = request.POST['number'],
            message = request.POST['msg']
        )
        print("==============================")
        msge = "message send successfully"
        messages.success(request,msge)
        return redirect('delivery_index')
    else:
        return render(request,"delivery_contact.html")

def delivery_Withdrawal_funds(request):
    return render(request,"delivery_Withdrawal_funds.html")

def delivery_profile_update(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
        if request.POST:
            truckpartner.t_name = request.POST['name']
            truckpartner.t_contact = request.POST['contact']
            if 'profile_picture' in request.FILES:
                truckpartner.t_picture = request.FILES['profile_picture']
            truckpartner.save()

            request.session['name'] = truckpartner.t_name
            request.session['picture'] = truckpartner.t_picture.url
            request.session['contact'] = truckpartner.t_contact
            
            msg ="profile successfully update"
            messages.success(request,msg)
            return redirect('delivery_profile')
        else:
            return render(request,"delivery_profile_update.html")
    except:
        pass
   
def packages(request):
    if request.POST:
        try:
            truck =Truckpartner.objects.get(t_email = request.POST['email'])

            price = int(request.POST.get('price'))
            
            truck.price = price
            truck.package_type = request.POST['ptype']
            truck.truck_type = request.POST['vtype']
            truck.end_date = truck.start_date+timedelta(days=30)
            print('==========truckprice',truck.price)


            client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': truck.price * 100, 'currency': 'INR', 'payment_capture': 1})
            truck.razorpay_order_id = payment['id']  
            truck.save()
            #creating a session and use in delivery success views
            request.session['temail']= request.POST['email']
            #print(p)
            context = {
                    'payment': payment,
                    'truck':truck,  # Ensure the amount is in paise
                }
            print(context)
            return render(request,'delivery_payments.html',context)

        except Exception as e:
            msg="Email is Not Registered"
            messages.error(request,msg)
            return render(request,"packages.html")
    else:
        return render(request,"packages.html")
    
def delivery_success(request):
    try:
        print("==============================================")
        #it fatch the session that create in the packages
        truck = Truckpartner.objects.get(t_email = request.session['temail'])

        print('========================================',truck.t_email)

        truck.razorpay_payment_id = request.GET.get('razorpay_payment_id')

        print('========================================',truck.razorpay_payment_id)
        truck.save()
        ride = Rides.objects.create(

            truckpartner = truck
        
        )
        print("---------------create ride for truckpartners",ride)
        return render(request, 'delivery_success.html')
    except Exception as e:
        print(e)
        return render(request, 'delivery_success.html')
    
def packages_details(request):  
    return render(request,"packages_details.html")

def delivery_payments(request):
    return render(request,"delivery_payments.html")

def Withdrawal_funds(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['email'])
        ride = Rides.objects.get(truckpartner = truckpartner)

        if request.POST:
            print("==========post")
            if request.POST['accountno'] == request.POST["caccountno"]:
                print("==========first",type(ride.total_earning))
                print("==========first",type(request.POST["amount"]))
                if ride.total_earning >= int(request.POST["amount"]):
                    print("==========second")
                    transactions = Transactions.objects.create(
                        truckpartner = truckpartner,
                        rides = ride,
                        account_holder_name = request.POST['hname'],
                        account_number = request.POST['accountno'],
                        ifsc_code = request.POST['ifsc_code'],
                        amount = request.POST['amount'],
                    )
                    ride.total_earning -= int(request.POST["amount"])
                    ride.save()

                    return redirect('delivery_mywallet')
                else:
                    msg="your balance low please enter limited amount !!"
                    messages.error(request,msg)
                    return render(request,'delivery_Withdrawal_funds.html')
            else:
                msg="account number and confirm account number does not match !!"
                messages.error(request,msg)
                return render(request,'delivery_Withdrawal_funds.html')
        else:
            return render(request,'delivery_Withdrawal_funds.html')    
    except Exception as e:
        print(e)
        return render(request,'delivery_Withdrawal_funds.html')