from callserviceapp.models import order
from math import asin, cos, radians, sin, sqrt
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
import base64


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'servidor.ssmtp@gmail.com'
EMAIL_HOST_PASSWORD = 'lgdi xmko ztgk vipm' #past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'default from email'

def send_user_mail(randomNumber, email):
    subject = 'Validación de e-mail - ServicesYA'
    cuerpo="Su número de validación es: "+str(randomNumber)

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo ,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1

def send_proveedor_mail_new_orden(ticket, email, usuario):
    subject = 'Nueva orden de servicio - Ticket: '+ticket+" - ServicesYA!"
    cuerpo = "Posee nueva solicitud de trabajo."+'\n'+'\n' + "Solicitud creada por: "+usuario+'\n'

    #message.attach_alternative(content, 'text/html')
    send_mail(subject, cuerpo,'servidor.ssmtp@gmail.com', [email],fail_silently = False) #Destinatario)
    return 1


def distanciaEnLaTierra(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

#Toma el tipo de proveedor, un arreglo de proveedores, la latitud y longitud del cliente y un rango de radio 
#De cada proveedor obtiene la distancia hasta el cliente. Si está dentro del radio devuleve la lista de proveedor
def proveedoresRadio(tipo, array, proveedores, lat, long, radio1, radio2, cantidad_proveedores_maxima):
    
    if proveedores:
        datos_de_proveedores=[]
        distancias=[]
        i=0
        for data in proveedores:
            #distance = math.sqrt(math.pow(data.posicion_lat-float(lat), 2) + math.pow(data.posicion_long-float(long), 2) )
            distance=distanciaEnLaTierra(float(data.posicion_long),float(data.posicion_lat),float(long),float(lat))
            
            if radio1 <= distance and distance < radio2:
                datos_de_proveedores.append(data)
                distancias.append(distance)
                i=i+1
                if i==cantidad_proveedores_maxima:
                    break
        
        if tipo==1: 
            j=0
            for datos in datos_de_proveedores:
                personales=datos.provider
                imagenes={}
            
                if personales.picture:
                    imagenes['picture']= "data:image/png;base64,"+base64.b64encode(personales.picture.read()).decode('ascii')
                else:
                    imagenes['picture']=""

                first={"item":datos.items,"certificado":imagenes['picture'] ,"distancia":distancias[j],
            "calificacion":datos.qualification,
                "nombre":personales.name, "apellido":personales.last_name, "email":personales.email, "tipo":"Proveedor de servicio independiente" }

                array.append(first)
                j=j+1
                                
        else: 
            j=0
            for datos in datos_de_proveedores:
                personales=datos.provider
                imagenes={}
            
                if personales.picture:
                    imagenes['picture']= "data:image/png;base64,"+base64.b64encode(personales.picture.read()).decode('ascii')
                else:
                    imagenes['picture']=""

                first={"item":datos.items,"certificado":imagenes['picture'] ,"distancia":distancias[j],
            "calificacion":datos.qualification,
                "nombre":personales.company_name, "apellido":personales.company_description, "email":personales.email, "tipo":"Empresa proveedora de servicio" }

                array.append(first)
                j=j+1
        return array

def ordenarProveedores(array):
    auxiliar=[] 
    for data in array:
        if not order.objects.filter(proveedor_email=array.email):
            auxiliar.append(data)
    i=0
    posicion=0
    for data in auxiliar:
        if data.calificacion > i: 
            i= data.calificacion
            posicion=posicion+1

    return auxiliar[posicion]
    
    #ahora si ordenar y obtener uno


