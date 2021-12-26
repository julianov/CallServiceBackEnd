from django.db.models.fields import DateTimeCheckMixin, DateTimeField
from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from json import loads

from callserviceapp.models import  client, item_company, ordenEmergencia, ordenGeneral, serviceProvider, item
from callserviceapp.models import company

from callserviceapp.utils import distanciaEnLaTierra, ordenarProveedores, proveedoresRadio, send_proveedor_mail_new_orden, send_user_mail
import random

import base64
import math

import datetime
import datetime




# Create your views here.


def homeCliente (request , lat, long):
    array=[]

    #datos_independiente=item.objects.exclude(radius=0).order_by('-qualification')
    datos_independiente=item.objects.order_by('-publicidad','-qualification')
    proveedoresRadio(1,array,datos_independiente,lat,long,0,30,6)
        
    #datos_companias=item_company.objects.exclude(radius=0).order_by('-qualification')
    datos_companias=item_company.objects.order_by('-publicidad','-qualification')
    proveedoresRadio(2,array,datos_companias,lat,long,0,30,6)
    
    if len(array)<=5:
        proveedoresRadio(1,array,datos_independiente,lat,long,30,150,6)        
        proveedoresRadio(2,array,datos_companias,lat,long,30,150,6)
        if len(array)==0:
            return HttpResponse("bad")
        else:
            return JsonResponse(array, safe=False)
    else:
        return JsonResponse(array, safe=False)

def homeClientePedirDatos (request , email,rubro, tipoPedido,lat, long):  
    
    datos_personales=serviceProvider.objects.filter(email=email).first()
   
    if datos_personales:
        datosItem= item.objects.filter(provider=datos_personales).filter(items=rubro).first()
        if datosItem:
            if (tipoPedido=="caracteres"):        
                
                distance=distanciaEnLaTierra(float(datosItem.posicion_long),float(datosItem.posicion_lat),float(long),float(lat))
                if datos_personales.picture:
                    imagen="data:image/png;base64,"+base64.b64encode(datos_personales.picture.read()).decode('ascii')
                else: 
                    imagen=""  

                data={"tipo":"Proveedor de servicio independiente","name":datos_personales.name, "last_name":datos_personales.last_name, "picture":imagen,"distancia":distance,
                    "items":datosItem.items, "qualification":datosItem.qualification,"days_of_works":datosItem.days_of_works,
                    "hour_init":datosItem.hour_init,"hour_end":datosItem.hour_end,"description":datosItem.description,
                    "radio":datosItem.radius,"pais":datosItem.pais, "provincia":datosItem.provincia, "ciudad":datosItem.ciudad, 
                    "calle":datosItem.domicilio_calle, "numeracion":datosItem.domicilio_numeracion }
                
                return JsonResponse(data, safe=False)
            else:
                imagenes={}
                
                if datosItem.certificate: 
                    imagenes['certificate']="data:image/png;base64,"+base64.b64encode(datosItem.certificate.read()).decode('ascii')
                else: 
                    imagenes['certificate']=""
                if datosItem.picture1: 
                    imagenes['picture1']="data:image/png;base64,"+base64.b64encode(datosItem.picture1.read()).decode('ascii')
                else: 
                    imagenes['picture1']=""
                if datosItem.picture2: 
                    imagenes['picture2']="data:image/png;base64,"+base64.b64encode(datosItem.picture2.read()).decode('ascii')
                else: 
                    imagenes['picture2']=""
                if datosItem.picture3: 
                    imagenes['picture3']="data:image/png;base64,"+base64.b64encode(datosItem.picture3.read()).decode('ascii')
                else: 
                    imagenes['picture3']=""
                data={"certificate":imagenes['certificate'] ,"picture1":imagenes['picture1'] , "picture2": imagenes['picture2'], "picture3":imagenes['picture3'] ,
                     }
                
                return JsonResponse(data, safe=False)  

        else:
            return HttpResponse("bad") 
    else: 
        datos_compania=company.objects.filter(email=email).first()
        if datos_compania: 
            datos_item_compania=item_company.objects.filter(provider=datos_compania).filter(items=rubro).first()
            if datos_item_compania:
                imagenes={}
                if datos_compania.picture:
                    imagenes['picture']="data:image/png;base64,"+base64.b64encode(datos_compania.picture.read()).decode('ascii')
                else: 
                    imagenes['picture']=""
                if datos_item_compania.certificate: 
                    imagenes['certificate']="data:image/png;base64,"+base64.b64encode(datos_item_compania.certificate.read()).decode('ascii')
                else: 
                    imagenes['certificate']=""
                if datos_item_compania.picture1: 
                    imagenes['picture1']="data:image/png;base64,"+base64.b64encode(datos_item_compania.picture1.read()).decode('ascii')
                else: 
                    imagenes['picture1']=""
                if datos_item_compania.picture2: 
                    imagenes['picture2']="data:image/png;base64,"+base64.b64encode(datos_item_compania.picture2.read()).decode('ascii')
                else: 
                    imagenes['picture2']=""
                if datos_item_compania.picture3: 
                    imagenes['picture3']="data:image/png;base64,"+base64.b64encode(datos_item_compania.picture3.read()).decode('ascii')
                else: 
                    imagenes['picture3']=""            
                
                distance=distanciaEnLaTierra(float(datos_item_compania.posicion_long),float(datos_item_compania.posicion_lat),float(long),float(lat))
                
                data={"tipo":"Empresa de servicios" ,"name":datos_compania.company_name, "last_name":datos_compania.company_description, "picture":imagenes['picture'],"distancia":distance,
                "items":datos_item_compania.items, "qualification":datos_item_compania.qualification,"days_of_works":datos_item_compania.days_of_works,
                "hour_init":datos_item_compania.hour_init,"hour_end":datos_item_compania.hour_end,"description":datos_item_compania.description,
                "certificate":imagenes['certificate'] ,"picture1":imagenes['picture1'] , "picture2": imagenes['picture2'], "picture3":imagenes['picture3']  ,
                "radio":datos_item_compania.radius,"pais":datos_item_compania.pais, "provincia":datos_item_compania.provincia, "ciudad":datos_item_compania.ciudad, 
                "calle":datos_item_compania.domicilio_calle, "numeracion":datos_item_compania.domicilio_numeracion}
            
                return JsonResponse(data, safe=False)
                
            else: 
                return HttpResponse("bad")


