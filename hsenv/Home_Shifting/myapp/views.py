from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
import random
import requests
from django.conf import settings
from django.urls import reverse
import razorpay
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.


def index (request):
    if request.POST:
        user = User.objects.get(uemail = request.session['uemail'])
        book = Booking.objects.filter(userid = user)

        for booking in book:
            print("======================",booking.razorpay_order_id)
            if booking.razorpay_order_id == request.POST['order_id']:
                print("hello")
                booking = get_object_or_404(Booking, pk=booking.pk)
                print(booking)
                context = {'booking': booking}
                return render(request, "utrack.html",context)
        else:
            pmsg="Please Enter Vaild Order ID"
            messages.error(request, pmsg)
            return redirect('index')

    else:
        return render(request,'index.html')

def signup(request):
    if request.POST:
        print(">>>>>>>>>>>page lode")
        try:
           print("=================Email Alredy exits===================")
           user = User.objects.get(uemail = request.POST['uemail'])
           print(">>>>>>>>>>>>>>>>Email Alredy Exist!!!!")
           msg1 = "email Alredy Exist !!!!!"
           messages.error(request,msg1)
           return redirect('index')
        except:
            if request.POST['upassword'] == request.POST['ucpassword']:
                user = User.objects.create(
                    uname = request.POST['uname'],
                    uemail = request.POST['uemail'],
                    ucontact = request.POST['ucontact'],
                    upassword = request.POST['upassword'],
                )
                print(user.uname)
                msg = "Your Registration Done ...."
                print("============",msg)
                messages.success(request, msg)
                return redirect('index')
                # add ragistration than redirect login page
            else:
                pmsg="Password and Confim Password Does Not Matched !!!"
                messages.error(request, pmsg)
                return redirect('index')
    else:
        return redirect('index')
    
def login(request):
    if request.POST:
        try:
            print("check password and email")
            user=authenticate=User.objects.get(uemail = request.POST['uemail'],upassword = request.POST['upassword'])
            request.session['uemail'] = user.uemail
            request.session['uname'] = user.uname
            request.session['upassword'] = user.upassword
            print(">>>>>>>>>session start : ",request.session['uemail'])
            print(">>>>>>>>>>>> login successfully >>>>>>>>>>>>>>>>>...")
            msg = "login successfully"
            messages.success(request,msg)
            return redirect('index')  
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            print(msg)
            return redirect('index')
    else:
        return render(request,'index.html')
    
def logout(request):
    del request.session['uemail']
    del request.session['uname']
    del request.session['upassword']
    print(">>>>>>>>>>>>>>>>>>>>>>>>LOGOUT")
    msg="Logout successfully"
    messages.success(request,msg)
    return redirect('index')

def change_pswd(request): 
   if request.POST:
       print("page lode")
       user=User.objects.get(uemail=request.session['uemail'])
       
       if user.upassword == request.POST['cu_password']:
           print("<<<<page lode user cureent password perfect >>>>>>")

           if request.POST['npassword'] == request.POST['cpassword']:
               print("========Page Loade new password and conifrm password match =========")
               user.upassword = request.POST['cpassword']
               user.save()
               return redirect('logout')
           else:
                msg = "New Password conifrm  password Does not match..."
                messages.error(request,msg)
                return redirect('login')
       else:
           msg1="Current Password Does not match !!!"
           messages.error(request,msg1)
           return redirect('login') 
   else:
       return redirect('login')
   
   
def forget_pswd(request):
    if request.POST:
        try:
            print("====================================page loade =======================================")
            user = User.objects.get(ucontact = request.POST['ucontact'])
            mobile = request.POST['ucontact']
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
            msg = "Otp Sent Successfully.........."
            print(msg)
            print(response.text)
            request.session['mobile']=mobile
            request.session['otp']=otp
            return render(request,'otp.html')
        except Exception as e:
                print(e)
                print("===========except page loade==============")
                msg = "invalid Phone Number  !!!"
                return render(request,"forget_password.html")
    else:
        print("==============================else part run ====================================")
        return render(request,"forget_password.html")
    
def otp(request):
    if request.method=="POST":     
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        print(type(otp))
        print(type(uotp))
        
        if otp==uotp:
          print("Hello")
          del request.session['otp']
          return render(request,"reset_password.html")
        else:
          msg = "Invalid Otp"
          print(msg)
          messages.error(request,msg)
          return render(request,"otp.html")
    else:
        return render(request,"otp.html")
    
