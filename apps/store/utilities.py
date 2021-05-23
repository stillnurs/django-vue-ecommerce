from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from apps.order.views import render_to_pdf
from django.http import HttpResponse

def decrement_product_quantity(order):
    for item in order.items.all():
        product = item.product
        product.num_available = product.num_available - item.quantity
        product.save()

# def send_order_confirmation(order):
#     subject = 'Order confirmation'
#     from_email = 'noreply@dropshipper_django_vue.com'
#     to = ['mail@dropshipper_django_vue.com', order.email]
#     text_content = 'Your order is successful!'
#     html_content = render_to_string('order_confirmation.html', {'order': order})

#     pdf = render_to_pdf('order_pdf.html', {'order': order})

#     msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#     msg.attach_alternative(html_content, "text/html")

#     if pdf:
#         name = 'order_%s.pdf' % order.id
#         msg.attach(name, pdf, 'application/pdf')
    
#     msg.send()

def send_order_confirmation(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Your order is successful!'
    html_content = render_to_string('order_confirmation.html', {'order': order})

    pdf = render_to_pdf('order_pdf.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    if pdf:
        name = 'order_%s.pdf' % order.id
        msg.attach(name, pdf, 'application/pdf')
    
    msg.send()
    

def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    subject = 'New order'
    text_content = 'You have a new order!'
    for vendor in order.vendors.all():
        to_email = vendor.created_by.email
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