def register (request, type, email, password):
    if type == '1':
        #nuevo usuario
        cliente=client.objects.filter(email=email)
        proveedor_independiente=serviceProvider.objects.filter(email=email)
        proveedor_empresa=company.objects.filter(email=email)

        if not (cliente and proveedor_independiente and proveedor_empresa):
            print("no objetos se crea nuevo")
            randomNumber = random.randint(1, 99999)
            send_user_mail(randomNumber, email)
            b = client( email=email, password=password)
            b.save()
            return HttpResponse(randomNumber)
        else:
            return HttpResponse("User alredy taken")
    if type == '2':
        #nuevo proveedor de servicios
        cliente=client.objects.filter(email=email)
        proveedor_independiente=serviceProvider.objects.filter(email=email)
        proveedor_empresa=company.objects.filter(email=email)
        
        if not (cliente and proveedor_independiente and proveedor_empresa):
            randomNumber = random.randint(1, 99999)
            send_user_mail(randomNumber, email)
            b = serviceProvider( email=email, password=password)
            b.save()
            return HttpResponse(randomNumber)
        else:
            return HttpResponse("User alredy taken")
    if type == '3':
        #nueva empresa
        cliente=client.objects.filter(email=email)
        proveedor_independiente=serviceProvider.objects.filter(email=email)
        proveedor_empresa=company.objects.filter(email=email)
        
        if not (cliente and proveedor_independiente and proveedor_empresa):
            randomNumber = random.randint(1, 99999)
            send_user_mail(randomNumber, email)
            b = company( email=email, password=password)
            b.save()
            return HttpResponse(randomNumber)
        else:
            return HttpResponse("User alredy taken")
    else:
        return HttpResponse("No es cliente normal")

def askPersonalInfo(request,type,email):
    if type=="1":
        objetos=client.objects.filter(email=email)
        if objetos:
            
            if objetos.first().name==None:
                return HttpResponse("no ha cargado información personal")
            else:
                datos=objetos.first()
                imagen={}
                if datos.picture:
                    imagen['client_picture']= "data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
                else:
                    imagen['client_picture']=""
                data = [{"name": datos.name, "last_name": datos.last_name,
                "qualification": datos.qualification,},
                
                {"client_picture": imagen['client_picture']}]

                return JsonResponse(data, safe=False)
        else:
            return HttpResponse("usuario no registrado")
    if type=="2":
        objetos=serviceProvider.objects.filter(email=email)
        if not objetos: 
            return HttpResponse("usuario no registrado")
        else: 
            
            if objetos.first().name==None:
                return HttpResponse("no ha cargado información personal")
            else:
                datos=objetos.first()
                imagen={}
                if datos.picture:
                    imagen['client_picture']= "data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
                else:
                    imagen['client_picture']=""
                #if datos.imagen_promocional:
                 #   imagen['imagen_promocional']= "data:image/png;base64,"+base64.b64encode(datos.imagen_promocional.read()).decode('ascii')
                #else:
                 #   imagen['imagen_promocional']=""

                data = [{"name": datos.name, "last_name": datos.last_name,
                },
                
                {"client_picture": imagen['client_picture'] }]

                return JsonResponse(data, safe=False)

    if type=="3":
        objetos=company.objects.filter(email=email)
        if not objetos: 
            return HttpResponse("usuario no registrado")
        else: 
            if objetos.first().company_name==None:
                return HttpResponse("no ha cargado información personal")
            else:
                datos=objetos.first()
                imagen={}
                if datos.picture:
                    imagen['client_picture']= "data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
                else:
                    imagen['client_picture']=""
             #   if datos.imagen_promocional:
              #      imagen['imagen_promocional']= "data:image/png;base64,"+base64.b64encode(datos.imagen_promocional.read()).decode('ascii')
               # else:
                #    imagen['imagen_promocional']=""

                data = [{"name": datos.company_name, "description": datos.company_description,
                },
                
                {"client_picture": imagen['client_picture'] }]

                return JsonResponse(data, safe=False)
    else:
        return HttpResponse("Problema de sistema")





from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def completeInfo (request): 
    if request.method == 'POST': 
        if(request.POST.get("tipo")=="1"):
            objetos=client.objects.filter(email=request.POST.get("email"))
            if objetos:
                modelo=objetos.first()
                modelo.name=request.POST.get("nombre")
                modelo.last_name=request.POST.get("apellido")
                modelo.picture= request.FILES.get("image")
                modelo.qualification=0
                modelo.save()
                return HttpResponse("todo ok")
            else: 
                return HttpResponse("no usuario registrado")
        if(request.POST.get("tipo")=="2"):
            objetos=serviceProvider.objects.filter(email=request.POST.get("email"))
            print("a ver")
            print(request.POST.get("email"))
            if objetos:
                modelo=objetos.first()
                modelo.name=request.POST.get("nombre")
                modelo.last_name=request.POST.get("apellido")
                modelo.picture= request.FILES.get("image")
               # modelo.imagen_promocional= request.FILES.get("imagenPromocional")
                modelo.qualification=0
                modelo.save()
                return HttpResponse("todo ok")
            else: 
                return HttpResponse("no usuario registrado")
        if(request.POST.get("tipo")=="3"):
            objetos=company.objects.filter(email=request.POST.get("email"))
            if objetos:
                modelo=objetos.first()
                modelo.company_name=request.POST.get("nombre")
                modelo.company_description=request.POST.get("descripcion")
                modelo.picture= request.FILES.get("image")
              #  modelo.imagen_promocional= request.FILES.get("imagenPromocional")
                modelo.qualification=0
                modelo.save()
                return HttpResponse("todo ok")
            else: 
                return HttpResponse("no usuario registrado")  
        else:
            return HttpResponse("no usuario registrado")

@csrf_exempt 
def nuevaInfoPersonal (request): 
    if request.method == 'POST':
        

        if(request.POST.get("tipo")=="1"):
            objetos=client.objects.filter(email=request.POST.get("email"))
            if not objetos:
                return HttpResponse("no ha sido posible")
            else: 
                email=objetos.first().email
                password=objetos.first().password
                objetos.first().delete()
                new=client()
                new.email=email
                new.password=password
                new.name=request.POST.get("nombre")
                new.last_name=request.POST.get("apellido")
                new.picture= request.FILES.get("image")
                new.qualification=request.POST.get("calificacion")
                new.save() 
                return HttpResponse("ok")

        if(request.POST.get("tipo")=="2"):
            objetos_=serviceProvider.objects.filter(email=request.POST.get("email"))
            print(objetos_)
            print(serviceProvider.objects.all())
            print(request.POST.get("email"))
            if not objetos_:
                return HttpResponse("no ha sido posible")
            else: 
                email=objetos_.first().email
                password=objetos_.first().password
                objetos_.first().delete()
                new=serviceProvider()
                new.email=email
                new.password=password
                new.name=request.POST.get("nombre")
                new.last_name=request.POST.get("apellido")
                new.picture= request.FILES.get("image")
               # new.imagen_promocional= request.FILES.get("imagenPromocional")
                new.save() 
                return HttpResponse("ok")

        if(request.POST.get("tipo")=="3"):
            objetos=company.objects.filter(email=request.POST.get("email"))
            print(request.POST.get("email"))
            if not objetos:
                return HttpResponse("no ha sido posible")
            else: 
                email=objetos.first().email
                password=objetos.first().password
                objetos.first().delete()
                new=company()
                new.email=email
                new.password=password
                new.company_name=request.POST.get("nombre")
                new.company_description=request.POST.get("descripcion")
                new.picture= request.FILES.get("image")
               # new.imagen_promocional= request.FILES.get("imagenPromocional")
                new.save()
                return HttpResponse("ok")