def resetpass(request):
     print("=========== resetpage page hello===============")
     if request.POST:
         print("=========== request page hello===============")
         try:
            print("===========hello===============")
            user = User.objects.get(ucontact = request.session['mobile'])
            if request.POST['npassword']==request.POST['cnpassword']:
                print("===========1  hello===============")
                user.upassword =request.POST['npassword']
                user.save()
                return  redirect('index')
            else:
                pass
         except  Exception as e:
             print(e)
     else: 
         return render(request,'reset_password.html')
       

def booking(request):
    if 'uemail' in request.session:
  
        if request.POST:
            userid = User.objects.get(uemail=request.session['uemail'])
            price = int(request.POST.get('price'))
            book = Booking.objects.create(
                htype=request.POST['htype'],
                userid=userid,
                bname=request.POST['name'],
                movefrom=request.POST['moving_from'],
                moveto=request.POST['moving_to'],
                state=request.POST['state'],
                zipcode=request.POST['zipcode'],
                price=price
            )
            
            print(type(book.price))
            print("=================================")
    
            client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': book.price * 100, 'currency': 'INR', 'payment_capture': 1})
            book.razorpay_order_id = payment['id']
            book.save()

            request.session['name']= book.bname
            print(request.session['name'])

            context = {
                    'payment': payment,
                    'book':book,  # Ensure the amount is in paise
                }
            
            print("=======================",context)
            print("&7777777777777777777777",payment)
            

        
            return render(request, 'payment.html',context)
        else:
            return render(request, "booking.html")

    else:
        messages.info(request, "Please login now.........")
        return render(request, "booking.html")

def mybooking(request):
    user = User.objects.get(uemail = request.session['uemail'])
    user_bookings = Booking.objects.filter(userid=user)
    print(user_bookings)
    return render(request,"mybooking.html",{'user_bookings': user_bookings})

def payments(request):
    return render (request,"payment.html")

def mymail(subject, template, to, context,order_id):
    subject = subject
    template_str = template +'.html'
    context['order_id'] = order_id
    html_message = render_to_string(template_str, context)
    plain_message = strip_tags(html_message)
    from_email = 'kurmipurshottam@gmail.com'
    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message,
        fail_silently=False,
    )

def success(request):
    uemail = request.session.get('uemail')

    if uemail:
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        if razorpay_payment_id!="":
            # Update the booking instance with the Razorpay payment ID
            booking.razorpay_payment_id = razorpay_payment_id
            booking.save()

            subject = 'booking successfully'
            template = "success_email"
            to = user.uemail
            context = {'user':user.uname}
            order_id = booking.razorpay_order_id
            mymail(subject, template, to, context,order_id)
            print('======================send otp successfully')
        else:
            msg = "pyament failed"
            messages.error(request,msg)
            booking.delete()
            return redirect('index')

        return render(request, 'success.html')
    else:
        msg= "Please login....."
        messages.info(request,msg)
        return render(request,"index.html")

     
def vehical (request):  
    return render(request,'vehical.html')

def service (request):
    return render(request,'services.html')

def contact(request):
    if request.POST:
        contact = Contact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            number = request.POST['mobile'],
            message = request.POST['msg']
        )
        print("uuuuuuuuuuuussssssssssssseeeeeeeeeeeeeeeeerrrrrrrrrrrrrr")
        msg = "message send successfully"
        messages.success(request,msg)
        return redirect('index')
    else:
        return render(request,'contact.html')

def about(request):
    return render(request,"about.html")

def utrack(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    context = {'booking': booking}
    print(context)
    return render(request, "utrack.html", context)

def cancel(request,pk):
    uemail = request.session.get('uemail')
    booking = Booking.objects.get(pk=pk)
    user = get_object_or_404(User, uemail=uemail)
    # Check if the booking is not already canceled
    if booking.status != 'cancel':
        if booking.status != 'finish':
            # Set the status to 'cancel'
            booking.status = 'cancel'
            booking.save()
            if booking.status == 'cancel':
                # Update the booking instance with the Razorpay payment ID
                subject = 'booking cancel successfully'
                template = "cancel_email"
                to = user.uemail
                context = {'user':user.uname}
                order_id = booking.razorpay_order_id
                mymail(subject, template, to, context,order_id)
                print('======================send successfully')
                msg="Booking Cancel Successfully"
                messages.success(request,msg)

                # Redirect back to the user's bookings page
                return redirect('mybooking')
            
        else:
            msg="Booking Already Finished"
            messages.info(request,msg)
            # Redirect back to the user's bookings page
            return redirect('mybooking')
    else:
        msg="Booking Already Cancel"
        messages.error(request,msg)
        # Redirect back to the user's bookings page
        return redirect('mybooking')