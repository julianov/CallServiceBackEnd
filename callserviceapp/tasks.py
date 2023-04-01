from celery import shared_task

from math import asin, cos, radians, sin, sqrt
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail

from callservices import celery


@shared_task()
def send_user_mail(randomNumber, email):
    subject = 'Validación de e-mail - ServicesYA'
    cuerpo="Su número de validación es: "+str(randomNumber)

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo ,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1

@shared_task()
def send_proveedor_mail_new_orden(ticket, email, usuario):
    subject = "Nueva orden de servicio - Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "Posee nueva solicitud de trabajo."+'\n'+'\n' + "Solicitud creada por: "+str(usuario)+'\n'

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1


@shared_task()
def send_orden_emergencia(ticket, email , categoria,descripcion_problema):
    
    subject = "ORDEN DE EMERGENCIA - Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "Orden de emergencia"+'\n'+'\n'+"Posee nueva solicitud de trabajo."+'\n'+'\n' + "Categoría: "+str(categoria)+'\n'+'\n'+'\n'+descripcion_problema

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1


@shared_task()
def send_proveedor_mail_more_info(ticket, informacion_solicitada, email):
    subject = "Solicitud de más información - Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "El proveedor de servicio solicita la siguiente información."+'\n'+'\n' +str(informacion_solicitada)+'\n'+'\n'+"Recuerde, cuanta más información le brinde al proveedor, más fácil es presupuestarle el trabajo."

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1

@shared_task()
def send_client_mail_more_info(ticket, informacion_solicitada, response, email):
    subject = "Respuesta a la solicitud de más información - Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "El cliente ha respondido a la solicitud"+'\n'+'\n' +str(informacion_solicitada)+'\n'+'\n'+"Con la siguiente información"+'\n'+str(response)

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1

@shared_task()
def send_proveedor_change_date (ticket, new_date, new_time, email):
    subject = "Cambio de fecha de orden de servicio - Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "El proveedor ha cambiado la fecha y hora de la orden de servicio"+'\n'+'\n' +str(new_date)+' '+str(new_time) +'\n'+'\n'+"Puede comunicarse con el proveedor mediante el chat en la aplicación"

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1


@shared_task()
def send_proveedor_on_trip (ticket, proveedor, rubro, email):
    subject = "Proveedor en camino! - Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "El proveedor se encuentra en camino a su locación para realizar la orden de servicio"+'\n'+'\n' +str(proveedor)+'\n'+str(rubro) +'\n'+'\n'+"Puede comunicarse con el proveedor mediante el chat en la aplicación"

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1

@shared_task()
def send_proveedor_order_canceled (ticket, proveedor, rubro, motivo, email):
    subject = "Proveedor ha cancelado la orden- Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "El proveedor ha cancelado la orden de servicio"+'\n'+'\n'+"Rubro: "+str(rubro)+'\n'+"Proveedor: "+str(proveedor)+'\n'+"Motivo: "+str(motivo)

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1

@shared_task()
def send_client_order_canceled (ticket, rubro, motivo, email, usuario):
    subject = "Cliente ha cancelado la orden- Ticket: "+str(ticket)+" - ServicesYA!"
    cuerpo = "El cliente ha cancelado la orden de servicio"+'\n'+'\n'+"Rubro: "+str(rubro)+'\n'+"Cliente: "+str(usuario)+'\n'+"Motivo: "+str(motivo)

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1