#aca tira un error che en complete inforubros por algo relacionado al item publicidad

@csrf_exempt 
def completeInfoRubros (request,modo,tipo,email):
    print("modo: "+ modo+" tipo: "+ tipo+" email: "+email)
    if modo=="pedir":
        if tipo=="2":
            proveedores=serviceProvider.objects.filter(email=email)
            if not proveedores:
                return HttpResponse("No usuario registrado")
            else:
                rubros=item.objects.filter(provider=proveedores.first())
                print(rubros)
                if not rubros:
                    return HttpResponse ("No hay rubros cargados")
                else:                    
                    x=[]
                    for i in range(0, len(rubros)):
                        x.append(rubros[i].items+"-")
                    return HttpResponse(x)
                    #aca tengo que devolver los tipos de rubros cargados
        if tipo=="3":
            empresa=company.objects.filter(email=email)
            if not empresa:
                return HttpResponse("No usuario registrado")
            else:
                rubros=item_company.objects.filter(provider=empresa.first())
                print("tenemos un rubor:")
                print(rubros.first().items)
                if not rubros:
                    return HttpResponse ("No hay rubros cargados")
                else:
                    x=[]
                    for i in range(0, len(rubros)):
                        x.append(rubros[i].items+"-")
                        print(x)
                    return HttpResponse(x)
    return HttpResponse("No usuario registrado")



@csrf_exempt 
def addRubro (request):
    if request.method == 'POST': 
        if request.POST.get("tipo")=="2":
            proveedores=serviceProvider.objects.filter(email=request.POST.get("email"))
            if not proveedores:
                return HttpResponse("No usuario registrado")
            else:
                proveedor=proveedores.first()
                rubros=item.objects.filter(provider=proveedor)
                print("la cantidad de rubros que tiene es: "+str(len(rubros)))
               # print("los mismos son: "+rubros)
                if len(rubros)<2:
                    
                    posicion_global=(request.POST.get("posicion").split("/"))
                    print("la posición que llega es: "+str(request.POST.get("posicion")))
                    print("su longitud es: "+ str(len (posicion_global) ))
                    new = item()
                    new.items=request.POST.get("item") 
                    new.provider=proveedores.first()

                    new.radius=request.POST.get("radius")
                    if len (posicion_global) > 1:
                        new.posicion_lat= posicion_global[0]
                        new.posicion_long= posicion_global[1]
                    else:
                        new.posicion_lat=0
                        new.posicion_long=0
                    
                    new.pais=request.POST.get("pais")
                    new.provincia=request.POST.get("provincia")
                    new.ciudad=request.POST.get("ciudad")
                    new.domicilio_calle= request.POST.get("calle") 
                    new.domicilio_numeracion=request.POST.get("calle-numeracion")

                    new.qualification=0
                    new.publicidad=0
 
                    new.description=request.POST.get("description")
                    new.days_of_works=request.POST.get("days_of_works")
                    new.hour_init=request.POST.get("hour_init")
                    new.hour_end=request.POST.get("hour_end") 
                    new.certificate=request.FILES.get("certificate")	
                    new.picture1=request.FILES.get("picture1")
                    new.picture2=request.FILES.get("picture2")
                    new.picture3=request.FILES.get("picture3")
                    new.save()
                                        	
                    #new.picture3=""
                    return HttpResponse("rubro cargado")
                else:
                    return HttpResponse("ha cargado la cantidad maxima de items")
        if request.POST.get("tipo")=="3":
            proveedores=company.objects.filter(email=request.POST.get("email"))
            if not proveedores:
                return HttpResponse("No usuario registrado")
            else:
                proveedor=proveedores.first()

                rubros=item_company.objects.filter(provider=proveedor)

                if len(rubros)<2:
                    print(request.FILES.get("certificate"))
                    posicion_global=(request.POST.get("posicion").split("/"))
                    print("latitud: "+posicion_global[0])
                    print("longitud: "+posicion_global[1])

                    new = item_company()
                    new.items=request.POST.get("item") 
                    new.provider=proveedores.first()

                    new.radius=request.POST.get("radius")
                    new.qualification=0
                    new.publicidad=0
                    new.pais=request.POST.get("pais")
                    new.provincia=request.POST.get("provincia")
                    new.ciudad=request.POST.get("ciudad")
                    new.domicilio_calle= request.POST.get("calle") 
                    new.domicilio_numeracion=request.POST.get("calle-numeracion")
                    new.posicion_lat= posicion_global[0]
                    new.posicion_long= posicion_global[1]                    
                    new.description=request.POST.get("description")
                    new.days_of_works=request.POST.get("days_of_works")
                    new.hour_init=request.POST.get("hour_init")
                    new.hour_end=request.POST.get("hour_end") 
                    new.certificate=request.FILES.get("certificate")	
                    new.picture1=request.FILES.get("picture1")
                    new.picture2=request.FILES.get("picture2")
                    new.picture3=request.FILES.get("picture3")
                    new.save()	

                    #new.picture3=""
                    return HttpResponse("rubro cargado")
                else:
                    return HttpResponse("ha cargado la cantidad maxima de items")

def requestRubros(request, tipo,email,rubro):
    print("llego aqui che")
    if tipo=="2":
        proveedores=serviceProvider.objects.filter(email=email)
        if proveedores:
            rubro=item.objects.filter(provider=proveedores.first()).filter(items=rubro)
            if rubro:
                datos=rubro.first()
                images = {}
                if datos.certificate: 
                    images['certificado'] = "data:image/png;base64,"+base64.b64encode(datos.certificate.read()).decode('ascii')
                else:
                    images['certificado'] = ""
                if datos.picture1: 
                    images['imagen1'] ="data:image/png;base64,"+base64.b64encode(datos.picture1.read()).decode('ascii')
                else: 
                    images['imagen1'] =""
                if datos.picture2  : 
                    images['imagen2'] ="data:image/png;base64,"+base64.b64encode(datos.picture2.read()).decode('ascii')
                else:
                    images['imagen2'] =""
                if datos.picture3: 
                    images['imagen3'] ="data:image/png;base64,"+base64.b64encode(datos.picture3.read()).decode('ascii')
                else: 
                    images['imagen3'] =""

                data = [{"item": datos.items, "radius": str(datos.radius),
                "description": datos.description, "qualification":str(datos.qualification)},
                
                {"days_of_works": datos.days_of_works,
                "hour_init": str(datos.hour_init), "hour_end": str(datos.hour_end)},
                
                {"certificate": images['certificado'],
                "picture1": images['imagen1'],
                "picture2": images['imagen2'],
                "picture3": images['imagen3']},
                {"pais":datos.pais, "provincia":datos.provincia, "ciudad":datos.ciudad, 
                "calle":datos.domicilio_calle, "numeracion":datos.domicilio_numeracion}]
                
                return JsonResponse(data, safe=False)
                #return HttpResponse(data)
            else:
                return HttpResponse ("incongruencia de datos")
        else: 
            return HttpResponse ("incongruencia de datos")
    if tipo=="3":
        print("llego al número 3")
        proveedores=company.objects.filter(email=email)
        if proveedores:
            rubro=item_company.objects.filter(provider=proveedores.first()).filter(items=rubro)
            if rubro:
                print("tenemos el primer rubro")
                datos=rubro.first()
                images = {}
                if datos.certificate: 
                    images['certificado'] = "data:image/png;base64,"+base64.b64encode(datos.certificate.read()).decode('ascii')
                else:
                    images['certificado'] = ""
                if datos.picture1: 
                    images['imagen1'] ="data:image/png;base64,"+base64.b64encode(datos.picture1.read()).decode('ascii')
                else: 
                    images['imagen1'] =""
                if datos.picture2: 
                    images['imagen2'] ="data:image/png;base64,"+base64.b64encode(datos.picture2.read()).decode('ascii')
                else:
                    images['imagen2'] =""
                if datos.picture3: 
                    images['imagen3'] ="data:image/png;base64,"+base64.b64encode(datos.picture3.read()).decode('ascii')
                else: 
                    images['imagen3'] =""
                
                data = [{"item": datos.items, "radius": str(datos.radius),
                "description": datos.description,"qualification":str(datos.qualification)},
                
                {"days_of_works": datos.days_of_works,
                "hour_init": str(datos.hour_init), "hour_end": str(datos.hour_end)},
                
                {"certificate": images['certificado'],
                "picture1": images['imagen1'],
                "picture2": images['imagen2'],
                "picture3": images['imagen3']},
                {"pais":datos.pais, "provincia":datos.provincia, "ciudad":datos.ciudad, 
                "calle":datos.domicilio_calle, "numeracion":datos.domicilio_numeracion}]

                return JsonResponse(data, safe=False)
            else:
                return HttpResponse ("incongruencia de datos")
        else: 
            return HttpResponse ("incongruencia de datos")

