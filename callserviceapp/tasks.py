from celery import shared_task

from math import asin, cos, radians, sin, sqrt
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
import base64

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



