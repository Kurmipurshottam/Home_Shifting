from django.contrib import admin
from .models import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table,TableStyle
# Register your models here.

# admin.site.register(User)
# admin.site.register(Booking)
# admin.site.register(Contact)

#==================================================

def export_to_pdf(modeladmin, request, queryset):
# Create a new PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Generate the report using ReportLab

    # Custom page size (width, height)
    custom_page_size = (900, 600)
    doc = SimpleDocTemplate(response, pagesize=custom_page_size)
    elements = []

    # Define the style for the table
    style = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])

    #Create the table data
    data = []
    for obj in queryset:
        #  data.append([obj.uname, obj.uemail,
        #  obj.ucontact,obj.upassword])

        # data.append([obj.htype,obj.bname,
        # obj.movefrom,obj.moveto,obj.state,obj.zipcode,obj.price,obj.razorpay_order_id,obj.razorpay_payment_id,obj.date])
           
           data.append([obj.name, obj.email,
           obj.number,obj.message])
        
    # Create the table
    t = Table( data, style=style)
    # Add the table to the elements array
    elements.append(t)
    # Build the PDF document
    doc.build(elements)
    return response

export_to_pdf.short_description = "Export to PDF"



class ShowUser(admin.ModelAdmin):
    list_display = ['uname', 'uemail', 'ucontact', 'upassword']
    actions = [export_to_pdf]

admin.site.register(User, ShowUser)

class ShowBooking(admin.ModelAdmin):
    list_display = ['htype', 'bname', 'movefrom', 'moveto', 'state', 'zipcode', 'price', 'razorpay_order_id', 'razorpay_payment_id']  # Removing 'date' field from 'list_display'
    actions = [export_to_pdf]

admin.site.register(Booking, ShowBooking)


class ShowContact(admin.ModelAdmin):
    list_display = ['name', 'email', 'number', 'message']
    actions = [export_to_pdf]

admin.site.register(Contact, ShowContact)