@csrf_exempt 
def deleteRubro (request):
    if request.method == 'POST':
        if(request.POST.get("tipo")=="2"):
            print("aca debería llegar")
            proveedores=serviceProvider.objects.filter(email=request.POST.get("email"))
            print(proveedores)
            if proveedores:
                item.objects.filter(provider=proveedores.first()).filter(items=request.POST.get("item")).delete()
                return HttpResponse("rubro elimnado")
            else:
                return HttpResponse("no ha sido posible eliminar el rubro")
        elif (request.POST.get("tipo")=="3"):
            proveedores=company.objects.filter(email=request.POST.get("email"))
            if proveedores:
                item_company.objects.filter(provider=proveedores.first()).filter(items=request.POST.get("item")).delete()
                return HttpResponse("rubro elimnado")
            else:
                return HttpResponse("no ha sido posible eliminar el rubro")
        else:
            return HttpResponse("no ha sido posible eliminar el rubro")

@csrf_exempt 
def modificarRubro (request):
    print("lo que llego de provincia: ")
    print(request.POST.get("provincia"))
    if request.method == 'POST':
        print("el email que llego es: ")
        print(request.POST.get("email"))
        if(request.POST.get("tipo")=="2"):
            proveedores=serviceProvider.objects.filter(email=request.POST.get("email"))
            if proveedores:
                rubro=item.objects.filter(provider=proveedores.first()).filter(items=request.POST.get("item")).first()
                
                latitud=rubro.posicion_lat
                longitud=rubro.posicion_long
                calificacion=rubro.qualification
                rubro.delete()
                   
                new = item()
                new.items=request.POST.get("item") 
                new.provider=proveedores.first()

                new.radius=request.POST.get("radius")
                new.posicion_lat= latitud
                new.posicion_long=longitud
                new.pais=request.POST.get("pais")
                new.provincia=request.POST.get("provincia")
                new.ciudad=request.POST.get("ciudad")
                new.domicilio_calle= request.POST.get("calle") 
                new.domicilio_numeracion=request.POST.get("calle-numeracion")

                new.qualification=calificacion
 
                new.description=request.POST.get("description")
                new.days_of_works=request.POST.get("days_of_works")
                new.hour_init=request.POST.get("hour_init")
                new.hour_end=request.POST.get("hour_end") 
                new.certificate=request.FILES.get("certificate")	
                new.picture1=request.FILES.get("picture1")
                new.picture2=request.FILES.get("picture2")
                new.picture3=request.FILES.get("picture3")
                new.save()
                
                return HttpResponse("rubro modificado")
            else:
                return HttpResponse("no ha sido posible modificar el rubro")
        elif (request.POST.get("tipo")=="3"):
            proveedores=company.objects.filter(email=request.POST.get("email"))
            if proveedores:                
                rubro=item_company.objects.filter(provider=proveedores.first()).filter(items=request.POST.get("item"))
                latitud=rubro.posicion_lat
                longitud=rubro.posicion_long
                calificacion=rubro.qualification
                rubro.delete()
                   
                new = item()
                new.items=request.POST.get("item") 
                new.provider=proveedores.first()

                new.radius=request.POST.get("radius")
                new.posicion_lat= latitud
                new.posicion_long=longitud
                new.pais=request.POST.get("pais")
                new.provincia=request.POST.get("provincia")
                new.ciudad=request.POST.get("ciudad")
                new.domicilio_calle= request.POST.get("calle") 
                new.domicilio_numeracion=request.POST.get("calle-numeracion")

                new.qualification=calificacion
 
                new.description=request.POST.get("description")
                new.days_of_works=request.POST.get("days_of_works")
                new.hour_init=request.POST.get("hour_init")
                new.hour_end=request.POST.get("hour_end") 
                new.certificate=request.FILES.get("certificate")	
                new.picture1=request.FILES.get("picture1")
                new.picture2=request.FILES.get("picture2")
                new.picture3=request.FILES.get("picture3")
                new.save()

                return HttpResponse("rubro modificado")
            else:
                return HttpResponse("no ha sido posible modificar el rubro")
        else:
            return HttpResponse("no ha sido posible modificar el rubro")

def login(request, email, password):
    client_=client.objects.filter(email=email).filter(password=password)
    if client_:
        datos=client_.first()
        imagen={}
        if datos.picture:
            imagen['img_personal']="data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
        else:
            imagen['img_personal']=""
            
        data=[{"user":datos.email, "clientType":"1", "calificacion":datos.qualification,"picture":imagen['img_personal']}]
        return JsonResponse(data, safe=False)
            
    else: 
        serviceProvider_=serviceProvider.objects.filter(email=email).filter(password=password)
        if serviceProvider_:
            datos=serviceProvider_.first()
            imagen={}
            if datos.picture:
                imagen['img_personal']="data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
            else:
                imagen['img_personal']=""

            data=[{"user":datos.email, "clientType":"2", "picture":imagen['img_personal']}]
            return JsonResponse(data, safe=False) 
        else:
            company_=company.objects.filter(email=email).filter(password=password)
            if company_:
                datos=company_.first()
                imagen={}
                if datos.picture:
                    imagen['img_personal']="data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
                else:
                    imagen['img_personal']=""
                data=[{"user":datos.email, "clientType":"3", "picture":imagen['img_personal']}]
                return JsonResponse(data, safe=False)
            else: 
                return HttpResponse("usuario y contraseña no válidos")


