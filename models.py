from django.db import models

# Create your models here.

class client(models.Model):
    #user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()	
    random_number= models.IntegerField(default=0)
    name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    picture=models.ImageField(upload_to='media/', blank=True)	
    qualification=models.IntegerField(default=0)

    def __str__(self):
        return self.email

class serviceProvider(models.Model):
    #user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(default=None)	
    random_number= models.IntegerField(default=0)
    name = models.CharField(max_length=200, blank=True)  
    last_name = models.CharField(max_length=200, blank=True)
    picture=models.ImageField(blank=True)	

    def __str__(self):
        return self.email


class item (models.Model):
    ITEMS = [
    ("CARPINTERÍA","CARPINTERÍA"),
    ("CERRAJERÍA","CERRAJERÍA"),
    ("ELECTRICIDAD","ELECTRICIDAD"),
    ("ELECTRÓNICA","ELECTRÓNICA"),
    ("FLETE","FLETE"),
    ("GASISTA","GASISTA"),
    ("HERRERÍA","HERRERÍA"),
    ("INFORMÁTICA","INFORMÁTICA"),
    ("JARDINERÍA","JARDINERÍA"),
    ("MECÁNICA","MECÁNICA"),
    ("PLOMERÍA","PLOMERÍA"),
    ("REFRIGERACIÓN","REFRIGERACIÓN"),
    ("TELEFONÍA CELULAR","TELEFONÍA CELULAR"),
    ("TEXTIL","TEXTIL"),
    ]
    DAYS_OF_WORKS = [
    ("LUNES A VIERNES", "LUNES A VIERNES"),
    ("LUNES A LUNES", "LUNES A LUNES"),
    ]
    items = models.CharField(max_length=25, choices = ITEMS)
    certificate=models.ImageField(default=None)	
    provider = models.ForeignKey(serviceProvider, on_delete=models.CASCADE, null=True)
    radius = models.FloatField(default=None)
    qualification=models.IntegerField(default=0)

    pais= models.TextField(blank = True)
    provincia= models.TextField(blank = True)
    ciudad= models.TextField(blank = True)
    domicilio_calle= models.TextField(blank = True)
    domicilio_numeracion=models.TextField(blank = True)
    posicion_lat = models.FloatField(default=None)
    posicion_long= models.FloatField(default=None)
    description= models.TextField(blank = True)
    days_of_works = models.CharField(max_length=25,choices= DAYS_OF_WORKS,default= "LV")
    hour_init = models.TimeField()
    hour_end = models.TimeField()
    picture1=models.ImageField(default=None, blank=True)	
    picture2=models.ImageField(default=None,blank=True)	
    picture3=models.ImageField(default=None, blank=True)	
    
    #hour_price=	models.FloatField(default=None)
    def __str__(self):
        return str(self.provider.email)

class company (models.Model):
    #user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(default=None)
    random_number= models.IntegerField(default=0)
    company_name = models.CharField(max_length=200, blank=True)  
    company_description = models.CharField(max_length=200, blank=True)  

    picture=models.ImageField(default=None)	
	
    def __str__(self):
        return self.email   

class item_company (models.Model):
    ITEMS = [
    ("CARPINTERÍA","CARPINTERÍA"),
    ("CERRAJERÍA","CERRAJERÍA"),
    ("ELECTRICIDAD","ELECTRICIDAD"),
    ("ELECTRÓNICA","ELECTRÓNICA"),
    ("FLETE","FLETE"),
    ("GASISTA","GASISTA"),
    ("HERRERÍA","HERRERÍA"),
    ("INFORMÁTICA","INFORMÁTICA"),
    ("MECÁNICA","MECÁNICA"),
    ("PLOMERÍA","PLOMERÍA"),
    ("REFRIGERACIÓN","REFRIGERACIÓN"),
    ("TELEFONÍA CELULAR","TELEFONÍA CELULAR"),
    ("TEXTIL","TEXTIL"),
    ]
    DAYS_OF_WORKS = [
    ("LV", "LUNES A VIERNES"),
    ("LL", "LUNES A LUNES"),
    ]
    items = models.CharField(max_length=25, choices = ITEMS)
    certificate=models.ImageField(upload_to='media/')	
    provider = models.ForeignKey(company, on_delete=models.CASCADE)
    description= models.TextField(blank = True)
    radius = models.FloatField(default=None)
    qualification=models.IntegerField(default=0)

    pais= models.TextField(blank = True)
    provincia= models.TextField(blank = True)
    ciudad= models.TextField(blank = True)
    domicilio_calle= models.TextField(blank = True)
    domicilio_numeracion=models.TextField(blank = True)
    posicion_lat = models.FloatField(default=None)
    posicion_long= models.FloatField(default=None)
    days_of_works = models.CharField(max_length=25,choices= DAYS_OF_WORKS,default= "LV")
    hour_init = models.TimeField()
    hour_end = models.TimeField()
    picture1=models.ImageField(default=None, blank=True)	
    picture2=models.ImageField(default=None, blank=True)	
    picture3=models.ImageField(default=None, blank=True)
   # hour_price=	models.FloatField(default=None)

class order (models.Model):
    STATUS = [
        ("SO", "SOLICITADA"),
        ("EC", "EN CURSO"),
        ("CE", "CERRADA"),
    ]

    client = models.ForeignKey(client, on_delete=models.CASCADE)
    serviceProvider = models.ForeignKey(serviceProvider, on_delete=models.CASCADE)
    status = models.CharField(max_length=2,choices= STATUS,default= "SO")
    item= models.ForeignKey(item, on_delete=models.CASCADE)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    day = models.DateField()
    time = models.TimeField()
    problem_description = models.TextField()




