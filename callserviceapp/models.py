from sqlite3 import Timestamp
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser


class validation_token (models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    val_token= models.IntegerField(default=0)


class user_data (models.Model):

    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    client_type= models.IntegerField(default=1, blank=True) 
    name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    picture=models.ImageField(upload_to='media/', blank=True)	
    qualification=models.IntegerField(default=0)
    cantidad_ordenes_realizadas =models.IntegerField(default=0)
    cantidad_ordenes_canceladas =models.IntegerField(default=0) 
    posicion_lat = models.FloatField(default=None, null=True)
    posicion_long= models.FloatField(default=None, null=True)


class item (models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    ITEMS = [
    ("CARPINTERÍA","CARPINTERÍA"),
    ("CERRAJERÍA","CERRAJERÍA"),
    ("CONSTRUCCIÓN","CONSTRUCCIÓN"),
    ("CONTADURÍA","CONTADURÍA"),
    ("ELECTRICIDAD","ELECTRICIDAD"),
    ("ELECTRÓNICA","ELECTRÓNICA"),
    ("ESTÉTICA","ESTÉTICA"),
    ("FLETE","FLETE"),
    ("FUMIGACIÓN","FUMIGACIÓN"),
    ("GASISTA","GASISTA"),
    ("HERRERÍA","HERRERÍA"),
    ("INFORMÁTICA","INFORMÁTICA"),
    ("JARDINERÍA","JARDINERÍA"),
    ("MECÁNICA","MECÁNICA"),
    ("MODA","MODA"),
    ("PASEADOR DE MASCOTAS","PASEADOR DE MASCOTAS"),
    ("PINTOR","PINTOR"),
    ("REFRIGERACIÓN","REFRIGERACIÓN"),
    ("REMOLQUES - GRÚAS","REMOLQUES"),
    ("PLOMERÍA","PLOMERÍA"), 
    ("TELEFONÍA CELULAR","TELEFONÍA CELULAR"),
    ("TEXTIL","TEXTIL"),
    ]
    DAYS_OF_WORKS = [
    ("LUNES A VIERNES", "LUNES A VIERNES"),
    ("LUNES A LUNES", "LUNES A LUNES"),
    ]
    items = models.CharField(max_length=250, choices = ITEMS)
    certificate=models.ImageField(default=None)	
    radius = models.FloatField(default=None)
    qualification=models.IntegerField(default=0)
    publicidad=models.IntegerField(default=0) #valor que dependerá de si pagó publicidad

    hace_orden_emergencia = models.BooleanField(default=False)

    pais= models.TextField(blank = True)
    provincia= models.TextField(blank = True)
    ciudad= models.TextField(blank = True)
    domicilio_calle= models.TextField(blank = True)
    domicilio_numeracion=models.TextField(blank = True)
    description= models.TextField(blank = True)
    days_of_works = models.CharField(max_length=250,choices= DAYS_OF_WORKS,default= "LV")
    hour_init = models.TimeField()
    hour_end = models.TimeField()
    picture1=models.ImageField(default=None, blank=True)	
    picture2=models.ImageField(default=None,blank=True)	
    picture3=models.ImageField(default=None, blank=True)	
    
    #hour_price=	models.FloatField(default=None)
    def __str__(self):
        return str(self.provider.email)


#################################################################################################################
#Models for orders


class ordenGeneral (models.Model):
    
    id = models.AutoField(primary_key=True)

    client_email = models.EmailField(blank=True)
    proveedor_email=models.EmailField(blank=True)
    rubro= models.OneToOneField(item,blank=True,null=True,on_delete=models.CASCADE)
    tiempo_respuesta_promedio=models.FloatField(default=1000)

    fecha_creacion=models.DateField( auto_now_add=True)
    ticket =  models.IntegerField(default=1000, blank=True)

    STATUS = [
        ("ENV","ENVIADA"), #Generada por el cliente
        ("REC","RECIBIDA"), # la vio el proveedor
        ("PEI","PEDIDO INFORMACION"), #el proveedor pide mas info
        ("RES", "RESPUESTA DEL CLIENTE"), #EL CLIENTE RESPONDIO
        ("PRE","PRESUPUESTADA"), #PRESUPUESTADA POR EL PROVEEDOR
        ("ACE","ACEPTADA"), #ACEPTADA POR EL CLIENTE
        ("EVI","EN VIAJE"), #EL PROVEEDOR EN VIAJE
        ("ENS","EN SITIO"), # EL PROVEEDOR EN SITIO
        ("RED","REALIZADA"), #REALIZADA
        ("CAN","CANCELADA"), #CANCELADA
        ("REX","RECHAZADA"), #RECHAZADA
    ]
    status = models.CharField(max_length=3,choices= STATUS,default= "SO")
       
    location_lat = models.FloatField(default=None, blank=True)
    location_long = models.FloatField(default=None, blank=True)
    
    day = models.TextField(default="",blank=True)
    time = models.TextField(default="",blank=True)
   
    tituloPedido = models.TextField(default="Solicitud de pedido")
    problem_description = models.TextField(default=None, blank=True)
   # direccion = models.TextField(default=None, blank=True)
    picture1=models.ImageField(default=None, blank=True)
    picture2=models.ImageField(default=None,blank=True)

    presupuesto_inicial=models.FloatField(default=0)
    pedido_mas_información=models.TextField(default="")
    respuesta_cliente_pedido_mas_información=models.TextField(default=0)
    picture1_mas_información=models.ImageField(default=None, blank=True)
    picture2_mas_información=models.ImageField(default=None,blank=True)

    motivo_rechazo=models.TextField(default=None, blank=True)

    califico_el_cliente=models.BooleanField(default=False)
    califico_el_proveedor=models.BooleanField(default=False)
    calificacion_proveedor= models.IntegerField(default=0)
    calificacion_cliente=models.IntegerField(default=0)
    resena_al_proveedor=models.TextField(default = None, blank=True)    
    resena_al_cliente=models.TextField(default = None, blank=True)    


class ordenEmergencia (models.Model):

    id = models.AutoField(primary_key=True)

    STATUS = [
        ("ENV","ENVIADA"), #GENERADA POR EL CLIENTE - BUSCANDO PROVEEDORES
        ("ACE","ACEPTADA"), #ACEPTADA POR PROVEEDOR
        ("EVI","EN VIAJE"), #PROVEEDOR EN VIAJE
        ("ENS","EN SITIO"), #PROVEEDOR EN SITIO
        ("RED","REALIZADA"), #ORDEN REALIZADA
        ("CAN","CANCELADA"), #ORDEN CANCELADA POR CLIENTE
        ("REX","RECHAZADA"), #ORDEN RECHAZADA POR PROVEEDOR
    ]
    status = models.CharField(max_length=3,choices= STATUS,default= "ENV")

    rubro= models.TextField(blank=True)

    client_email = models.EmailField(blank=True)
    proveedor_email=models.EmailField(blank=True)
    
    fecha_creacion=models.DateField( auto_now_add=True)
    ticket =  models.IntegerField(default=1000, blank=True)
   
    location_cliente_lat = models.FloatField(default=None, blank=True)
    location_cliente_long = models.FloatField(default=None, blank=True)
   
    problem_description = models.TextField(blank=True)
    picture1=models.ImageField(default=None, blank=True)
    picture2=models.ImageField(default=None,blank=True)

    motivo_rechazo=models.TextField(default=None, blank=True)

    califico_el_cliente=models.BooleanField(default=False)
    califico_el_proveedor=models.BooleanField(default=False)
    calificacion_proveedor= models.IntegerField(default=0)
    calificacion_cliente=models.IntegerField(default=0)
    resena_al_proveedor=models.TextField(default = None, blank=True)    
    resena_al_cliente=models.TextField(default = None, blank=True)  


class ordenEmergenciaLista (models.Model):
    STATUS = [
        ("CE","CORREO ENVIADO"),
        ("OA","ORDEN ACEPTADA"),
    ]

    rubro=models.TextField(blank=True)
    ticket = models.IntegerField(default=1000, blank=True) 
    proveedor_email=models.EmailField(blank=True)
    status = models.CharField(max_length=3,choices= STATUS,default= "SO")


class chat (models.Model): 
    id = models.AutoField(primary_key=True)
    mensaje=models.TextField(blank=True)
    user= models.EmailField(blank=True)
    ticket = models.IntegerField(default=1000, blank=True) 
    day = models.TextField(blank=True,  null=True)
    time = models.TextField(blank=True, null=True)
    timestamp = models.TimeField(auto_now_add=True)
    daystamp = models.DateField(auto_now_add=True)
  
class nuevo_chat (models.Model): 
    notify_to=models.EmailField(blank=True)
    message_from=models.EmailField(blank=True)
    ticket = models.IntegerField(default=1000, blank=True) 


################################################################################################


class campañaPublicidad (models.Model):
    id = models.AutoField(primary_key=True)

    TYPE = [
        ("EM", "EMAIL"),
        ("HO", "HOME"),
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    type = models.CharField(max_length=2,choices= TYPE,default= "HO")
    