def restarPassword(request, email):
    print("llego aqui")
    client_=client.objects.filter(email=email)
    if client_:
        randomNumber = random.randint(1, 99999)
        print(randomNumber)
        nuevo=client_.first()
        nuevo.random_number=randomNumber
        nuevo.save()
        send_user_mail(randomNumber, email)
        return HttpResponse(randomNumber)
    else:
        serviceProvider_=serviceProvider.objects.filter(email=email)
        if serviceProvider_:
            randomNumber = random.randint(1, 99999)
            send_user_mail(randomNumber, email)
            nuevo=serviceProvider_.first()
            nuevo.random_number=randomNumber
            nuevo.save()
            return HttpResponse(randomNumber)
        else: 
            company_=company.objects.filter(email=email)
            if company_:
                randomNumber = random.randint(1, 99999)
                send_user_mail(randomNumber, email)
                nuevo=company_.first()
                nuevo.random_number=randomNumber
                nuevo.save()
                return HttpResponse(randomNumber)   
            else:
                return HttpResponse("usuario y email no registrado")         

def setNewPassword (request, email, codigo,password):
    client_=client.objects.filter(email=email).filter(random_number=codigo)
    if client_:
        nuevo=client_.first()
        nuevo.password=password
        nuevo.save()
        return HttpResponse("Contraseña cambiada correctamente")
    else:
        serviceProvider_=serviceProvider.objects.filter(email=email).filter(random_number=codigo)
        if serviceProvider_:
            nuevo=serviceProvider_.first()
            nuevo.password=password
            nuevo.save()
            return HttpResponse("Contraseña cambiada correctamente")
        else: 
            company_=company.objects.filter(email=email).filter(random_number=codigo)
            if company_:
                nuevo=company_.first()
                nuevo.password=password
                nuevo.save()
                return HttpResponse("Contraseña cambiada correctamente")   
            else:
                return HttpResponse("usuario y email no registrado")


def ListaProveedores (datos_independiente,datos_companias):
    #datos_independientes es item
    #datos_empresa es item_company
    array=[]

    if datos_independiente:
        i=0
        print(datos_independiente)
        for datos in datos_independiente:
            print("veamos che")
            print(datos)
            print(i)
            personales=datos.provider

            imagenes={}
            
            if personales.picture:
                imagenes['picture']= "data:image/png;base64,"+base64.b64encode(personales.picture.read()).decode('ascii')
            else: 
                imagenes['picture']=""

            first={"item":datos.items,"imagen":imagenes['picture'] ,
           "calificacion":datos.qualification,
            "nombre":personales.name, "apellido":personales.last_name, "email":personales.email, "tipo":"Proveedor de servicio independiente" }

            array.append(first)
            i=i+1
            if i==10: 
                break
    
    datos_companias=item_company.objects.exclude(radius=0).order_by('-qualification')
    if datos_companias:
        i=0
        for datos in datos_companias:
            print(i)
            personales=datos.provider

            imagenes={}
            
            if personales.picture:
                imagenes['picture']= "data:image/png;base64,"+base64.b64encode(personales.picture.read()).decode('ascii')
            else: 
                imagenes['picture']=""


            first={"item":datos.items,"imagen":imagenes['picture'] ,
           "calificacion":datos.qualification,
            "nombre":personales.company_name, "apellido":"", "email":personales.email, "tipo":"Empresa de servicios" }

            array.append(first)
            i=i+1
            if i==10: 
                break
    return array

def ListaProveedoresPalabra (independiente_nombre,independiente_apellido,empresa_nombre,empresa_descripcion):
    array_items_independientes=[]
    array_items_empresa=[]
    if independiente_nombre:
        for datos in independiente_nombre:
            array_items_independientes=(item.objects.filter(provider=datos))
    if independiente_apellido: 
        for datos in independiente_apellido:
            array_items_independientes.append(item.objects.filter(provider=datos))
    if empresa_nombre:
        for datos in empresa_nombre:
            array_items_empresa=(item_company.objects.filter(provider=datos))
    if empresa_descripcion:
        for datos in empresa_descripcion:
            array_items_empresa.append(item_company.objects.filter(provider=datos))
    return ListaProveedores(array_items_independientes,array_items_empresa)
    
def Buscar (request , tipo, dato):
    if tipo=="categoria":
        categoria_a_buscar=dato
        categoria_buscada_en_independientes=item.objects.filter(items=categoria_a_buscar).order_by('-qualification')
        categoria_buscada_en_empresa=item_company.objects.filter(items=categoria_a_buscar).order_by('-qualification')
        print(categoria_buscada_en_independientes)

        if categoria_buscada_en_independientes or categoria_buscada_en_empresa:
            arreglo_a_enviar=ListaProveedores(categoria_buscada_en_independientes,categoria_buscada_en_empresa)
            if len(arreglo_a_enviar)== 0:
                return HttpResponse("bad")
            else:
                return JsonResponse(arreglo_a_enviar, safe=False)
        else:
            return HttpResponse("bad") 
    if tipo=="palabras":
        arreglo_proveedores_independientes_nombre=serviceProvider.objects.filter(name=dato)
        arreglo_proveedores_independientes_apellido=(serviceProvider.objects.filter(last_name=dato))
        arreglo_proveedores_empresas_nombre=company.objects.filter(company_name=dato)
        arreglo_proveedores_empresas_descripcion=(company.objects.filter(company_description=dato))
        print(arreglo_proveedores_independientes_nombre)
        print(arreglo_proveedores_independientes_apellido)
        print(arreglo_proveedores_empresas_nombre)
        print(arreglo_proveedores_empresas_descripcion)
        arreglo_a_enviar=ListaProveedoresPalabra(arreglo_proveedores_independientes_nombre,arreglo_proveedores_independientes_apellido,arreglo_proveedores_empresas_nombre,arreglo_proveedores_empresas_descripcion)
        if len(arreglo_a_enviar)== 0:
            return HttpResponse("bad")
        else:
            return JsonResponse(arreglo_a_enviar, safe=False)
    

            
##########################################################################################################

@csrf_exempt
def pedirOrdenGeneral (request):
    if request.method == 'POST': 
    
        ProveedorEmail=request.POST.get("ProveedorEmail")
        clienteEmail=request.POST.get("clienteEmail")
        tipoProveedor=request.POST.get("tipoProveedor")
        itemProveedor=request.POST.get("itemProveedor")
        clienteLat=request.POST.get("clienteLat")
        clienteLong=request.POST.get("clienteLong")
        tituloPedido=request.POST.get("tituloPedido")
        diaPedido=request.POST.get("diaPedido")
        horaPedido=request.POST.get("horaPedido")
        descripcion_problema=request.POST.get("descripcion_problema")
        direccion_pedido=request.POST.get("direccion")
        
        if tipoProveedor=="Proveedor de servicio independiente":
            serviceProvider_=serviceProvider.objects.filter(email=ProveedorEmail)
            client_=client.objects.filter(email=clienteEmail)
            print("ha llegado aquí")
            print(serviceProvider_)
            print(client_)
            if serviceProvider_ and client_: 
                
                rubro= item.objects.filter(items=itemProveedor, provider=serviceProvider_.first()).first()
                print("el rubro es: "+str(rubro))
                if not rubro:
                    return HttpResponse("bad")
                else:
                    if ordenGeneral.objects.filter(client_email=clienteEmail, proveedor_email=ProveedorEmail).exclude(status="CAN").exclude( status="REX").exclude( status="RED"):
                        return HttpResponse("ya hay una orden")
                    else:
                        new=ordenGeneral()
                        
                        new.status="ENV"
                        new.rubro=rubro
                        new.location_lat= clienteLat
                        new.location_long=clienteLong
                        new.tituloPedido=tituloPedido
                        if diaPedido and diaPedido!=None:
                            new.day=diaPedido
                        else: 
                            new.day=datetime.date(1997, 10, 19)
                        if horaPedido and horaPedido!=None:
                            new.time=horaPedido
                        else: 
                            new.time=datetime.time(0, 0, 0)
                        new.problem_description=descripcion_problema
                        new.direccion=direccion_pedido
                        if request.FILES.get("imagen1"):
                            new.picture1= request.FILES.get("imagen1")
                        if request.FILES.get("imagen2"):
                            new.picture2=request.FILES.get("imagen2")

                        new.client_email=clienteEmail
                        new.proveedor_email=ProveedorEmail
                        ticket_numero=ordenGeneral.objects.count()+ordenEmergencia.objects.count()+1000
                        new.ticket=ticket_numero
                        new.motivo_rechazo=""
                        new.resena=""
                        new.save()
                    
                        try:
                            print("el nombre del cliente es: "+client_.first().name)
                            print("el apellido del cliente es: "+client_.first().last_name)
                            send_proveedor_mail_new_orden(ticket_numero, ProveedorEmail, client_.first().name+" "+client_.first().last_name)
                        except:
                            print("problem found at send proveedor mail new orden")
                        return HttpResponse(ticket_numero) 

            else: 
                print("debe enviar bad")
                return HttpResponse("bad")
        else:
            company_=company.objects.filter(email=ProveedorEmail)
            client_=client.objects.filter(email=clienteEmail)
            if company_ and client_: 
                
                rubro= item.objects.filter(items=itemProveedor, provider=company_.first()).first()
                if not rubro:
                    return HttpResponse("bad")
                else:
                    if ordenGeneral.objects.filter(client_email=clienteEmail, proveedor_email=ProveedorEmail).exclude(status="CAN").exclude( status="REX").exclude( status="RED"):
                        return HttpResponse("ya hay una orden")
                    else: 
                        new=ordenGeneral()
                        new.rubro=rubro
                        new.status="ENV"
                        new.location_lat= clienteLat
                        new.location_long=clienteLong
                        new.tituloPedido=tituloPedido
                        if diaPedido:
                            new.day=diaPedido
                        if horaPedido:
                            new.time=horaPedido
                        new.problem_description=descripcion_problema
                        if request.FILES.get("imagen1"):
                            new.picture1= request.FILES.get("imagen1")
                        if request.FILES.get("imagen2"):
                            new.picture2=request.FILES.get("imagen2")
                        
                        new.client_email=clienteEmail
                        new.proveedor_email=ProveedorEmail
                        ticket_numero=ordenGeneral.objects.count()+ordenEmergencia.objects.count()+1000
                        new.ticket=ticket_numero
                        
                        new.save()

                        try:
                            send_proveedor_mail_new_orden(ticket_numero, ProveedorEmail, client_.name+" "+client_.last_name)
                        except:
                            print("problem found at send proveedor mail new orden")
                        return HttpResponse(ticket_numero) 

            else: 
                return HttpResponse("bad")

def consultarOrdenes(request , tipo,email):
    if tipo=="proveedor": 
        
        ordenesGenerales= ordenGeneral.objects.filter(proveedor_email=email).exclude(status="CAN").exclude( status="REX").exclude( status="RED")
        ordenesEmergencia= ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="CAN").exclude( status="REX").exclude( status="RED")
        array=[]
        print(ordenesGenerales.first())
        if ordenesGenerales:
            for datos in ordenesGenerales:
              cliente=client.objects.filter(email=datos.client_email).first()
              if cliente:
                imagen={}
                if cliente.picture:
                    imagen['imagen_Cliente']="data:image/png;base64,"+base64.b64encode(cliente.picture.read()).decode('ascii')
                else: 
                    imagen['imagen_Cliente']=""
                if datos.picture1: 
                    imagen['picture1']="data:image/png;base64,"+base64.b64encode(datos.picture1.read()).decode('ascii')
                else:
                    imagen['picture1']=""
                if datos.picture2: 
                    imagen['picture2']="data:image/png;base64,"+base64.b64encode(datos.picture2.read()).decode('ascii')
                else:
                    imagen['picture2']=""
                    
                array.append({"tipo":"Orden general","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                "dia":datos.day, "time":datos.time, "titulo":datos.tituloPedido,"descripcion":datos.problem_description,
                "location_lat":datos.location_lat,"location_long":datos.location_long, "email_cliente":cliente.email,
                "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_cliente":imagen['imagen_Cliente'],
                "presupuesto":datos.presupuesto_inicial, "pedidoMasInformacion": datos.pedido_mas_información})


        if ordenesEmergencia: 
            for datos in ordenesGenerales:
                cliente=client.objects.filter(email=datos.client_email).first()
                imagen={}
                if cliente.picture:
                    imagen['imagen_Cliente']="data:image/png;base64,"+base64.b64encode(cliente.picture.read()).decode('ascii')
                else: 
                    imagen['imagen_Cliente']=""
                if datos.picture1: 
                    imagen['picture1']="data:image/png;base64,"+base64.b64encode(datos.picture1.read()).decode('ascii')
                else:
                    imagen['picture1']=""
                if datos.picture2: 
                    imagen['picture2']="data:image/png;base64,"+base64.b64encode(datos.picture2.read()).decode('ascii')
                else:
                    imagen['picture2']=""
                    
                array.append({"tipo":"Orden de emergencia","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                "dia":datos.day, "time":datos.time, "titulo":datos.tituloPedido,"descripcion":datos.problem_description,
                "location_lat":datos.location_lat,"location_long":datos.location_long,"email_cliente":cliente.email,
                "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_cliente":imagen['imagen_Cliente'] })
        
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")
    elif tipo=="cliente":
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="CAN").exclude( status="REX").exclude( status="RED")
        ordenesEmergencia= ordenEmergencia.objects.filter(client_email=email).exclude(status="CAN").exclude( status="REX").exclude( status="RED")
        array=[]
        print("lets see")
        print(ordenesGenerales)
        print(ordenesEmergencia)
        if ordenesGenerales:
            for datos in ordenesGenerales:
              proveedor=serviceProvider.objects.filter(email=datos.proveedor_email).first()
              if not proveedor:
                  proveedor=company.objects.filter(email=datos.proveedor_email).first()
              if proveedor:
                print("ENTONCES DEBE LLEGAR AQUI")
                imagen={}
                if proveedor.picture:
                    imagen['imagen_proveedor']="data:image/png;base64,"+base64.b64encode(proveedor.picture.read()).decode('ascii')
                else: 
                    imagen['imagen_proveedor']=""
                if datos.picture1: 
                    imagen['picture1']="data:image/png;base64,"+base64.b64encode(datos.picture1.read()).decode('ascii')
                else:
                    imagen['picture1']=""
                if datos.picture2: 
                    imagen['picture2']="data:image/png;base64,"+base64.b64encode(datos.picture2.read()).decode('ascii')
                else:
                    imagen['picture2']=""
                    
                array.append({"tipo":"Orden general","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                "dia":datos.day, "time":datos.time, "titulo":datos.tituloPedido,"descripcion":datos.problem_description,
                "location_lat":datos.location_lat,"location_long":datos.location_long, "email_proveedor":proveedor.email,
                "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_proveedor":imagen['imagen_proveedor'],
                "presupuesto":datos.presupuesto_inicial, "pedidoMasInformacion": datos.pedido_mas_información })
            if len(array)>0:
                return JsonResponse(array, safe=False)
            else: 
                return HttpResponse("bad")
        if ordenesEmergencia: 
            for datos in ordenesGenerales:
                proveedor=serviceProvider.objects.filter(email=datos.proveedor_email).first()
                if not proveedor:
                    proveedor=company.objects.filter(email=datos.proveedor_email).first()
                if proveedor:
                    imagen={}
                    if proveedor.picture:
                        imagen['imagen_proveedor']="data:image/png;base64,"+base64.b64encode(proveedor.picture.read()).decode('ascii')
                    else: 
                        imagen['imagen_proveedor']=""
                    if datos.picture1: 
                        imagen['picture1']="data:image/png;base64,"+base64.b64encode(datos.picture1.read()).decode('ascii')
                    else:
                        imagen['picture1']=""
                    if datos.picture2: 
                        imagen['picture2']="data:image/png;base64,"+base64.b64encode(datos.picture2.read()).decode('ascii')
                    else:
                        imagen['picture2']=""
                        
                    array.append({"tipo":"Orden de emergencia","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                    "dia":datos.day, "time":datos.time, "titulo":datos.tituloPedido,"descripcion":datos.problem_description,
                    "location_lat":datos.location_lat,"location_long":datos.location_long,"email_cliente":proveedor.email,
                    "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_proveedor":imagen['imagen_proveedor'] })
            
            if len(array)>0:
                return JsonResponse(array, safe=False)
            else: 
                return HttpResponse("bad")
        else:
            return HttpResponse("bad")
    else:
        return HttpResponse("bad") 


def datosCliente(request , n_ticket, tipo_orden):
    if tipo_orden=="Orden general": 
        print("pues ha llegado aqui")
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if ordenesGenerales:
            cliente= client.objects.filter(email=ordenesGenerales.client_email).first()
            if cliente:
                imagen=""
                if cliente.picture:
                    imagen="data:image/png;base64,"+base64.b64encode(cliente.picture.read()).decode('ascii') 
                return JsonResponse( {"nombre":cliente.name,"apellido":cliente.last_name, 
                "imagen":imagen, "calificacion":cliente.qualification}, safe=False)

            else: 
                return HttpResponse("bad") 
        else: 
            return HttpResponse ("bad")
    elif tipo_orden=="Orden de emergencia":
        ordenesEmergencia= ordenEmergencia.objects.filter(ticket=n_ticket)
        if ordenesEmergencia:
            cliente= client.objects.filter(email=ordenesEmergencia.client_email).first()
            if cliente:
                imagen=""
                if cliente.picture:
                    imagen="data:image/png;base64,"+base64.b64encode(cliente.picture.read()).decode('ascii') 
                return JsonResponse( {"nombre":cliente.name,"apellido":cliente.last_name, 
                "imagen":imagen, "calificacion":cliente.qualification}, safe=False)

            else: 
                return HttpResponse("bad") 
        else: 
            return HttpResponse ("bad")
    else: 
        return HttpResponse("bad")


def datosProveedor(request , n_ticket, tipo_orden):
    if tipo_orden=="Orden general": 
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if ordenesGenerales:
            proveedor_independiente= serviceProvider.objects.filter(email=ordenesGenerales.proveedor_email).first()
            if proveedor_independiente:
                imagen=""
                if proveedor_independiente.picture:
                    imagen="data:image/png;base64,"+base64.b64encode(proveedor_independiente.picture.read()).decode('ascii') 
                
                rubro=item.objects.filter(provider=proveedor_independiente).first()
                if rubro:
                    calificacion=rubro.qualification
                else: 
                    calificacion="-"
                return JsonResponse( {"nombre":proveedor_independiente.name,"apellido":proveedor_independiente.last_name, 
                "imagen":imagen, "calificacion":calificacion}, safe=False)
            else:
                compania= company.objects.filter(email=ordenesGenerales.proveedor_email).first()
                if compania:
                    imagen=""
                    if compania.picture:
                        imagen="data:image/png;base64,"+base64.b64encode(compania.picture.read()).decode('ascii') 
                    rubro=item_company.objects.filter(provider=proveedor_independiente).first()
                    if rubro:
                        calificacion=rubro.qualification
                    else: 
                        calificacion="-"
                    return JsonResponse( {"nombre":compania.name,"apellido":compania.last_name, 
                "imagen":imagen, "calificacion":calificacion}, safe=False)
                else: 
                    return HttpResponse("bad") 
        else: 
            return HttpResponse ("bad")

    elif tipo_orden=="Orden de emergencia":
        ordenesEmergencia= ordenEmergencia.objects.filter(ticket=n_ticket)
        if ordenesEmergencia:
            proveedor_independiente= serviceProvider.objects.filter(email=ordenesEmergencia.proveedor_email).first()
            if proveedor_independiente:
                imagen=""
                if proveedor_independiente.picture:
                    imagen="data:image/png;base64,"+base64.b64encode(proveedor_independiente.picture.read()).decode('ascii') 
                return JsonResponse( {"nombre":proveedor_independiente.name,"apellido":proveedor_independiente.last_name, 
                "imagen":imagen, "calificacion":proveedor_independiente.qualification}, safe=False)
            else:
                compania= company.objects.filter(email=ordenesEmergencia.proveedor_email).first()
                if compania:
                    imagen=""
                    if compania.picture:
                        imagen="data:image/png;base64,"+base64.b64encode(compania.picture.read()).decode('ascii') 
                
                    return JsonResponse( {"nombre":compania.name,"apellido":compania.last_name, 
                "imagen":imagen, "calificacion":compania.qualification}, safe=False)
                else: 
                    return HttpResponse("bad") 
        else: 
            return HttpResponse ("bad")
    else: 
        return HttpResponse("bad")


def cambiarEstadoOrden (request , n_ticket, tipo_orden,nuevo_estado_orden):
    if tipo_orden=="Orden general": 
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if ordenesGenerales:
            ordenesGenerales.status=nuevo_estado_orden
            ordenesGenerales.save()
            return HttpResponse("ok")
        else: 
            return HttpResponse("bad")
    elif tipo_orden=="Orden de emergencia":
        ordenesEmergencia= ordenEmergencia.objects.filter(ticket=n_ticket)
        if ordenesEmergencia:
            ordenesEmergencia.status=nuevo_estado_orden
            ordenesEmergencia.save()
            return HttpResponse("ok")
        else: 
            return HttpResponse("bad")
    else: 
            return HttpResponse("bad")

@csrf_exempt
def agregarFotoOrden(request):
    if request.method == 'POST': 
        
        imagen1=""
        imagen2=""
        ticket=request.POST.get("ticket")
        tipo=request.POST.get("tipo")
        if request.FILES.get("imagen1"):
            imagen1= request.FILES.get("imagen1")
        if request.FILES.get("imagen2"):
            imagen2=request.FILES.get("imagen2")
        if tipo=="Orden general":
            orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
            if orden_General: 
                if imagen1!="":
                    orden_General.picture1=imagen1
                if imagen2!="":
                    orden_General.picture2=imagen2
                orden_General.save()
                return HttpResponse("ok")
            else:
                return HttpResponse("bad")
        if tipo=="Orden de emergencia":
            orden_Emergencia= ordenEmergencia.objects.filter(ticket=ticket).first()
            if orden_Emergencia: 
                if imagen1!="":
                    orden_Emergencia.picture1=imagen1
                if imagen2!="":
                    orden_Emergencia.picture2=imagen2
                orden_Emergencia.save()
                return HttpResponse("ok")
            else:
                return HttpResponse("bad")

@csrf_exempt
def masInfoOrdenProveedor (request):
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        tipo_orden=request.POST.get("tipoOrden")
        if tipo_orden=="Orden general":
            orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
            if orden_General:
                orden_General.pedido_mas_información=request.POST.get("masInfo")
                orden_General.status="PRE"
                orden_General.save()
                return HttpResponse("ok")
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")

@csrf_exempt
def masInfoOrdenCliente(request):
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        
        orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
        if orden_General:
            orden_General.respuesta_cliente_pedido_mas_información=request.POST.get("respuesta_informacion")
            orden_General.status="ACE"
            orden_General.picture1_mas_información= request.FILES.get("imagen1")
            orden_General.picture2_mas_información= request.FILES.get("imagen2")
            orden_General.save()
            return HttpResponse("ok")
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")

@csrf_exempt
def presupuestoProveedor(request):
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        tipo_orden=request.POST.get("tipoOrden")
        if tipo_orden=="Orden general":
            orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
            if orden_General:
                orden_General.presupuesto_inicial=request.POST.get("precio")
                orden_General.status="PRE"
                orden_General.save()
                return HttpResponse("ok")
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")    
@csrf_exempt

def presupuestoCliente(request):
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        tipo_orden=request.POST.get("tipoOrden")
        if tipo_orden=="Orden general":
            orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
            if orden_General:
                orden_General.status="ACE"
                orden_General.save()
                return HttpResponse("ok")
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")    
'''
@csrf_exempt
def pedirOrdenEmergencia (request):

    if request.method == 'POST': 
    
        
        clienteEmail=request.POST.get("clienteEmail")
        vieneADomicilio=request.POST.get("vieneADomicilio")
        itemProveedor=request.POST.get("itemProveedor")
        clienteLat=request.POST.get("clienteLat")
        clienteLong=request.POST.get("clienteLong")
        tituloPedido=request.POST.get("tituloPedido")
        descripcion_problema=request.POST.get("descripcion_problema")

        client_=client.objects.filter(email=clienteEmail)
        array=[]
        
        if vieneADomicilio:
            #si vieneADomicilio es igual a true entonces la solicitud es solo a proveedores que van a los lugares de los clientes.
            proveedoresindependientes=item.objects.filter(items=itemProveedor).filter(radius_gt=10).order_by('-publicidad','-qualification')
            proveedorescompanias=item_company.objects.filter(items=itemProveedor).filter(radius_gt=10).order_by('-publicidad','-qualification')
            proveedoresRadio(1,array,proveedoresindependientes,clienteLat,clienteLong,0,30,3)
            proveedoresRadio(2,array,proveedorescompanias,clienteLat,clienteLong,0,30,3)

            proveedorSleccionado=ordenarProveedores(array)

            proveedor= Proveedor ()
            proveedor.proveedor_company=proveedorSleccionado
            proveedor.item=itemProveedor
            proveedor.save()

            new=ordenEmergencia()
                
            new.status=order.ENV
            new.location_lat= clienteLat
            new.location_long=clienteLong
            new.tituloPedido=tituloPedido
            new.problem_description=descripcion_problema
            if request.FILES.get("imagen1"):
                new.picture1= request.FILES.get("imagen1")
            if request.FILES.get("imagen2"):
                new.picture2=request.FILES.get("imagen2")
            new.save()

            og=order()
            og.client=client_.first()
            og.proveedor=proveedor
                
            ticket_numero=order.objects.count()+1000
            og.ticket=ticket_numero 
            og.orden_general=new
            og.save()

            try:
                send_proveedor_mail_new_orden(ticket_numero, proveedorSleccionado.email, client_.name+" "+client_.last_name)
            except:
                print("problem found at send proveedor mail new orden")
            return JsonResponse(proveedorSleccionado, safe=False)

        else:
            proveedoresindependientes=item.objects.filter(items=itemProveedor).order_by('-publicidad','-qualification')
            proveedorescompanias=item_company.objects.filter(items=itemProveedor).order_by('-publicidad','-qualification')
            proveedoresRadio(1,array,proveedoresindependientes,clienteLat,clienteLong,0,30,3)
            proveedoresRadio(2,array,proveedorescompanias,clienteLat,clienteLong,0,30,3)

            proveedorSleccionado=ordenarProveedores(array)

            proveedor= Proveedor ()
            proveedor.proveedor_company=proveedorSleccionado
            proveedor.item=itemProveedor
            proveedor.save()

            new=ordenEmergencia()
                
            new.status=order.ENV
            new.location_lat= clienteLat
            new.location_long=clienteLong
            new.tituloPedido=tituloPedido
            new.problem_description=descripcion_problema
            if request.FILES.get("imagen1"):
                new.picture1= request.FILES.get("imagen1")
            if request.FILES.get("imagen2"):
                new.picture2=request.FILES.get("imagen2")
            new.save()

            og=order()
            og.client=client_.first()
            og.proveedor=proveedor
                
            ticket_numero=order.objects.count()+1000
            og.ticket=ticket_numero 
            og.orden_general=new
            og.save()
            
            try:
                send_proveedor_mail_new_orden(ticket_numero, proveedorSleccionado.email, client_.name+" "+client_.last_name)
            except:
                print("problem found at send proveedor mail new orden")
            return JsonResponse(proveedorSleccionado, safe=False)
'''
    

