from django.http import HttpResponse
from django.http import JsonResponse
from callserviceapp.models import  chat, nuevo_chat, ordenEmergencia, ordenEmergenciaLista, ordenGeneral, item, user_data, validation_token
from callserviceapp.utils import distanciaEnLaTierra, proveedoresRadio, proveedoresRadioOrdenEmergencia

import random
import base64
from django.views.decorators.csrf import csrf_exempt

from callserviceapp.tasks import send_client_mail_more_info, send_client_order_canceled, send_orden_emergencia, send_proveedor_change_date, send_proveedor_mail_more_info, send_proveedor_mail_new_orden, send_proveedor_on_trip, send_user_mail

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@csrf_exempt
def prueba(request): 
    send_user_mail.delay(2232,"julianov403@gmail.com")
    return HttpResponse("hi")


def login(request, email, password):

    user=User.objects.filter(email=email, password=password).first()
    if user:
        if user.is_active: 
            client_data=user_data.objects.filter(user_id=user).first()
            if client_data.name:
                imagen={}
                if client_data.picture:
                    imagen['img_personal']="data:image/png;base64,"+base64.b64encode(client_data.picture.read()).decode('ascii')
                else:
                    imagen['img_personal']=""
        
                data=[{"personalDataCompleted": "true","user":user.email, "clientType":client_data.client_type, "calificacion":client_data.qualification,"picture":imagen['img_personal']}]
                return JsonResponse(data, safe=False)
            else: 
                data=[{"personalDataCompleted": "false", "user":user.email, "clientType":client_data.client_type}]
                return JsonResponse(data, safe=False)
        else: 
            return HttpResponse("Must verify the email")        
    else:
        return HttpResponse("user or password incorrect")


def homeCliente (request , lat, long):
    array=[]

    proveedores=item.objects.order_by('-publicidad','-qualification')
    proveedoresRadio(1,array,proveedores,lat,long,0,30,10)
        
    if len(array)<=5:
        proveedoresRadio(1,array,proveedores,lat,long,30,150,6)        
        if len(array)==0:
            return HttpResponse("bad")
        else:
            return JsonResponse(array, safe=False)
    else:
        return JsonResponse(array, safe=False)


def proveedorUbicacion (request , email, lat, long):
    user=User.objects.filter(email=email).first()
    if user:
        userData=user_data.objects.filter(user_id=user).first()
        userData.posicion_lat=lat
        userData.posicion_long=long
        userData.save()
        return HttpResponse("ok")
        
    else:
        return HttpResponse("bad")
  


def homeClientePedirDatos (request , email,rubro, tipoPedido,lat, long):
    user=User.objects.filter(email=email).first()
    if user: 
        datosItem=item.objects.filter(user_id=user).filter(items=rubro).first()
        datos_personales=user_data.objects.filter(user_id=user).first()

        if datosItem and datos_personales:
            if (tipoPedido=="caracteres"):        
                distance=distanciaEnLaTierra(float(datos_personales.posicion_long),float(datos_personales.posicion_lat),float(long),float(lat))
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



########################################################################################3
#Registro

@csrf_exempt 
def register (request):
    if request.method == 'POST': 
        
        type=request.POST.get("tipo")
        email=request.POST.get("email")
        password =request.POST.get("password")

        user= User.objects.filter(email=email)
        if not user: 
            user = User(username=(email.split("@"))[0]+(email.split("@"))[1], email=email, password=password, is_active=False)
            user.save()
            randomNumber = random.randint(1, 99999)
            val_token=validation_token(user_id=user, val_token=randomNumber)
            val_token.save()
            send_user_mail.delay(randomNumber, email)
            userData=user_data (user_id=user,client_type=type)
            userData.save()
            return HttpResponse("email send")
        else:
            return HttpResponse("User alredy taken")
      

@csrf_exempt
def validacionEmail (request):
    if request.method == 'POST': 
        codigo=request.POST.get("codigo")
        email=request.POST.get("email")
        user=User.objects.filter(email=email).first()
        if user: 
            val_token=validation_token.objects.filter(user_id=user).first()
            if val_token: 
                if val_token.val_token == int(codigo): 
                    user.is_active=True
                    user.save()
                    return HttpResponse("email confirmed")
                else: 
                    return  HttpResponse("bad")
        else: 
            return HttpResponse("bad")


def askPersonalInfo(request,type,email):
    user=User.objects.filter(email=email).first()
    if user:
        userData=user_data.objects.filter(user_id=user).first()
        if userData: 
            if userData.name==None:
                return HttpResponse("no ha cargado información personal")
            else:
                imagen={}
                if userData.picture:
                    imagen['client_picture']= "data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii')
                else:
                    imagen['client_picture']=""
                data = [{"name": userData.name, "last_name": userData.last_name,
                "qualification": userData.qualification,},
                
                {"client_picture": imagen['client_picture']}]

                return JsonResponse(data, safe=False)
    else:
        return HttpResponse("usuario no registrado") 


@csrf_exempt 
def nuevaInfoPersonal (request): 
    if request.method == 'POST':
        user=User.objects.filter(email=request.POST.get("email")).first()
        
        if user:
            print("--------------------------")
            print(user)
            print("----------------------------")
            userData=user_data.objects.filter(user_id=user).first()
            if userData: 
                if request.POST.get("nombre")!= None:
                    userData.name=request.POST.get("nombre")
                if request.POST.get("apellido")!= None:
                    userData.last_name=request.POST.get("apellido")
                if request.FILES.get("image")!= None:
                    userData.picture= request.FILES.get("image")
                userData.save() 
                return HttpResponse("ok")
            else:
                return HttpResponse("bad")
        else: 
            return HttpResponse("bad")


@csrf_exempt 
def completeInfo (request): 
    if request.method == 'POST':

        user=User.objects.filter(email=request.POST.get("email")).first() 
        print("--------------------------")
        print(user)
        print("----------------------------")
        if user: 
            userData =user_data.objects.filter(user_id=user).first()
            if userData:
                userData.name=request.POST.get("nombre")
                userData.last_name=request.POST.get("apellido") 
                userData.picture= request.FILES.get("image") 
                userData.qualification=0
                userData.save()
                return HttpResponse("todo ok")
            else:
                return HttpResponse("bad")
        else: 
            return HttpResponse("no usuario registrado")

      
###############################################
#RUBROS

@csrf_exempt 
def addRubro (request):
    if request.method == 'POST':

        user=User.objects.filter(email=request.POST.get("email")).first()
        if user:
            rubros=item.objects.filter(user_id=user)
            if len(rubros)<2:
                posicion_global=(request.POST.get("posicion").split("/"))
                new = item()
                new.items=request.POST.get("item")
                new.user_id=user
                if request.POST.get("ordenEmergencia")=="no":
                    new.hace_orden_emergencia=False
                else: 
                    new.hace_orden_emergencia=True
                new.radius=request.POST.get("radius")
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
                return HttpResponse("rubro cargado")
            else:
                return HttpResponse("ha cargado la cantidad maxima de items")


@csrf_exempt 
def completeInfoRubros (request,modo,tipo,email):
    if modo=="pedir":
        user=User.objects.filter(email=email).first()
        if user:
            rubros=item.objects.filter(user_id=user) 
            if not rubros:
                return HttpResponse ("No hay rubros cargados")
            else:                    
                x=[]
                for i in range(0, len(rubros)):
                    x.append(rubros[i].items+"-")
                return HttpResponse(x)
        return HttpResponse("No usuario registrado")


def requestRubros(request, tipo,email,rubro):
    user=User.objects.filter(email=email).first()
    if user: 
        rubro=item.objects.filter(user_id=user).filter(items=rubro).first()
        if rubro:
            datos=rubro
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

            data = {"rubro": datos.items, "radius": str(datos.radius),
                "description":datos.description,"hace_orden_emergencia":"no",
                "qualification":str(datos.qualification),
                "pais":datos.pais, "provincia":datos.provincia, "ciudad":datos.ciudad,
                "calle":datos.domicilio_calle, "numeracion":datos.domicilio_numeracion,
                "days_of_works": datos.days_of_works,"hour_init": str(datos.hour_init),
                "hour_end": str(datos.hour_end),"certificate":images['certificado'],
                "picture1":images['imagen1'],"picture2": images['imagen2'],"picture3": images['imagen3'] }
                
            return JsonResponse(data, safe=False)
                #return HttpResponse(data)
        else:
            return HttpResponse ("incongruencia de datos")
        

@csrf_exempt 
def deleteRubro (request):
    if request.method == 'POST':
        user=User.objects.filter(email=request.POST.get("email")).first()
        if user:
            rubro=item.objects.filter(user_id=user).filter(items=request.POST.get("item")).first() 
            if rubro:
                rubro.delete()
                return HttpResponse("rubro elimnado")
            else:
                return HttpResponse("no ha sido posible eliminar el rubro")
        else:
            return HttpResponse("no ha sido posible eliminar el rubro") 



@csrf_exempt 
def modificarRubro (request):
    if request.method == 'POST':
        user=User.objects.filter(email=request.POST.get("email")).first()
        if user:
            rubro=item.objects.filter(user_id=user).filter(items=request.POST.get("item")).first()
            if rubro:
                calificacion=rubro.qualification
                rubro.delete()

                new = item()
                new.items=request.POST.get("item") 
                new.user_id=user

                new.radius=request.POST.get("radius")

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


def restarPassword(request, email):
    user=User.objects.filter(email=email).first() 
    if user:
        randomNumber = random.randint(1, 99999)
        val_token=validation_token(user_id=user, val_token=randomNumber)
        val_token.save()
        send_user_mail.delay(randomNumber, email)
        return HttpResponse(randomNumber)

    else:
        return HttpResponse("usuario y email no registrado")         

def setNewPassword (request, email, codigo,password):
    user=User.objects.filter(email=email).first() 
    if user:
        valToken=validation_token.objects.filter(user_id=user).first()
        if codigo==valToken.val_token:
            user.password=password
            user.save()
            return HttpResponse("Contraseña cambiada correctamente")
        else:
            return HttpResponse("Bad code") 
    else:
        return HttpResponse("usuario y email no registrado")


def buscar (request,tipo, dato):
    
    if tipo=="categoria":
        categoria_a_buscar=dato
        categoria_buscada=item.objects.filter(items=categoria_a_buscar).order_by('-qualification')
        if categoria_buscada:
            i=0
            array=[]
            for datos in categoria_buscada:
                
                personales=datos.user_id
                userData=user_data.objects.filter(user_id=personales).first()
                imagenes={}
                tipo_proveedor=""
                    
                if userData.picture:
                    imagenes['picture']= "data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii')
                else: 
                    imagenes['picture']=""
                if userData.client_type==2:
                    tipo_proveedor="Proveedor de servicio independiente"
                else:
                    tipo_proveedor="Empresa proveedora de servicios"

                first={"item":datos.items,"imagen":imagenes['picture'] ,
                    "calificacion":datos.qualification,
                    "nombre":userData.name, "apellido":userData.last_name, "email":"", "tipo":tipo_proveedor }

                array.append(first)
                i=i+1
                if i==30: 
                    break
            if len(array)== 0:
                return HttpResponse("bad")
            else:
                return JsonResponse(array, safe=False) 
        else:
            return HttpResponse("bad")


    if tipo=="palabras":
        arreglo_proveedores_nombre=user_data.objects.filter(name=dato)
        arreglo_proveedores_apellido=user_data.objects.filter(last_name=dato)
        array=[]
        if arreglo_proveedores_nombre: 
            for datos in arreglo_proveedores_nombre:
                imagenes={}
                if datos.picture:
                    imagenes['picture']= "data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
                else: 
                    imagenes['picture']=""
                if datos.client_type==2:
                    tipo_proveedor="Proveedor de servicio independiente"
                else:
                    tipo_proveedor="Empresa proveedora de servicios"

                rubro=item.objects.filter(user_id=datos.user_id).first()

                first={"item":rubro,"imagen":imagenes['picture'] ,
                    "calificacion":datos.qualification,
                    "nombre":datos.name, "apellido":datos.last_name, "email":"", "tipo":tipo_proveedor }
                array.append(first)
        
        if arreglo_proveedores_apellido and len(array)<30: 
            for datos in arreglo_proveedores_apellido:
                imagenes={}
                if datos.picture:
                    imagenes['picture']= "data:image/png;base64,"+base64.b64encode(datos.picture.read()).decode('ascii')
                else: 
                    imagenes['picture']=""
                if datos.client_type==2:
                    tipo_proveedor="Proveedor de servicio independiente"
                else:
                    tipo_proveedor="Empresa proveedora de servicios"

                rubro=item.objects.filter(user_id=datos.user_id).first()

                first={"item":rubro,"imagen":imagenes['picture'] ,
                    "calificacion":datos.qualification,
                    "nombre":datos.name, "apellido":datos.last_name, "email":"", "tipo":tipo_proveedor }
                array.append(first)
        if len(array)== 0:
            return HttpResponse("bad")
        else:
            return JsonResponse(array, safe=False) 

    

            
##########################################################################################################

def verReseñas (request , email, cantida, tipo):
    cantidad=int(cantida)
    if(email!="" and email!=None):
        if tipo=="cliente":
            ordenesGenerales=ordenGeneral.objects.filter(client_email=email)
            ordenesEmergencias=ordenEmergencia.objects.filter(client_email=email)
            if ordenesGenerales: 
                aux=cantidad
                array=[]
                for data in ordenesGenerales:
                    if aux < (cantidad+7):
                        valores={"calificación":data.calificacion_cliente, "resena":data.resena_al_cliente }
                        array.append(valores)
                        aux=aux+1
                    else: 
                        break
                if aux < (cantidad+7):
                    if ordenesEmergencias:
                        for data in ordenesEmergencias:
                            if aux < (cantidad+7):
                                valores={"calificación":data.calificacion_cliente, "resena":data.resena_al_cliente }
                                array.append(valores)
                                aux=aux+1
                            else: 
                                break
                if len(array)>0:
                    return JsonResponse(array, safe=False)
            elif ordenesEmergencias: 
                aux=cantidad
                array=[]
                for data in ordenesEmergencias:
                            if aux < (cantidad+7):
                                valores={"calificación":data.calificacion_cliente, "resena":data.resena_al_cliente }
                                array.append(valores)
                                aux=aux+1
                            else: 
                                break
            
                if len(array)>0:
                    return JsonResponse(array, safe=False)
            else: 
                return HttpResponse("bad")
        elif tipo=="Proveedor de servicio independiente":
            ordenesGenerales=ordenGeneral.objects.filter(proveedor_email=email)
            ordenesEmergencias=ordenEmergencia.objects.filter(proveedor_email=email)
            if ordenesGenerales: 
                aux=cantidad
                array=[]
                for data in ordenesGenerales:
                    if aux < (cantidad+7):
                        valores={"calificación":data.calificacion_proveedor, "resena":data.resena_al_proveedor }
                        array.append(valores)
                        aux=aux+1
                    else: 
                        break
                if aux < (cantidad+7):
                    if ordenesEmergencias:
                        for data in ordenesEmergencias:
                            if aux < (cantidad+7):
                                valores={"calificación":data.calificacion_proveedor, "resena":data.resena_al_proveedor }
                                array.append(valores)
                                aux=aux+1
                            else: 
                                break
                if len(array)>0:
                    return JsonResponse(array, safe=False)
            elif ordenesEmergencias: 
                aux=cantidad
                array=[]
                for data in ordenesEmergencias:
                            if aux < (cantidad+7):
                                valores={"calificación":data.calificacion_proveedor, "resena":data.resena_al_proveedor }
                                array.append(valores)
                                aux=aux+1
                            else: 
                                break
            
                if len(array)>0:
                    return JsonResponse(array, safe=False)
            else: 
                return HttpResponse("bad")
        else:
            ordenesGenerales=ordenGeneral.objects.filter(proveedor_email=email)
            ordenesEmergencias=ordenEmergencia.objects.filter(proveedor_email=email)
            if ordenesGenerales: 
                aux=cantidad
                array=[]
                for data in ordenesGenerales:
                    if aux < (cantidad+7):
                        valores={"calificación":data.calificacion_proveedor, "reseña":data.resena_al_proveedor }
                        array.append(valores)
                        aux=aux+1
                    else: 
                        break
                if aux < (cantidad+7):
                    if ordenesEmergencias:
                        for data in ordenesEmergencias:
                            if aux < (cantidad+7):
                                valores={"calificación":data.calificacion_proveedor, "reseña":data.resena_al_proveedor }
                                array.append(valores)
                                aux=aux+1
                            else: 
                                break
            
                if len(array)>0:
                    return JsonResponse(array, safe=False)
                else: 
                    return HttpResponse("bad")
            elif ordenesEmergencias: 
                aux=cantidad
                array=[]
                for data in ordenesEmergencias:
                            if aux < (cantidad+7):
                                valores={"calificación":data.calificacion_proveedor, "reseña":data.resena_al_proveedor }
                                array.append(valores)
                                aux=aux+1
                            else: 
                                break
            
                if len(array)>0:
                    return JsonResponse(array, safe=False)
            else: 
                return HttpResponse("bad")
        
    
    else: 
        return HttpResponse("bad")



def datosCliente(request , n_ticket, tipo_orden):

    if tipo_orden=="Orden general": 
        
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if ordenesGenerales:
            user=User.objects.filter(email=ordenesGenerales.client_email).first()
            if user:
                userData=user_data.objects.filter(user_id=user).first()
                if userData:
                    imagen=""
                    if userData.picture:
                        imagen="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii') 
                    
                    return JsonResponse( {"nombre":userData.name,"apellido":userData.last_name, 
                    "imagen":imagen, "calificacion":userData.qualification}, safe=False) 
                else:
                    return HttpResponse("bad")
            else: 
                return HttpResponse("bad") 

    elif tipo_orden=="Orden de emergencia":
        ordenesEmergencia= ordenEmergencia.objects.filter(ticket=n_ticket)
        if ordenesEmergencia:
            user=User.objects.filter(email=ordenesEmergencia.client_email).first()
            if user:
                userData=user_data.objects.filter(user_id=user).first()
                if userData:
                    imagen=""
                    if userData.picture:
                        imagen="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii') 
                    
                    return JsonResponse( {"nombre":userData.name,"apellido":userData.last_name, 
                    "imagen":imagen, "calificacion":userData.qualification}, safe=False) 
                else:
                    return HttpResponse("bad")
            else: 
                return HttpResponse("bad")


def datosProveedor(request , n_ticket, tipo_orden, rubro):
    if tipo_orden=="Orden general": 
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if ordenesGenerales:
            user=User.objects.filter(email=ordenesGenerales.proveedor_email).first()
            if user:
                userData=user_data.objects.filter(user_id=user).first()
                if userData:
                    imagen=""
                    if userData.picture:
                        imagen="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii') 
                    
                    return JsonResponse( {"nombre":userData.name,"apellido":userData.last_name, 
                    "imagen":imagen, "calificacion":userData.qualification}, safe=False) 
                else:
                    return HttpResponse("bad")
            else: 
                return HttpResponse("bad")
        else: 
            return HttpResponse("bad")

    elif tipo_orden=="Orden de emergencia":
        ordenesEmergencia= ordenEmergencia.objects.filter(ticket=n_ticket).first()
        if ordenesEmergencia:
            user=User.objects.filter(email=ordenesEmergencia.proveedor_email).first()
            if user:
                userData=user_data.objects.filter(user_id=user).first()
                if userData:
                    imagen=""
                    if userData.picture:
                        imagen="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii') 
                    
                    return JsonResponse( {"nombre":userData.name,"apellido":userData.last_name, 
                    "imagen":imagen, "calificacion":userData.qualification}, safe=False) 
                else:
                    return HttpResponse("bad")
            else: 
                return HttpResponse("bad")
        else: 
            return HttpResponse("bad")


###########################################################################################
#ORDEN GENERAL 


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

        user_proveedor=User.objects.filter(email=ProveedorEmail).first()
        
        rubro= item.objects.filter(items=itemProveedor, user_id=user_proveedor).first()
        
        if rubro:
            if ordenGeneral.objects.filter(client_email=clienteEmail, proveedor_email=ProveedorEmail).exclude(status="CAN").exclude( status="REX").exclude( status="RED").first():
                if ordenGeneral.objects.filter(client_email=clienteEmail, proveedor_email=ProveedorEmail).exclude(status="CAN").exclude( status="REX").exclude( status="RED").first().rubro.items==itemProveedor:
                            
                    return HttpResponse("ya hay una orden")
                else:
                    new=ordenGeneral()
                    new.status="ENV"
                    new.rubro=rubro
                    new.tituloPedido=tituloPedido
                    new.day=""
                    new.time=""
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
                    new.resena_al_proveedor=""
                    new.resena_al_cliente=""
                    new.location_lat=clienteLat
                    new.location_long=clienteLong
                    new.save()

                    user_client=User.objects.filter(email=clienteEmail).first()
                    userData=user_data.objects.filter(user_id=user_client).first()
                   
                        
                    send_proveedor_mail_new_orden.delay(ticket_numero, ProveedorEmail, userData.name+" "+userData.last_name)
                           
                    return HttpResponse(ticket_numero)
            else:
                new=ordenGeneral()
                new.status="ENV"
                new.rubro=rubro
                new.tituloPedido=tituloPedido
                new.day=""
                new.time=""
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
                new.resena_al_proveedor=""
                new.resena_al_cliente=""
                new.location_lat=clienteLat
                new.location_long=clienteLong
                new.save()

                user_client=User.objects.filter(email=clienteEmail).first()
                userData=user_data.objects.filter(user_id=user_client).first()
               
                        
                send_proveedor_mail_new_orden.delay(ticket_numero, ProveedorEmail, userData.name+" "+userData.last_name)
                           
                return HttpResponse(ticket_numero)

        else:
            return HttpResponse("bad")


def consultarOrdenes(request, tipo,email):
    if tipo=="proveedor": 
        ordenesGenerales= ordenGeneral.objects.filter(proveedor_email=email).exclude(status="CAN").exclude( status="REX").exclude( califico_el_proveedor=True)
        ordenesEmergencia= ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="ENV").exclude(status="CAN").exclude( status="REX")                                                             
        EmergenciaLista=ordenEmergenciaLista.objects.filter(proveedor_email=email).exclude(status="OA")
            
        
        array=[]
        if ordenesGenerales:
            for datos in ordenesGenerales:
              user=User.objects.filter(email=datos.client_email).first()
              userData=user_data.objects.filter(user_id=user).first() 
              if userData:
                imagen={}
                if userData.picture:
                    imagen['imagen_Cliente']="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii')
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
                if datos.picture1_mas_información: 
                    imagen['picture1_mas_información']="data:image/png;base64,"+base64.b64encode(datos.picture1_mas_información.read()).decode('ascii')
                else:
                    imagen['picture1_mas_información']=""
                if datos.picture2_mas_información: 
                    imagen['picture2_mas_información']="data:image/png;base64,"+base64.b64encode(datos.picture2_mas_información.read()).decode('ascii')
                else:
                    imagen['picture2_mas_información']=""
                    
                array.append({"rubro":datos.rubro.items,"tipo":"Orden general","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                "dia":datos.day, "time":datos.time, "titulo":datos.tituloPedido,"descripcion":datos.problem_description,
                "location_lat":datos.location_lat,"location_long":datos.location_long, "email_cliente":user.email,
                "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_cliente":imagen['imagen_Cliente'],
                "presupuesto":datos.presupuesto_inicial, "pedidoMasInformacion": datos.pedido_mas_información,
                "respuesta_cliente_pedido_mas_información":datos.respuesta_cliente_pedido_mas_información,
                "picture1_mas_información": imagen['picture1_mas_información'],
                "picture2_mas_información": imagen['picture2_mas_información']})


        if ordenesEmergencia: 
            for datos in ordenesEmergencia:
                user=User.objects.filter(email=datos.client_email).first()
                userData=user_data.objects.filter(user_id=user).first() 
                imagen={}
                if userData.picture:
                    imagen['imagen_Cliente']="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii')
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
                    
                array.append({"rubro":datos.rubro,"tipo":"ORDEN DE EMERGENCIA","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                "descripcion":datos.problem_description,
                "location_lat":datos.location_cliente_lat,"location_long":datos.location_cliente_long,"email_cliente":user.email,
                "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_cliente":imagen['imagen_Cliente'] })

        if EmergenciaLista:
            for datos in EmergenciaLista:
                array.append({"rubro":datos.rubro,"tipo":"Orden de emergencia","status":datos.status, "ticket":datos.ticket})

        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")
            
    elif tipo=="cliente":
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="CAN").exclude( status="REX").exclude(califico_el_cliente=True)
        ordenesEmergencia= ordenEmergencia.objects.filter(client_email=email).exclude(status="CAN").exclude( status="REX").exclude(califico_el_cliente=True)
        
        array=[]
       
        if ordenesGenerales:
            for datos in ordenesGenerales:
                user=User.objects.filter(email=datos.proveedor_email).first()
                userData=user_data.objects.filter(user_id=user).first() 
                if userData:
                    imagen={}
                    if userData.picture:
                        imagen['imagen_proveedor']="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii')
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
                    if datos.picture1_mas_información: 
                        imagen['picture1_mas_información']="data:image/png;base64,"+base64.b64encode(datos.picture1_mas_información.read()).decode('ascii')
                    else:
                        imagen['picture1_mas_información']=""
                    if datos.picture2_mas_información: 
                        imagen['picture2_mas_información']="data:image/png;base64,"+base64.b64encode(datos.picture2_mas_información.read()).decode('ascii')
                    else:
                        imagen['picture2_mas_información']=""

                    array.append({"rubro":datos.rubro.items,"tipo":"Orden general","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                    "dia":datos.day, "time":datos.time, "titulo":datos.tituloPedido,"descripcion":datos.problem_description,
                    "location_lat":datos.location_lat,"location_long":datos.location_long, "email_proveedor":user.email,
                    "presupuesto":str(datos.presupuesto_inicial), "pedidoMasInformacion": datos.pedido_mas_información,
                    "respuesta_cliente_pedido_mas_información":datos.respuesta_cliente_pedido_mas_información,
                    "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_proveedor":imagen['imagen_proveedor'],
                    "picture1_mas_información": imagen['picture1_mas_información'],
                    "picture2_mas_información": imagen['picture2_mas_información'] }) 
            
        if ordenesEmergencia: 
            for datos in ordenesEmergencia:
                user=User.objects.filter(email=datos.proveedor_email).first()
                userData=user_data.objects.filter(user_id=user).first() 
               
                imagen={}
                proveedor_email=""
                if userData:
                    if userData.picture:
                        imagen['imagen_proveedor']="data:image/png;base64,"+base64.b64encode(userData.picture.read()).decode('ascii')
                    proveedor_email=user.email
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
                        
                array.append({"rubro":datos.rubro,"tipo":"Orden de emergencia","status":datos.status, "fecha_creacion":datos.fecha_creacion , "ticket":datos.ticket,
                "problem_description":datos.problem_description,
                "location_cliente_lat":datos.location_cliente_lat,"location_cliente_long":datos.location_cliente_long,"email_proveedor":proveedor_email,
                "picture1":imagen['picture1'], "picture2":imagen['picture2'], "imagen_proveedor":imagen['imagen_proveedor'] })
            

        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")   
        
    else:
        return HttpResponse("bad") 


def cambiarEstadoOrden (request , n_ticket, tipo_orden,nuevo_estado_orden):
    if tipo_orden=="Orden general": 
        
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if ordenesGenerales:
                                       
            ordenesGenerales.status=nuevo_estado_orden
            ordenesGenerales.save()

            if nuevo_estado_orden == "EVI":
                user=User.objects.filter(email=ordenesGenerales.proveedor_email).first()
                userData=user_data.objects.filter(user_id=user).first()
                if userData:
                    send_proveedor_on_trip.delay(n_ticket,userData.name+" "+userData.last_name,ordenesGenerales.rubro,ordenesGenerales.client_email)
                    return HttpResponse("ok")
                
                else:
                    return HttpResponse("bad")  
            else: 
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


def cancelarOrdenGeneral (request , n_ticket, tipo_orden,nuevo_estado_orden,motivo):
    if tipo_orden=="Orden general": 
        ordenesGenerales= ordenGeneral.objects.filter(ticket=n_ticket).first()
        if nuevo_estado_orden=="CAN":

            email_cliente=ordenesGenerales.client_email
            user=User.objects.filter(email=email_cliente).first()
            userData=user_data.objects.filter(user_id=user).first()
            userData.cantidad_ordenes_canceladas=userData.cantidad_ordenes_canceladas+1
            userData.save()
            ordenesGenerales.status=nuevo_estado_orden
            ordenesGenerales.motivo_rechazo=motivo
            ordenesGenerales.save()
            
            send_client_order_canceled.delay(n_ticket,ordenesGenerales.rubro,motivo,ordenesGenerales.proveedor_email, userData.name+" "+userData.last_name)
            return HttpResponse("ok")
        else:
            email_proveedor=ordenesGenerales.proveedor_email
            user=User.objects.filter(email=email_proveedor).first()
            userData=user_data.objects.filter(user_id=user).first()
            if userData:
                userData.cantidad_ordenes_rechazadas=userData.cantidad_ordenes_rechazadas+1 
                userData.save()
                ordenesGenerales.status=nuevo_estado_orden
                ordenesGenerales.motivo_rechazo=motivo
                ordenesGenerales.save()
                return HttpResponse("ok")
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
                orden_General.status="PEI"
                orden_General.save()

                send_proveedor_mail_more_info.delay(ticket, request.POST.get("masInfo"),orden_General.client_email)

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
            orden_General.status="RES"
            orden_General.picture1_mas_información= request.FILES.get("imagen1")
            orden_General.picture2_mas_información= request.FILES.get("imagen2")
            orden_General.save()
            send_client_mail_more_info.delay(ticket, orden_General.pedido_mas_información, request.POST.get("respuesta_informacion"), orden_General.client_email)
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
                orden_General.day=request.POST.get("dia")
                orden_General.time=request.POST.get("hora")
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
        orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
        if orden_General:
            orden_General.status="ACE"
            orden_General.save()
            return HttpResponse("ok")
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")    


@csrf_exempt
def cambiarfechaordengeneral (request): 
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
        if orden_General:
            orden_General.day=request.POST.get("dia")
            orden_General.time=request.POST.get("hora")
            orden_General.save()
            send_proveedor_change_date.delay(ticket,request.POST.get("dia"), request.POST.get("hora"),orden_General.client_email )
            return HttpResponse("ok")
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad") 


@csrf_exempt
def finalizarOrdenProveedor(request):
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        calificacion = request.POST.get("calificacion")
        resena = request.POST.get("resena")
        orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
        if orden_General:
            email=orden_General.client_email
            user=User.objects.filter(email=email).first()
            userData=user_data.objects.filter(user_id=user).first()
            if userData:
                calificacion_inicial= userData.qualification
                userData.qualification=calificacion_inicial + (int(calificacion)/( (userData.cantidad_ordenes_realizadas + userData.cantidad_ordenes_canceladas)+1))
                userData.cantidad_ordenes_realizadas=userData.cantidad_ordenes_realizadas+1
                userData.save()
                if resena!="":
                    orden_General.resena_al_cliente=resena
                orden_General.calificacion_cliente=calificacion #la calificación en la orden no es igual a la calificación del cliente
                orden_General.status="RED"
                orden_General.califico_el_proveedor=True
                orden_General.save()

                return HttpResponse("ok")
            else: 
                return HttpResponse("bad")
        
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad") 


@csrf_exempt
def finalizarOrdenCliente(request):
    if request.method == 'POST':
        ticket=request.POST.get("ticket")
        calificacion = request.POST.get("calificacion")
        resena = request.POST.get("resena")
        orden_General= ordenGeneral.objects.filter(ticket=ticket).first()
        if orden_General:
            email=orden_General.proveedor_email
            user=User.objects.filter(email=email).first()
            userData=user_data.objects.filter(user_id=user).first()
            if userData:
                calificacion_inicial= userData.qualification
                userData.qualification=calificacion_inicial + (int(calificacion)/( (userData.cantidad_ordenes_realizadas + userData.cantidad_ordenes_canceladas)+1))
                userData.cantidad_ordenes_realizadas=userData.cantidad_ordenes_realizadas+1
                userData.save()
                #orden_General.rubro.save()
                if resena!="":
                    orden_General.resena_al_proveedor=resena
                orden_General.calificacion_proveedor = calificacion #la calificación en la orden no es igual a la calificación del cliente
                orden_General.status="RED"
                orden_General.califico_el_cliente=True
                orden_General.save()
                return HttpResponse("ok")

            else: 
                return HttpResponse("bad")
        
        else:
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad") 

def consultarTodasLasOrdenes (request, tipo, email):
    if (tipo=="cliente"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="RED").exclude(status="CAN").exclude(status="REX")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(client_email=email).exclude(status="RED").exclude(status="CAN").exclude(status="REX")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(client_email=email).exclude(status="ENV").exclude(status="REC").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")


def consultarTodasLasOrdenesCanceladas(request, tipo, email): 
    if(tipo=="cliente"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="RED").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(client_email=email).exclude(status="RED").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")
    elif (tipo=="proveedor"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(proveedor_email=email).exclude(status="RED").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="RED").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")

def consultarTodasLasOrdenesCurso(request, tipo, email):
    if(tipo=="cliente"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="RED").exclude(status="CAN").exclude(status="REX")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(client_email=email).exclude(status="RED").exclude(status="CAN").exclude(status="REX")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")
    elif (tipo=="proveedor"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(proveedor_email=email).exclude(status="RED").exclude(status="CAN").exclude(status="REX")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="RED").exclude(status="CAN").exclude(status="REX")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")

def consultarTodasLasOrdenesFinalizadas(request, tipo, email):
    if(tipo=="cliente"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(client_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(client_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")
    elif (tipo=="proveedor"):
        array= []
        ordenesGenerales= ordenGeneral.objects.filter(proveedor_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesGenerales:
            for data in ordenesGenerales:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        ordenesEmergencia = ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="ENV").exclude(status="REC").exclude(status="ABI").exclude(status="PEI").exclude(status="PRE").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
        if ordenesEmergencia:
            for data in ordenesEmergencia:
                if data.rubro:
                    array.append({"rubro":data.rubro.items,"status":data.status,"fecha":data.fecha_creacion, "ticket":data.ticket})
        if len(array)>0:
            return JsonResponse(array, safe=False)
        else: 
            return HttpResponse("bad")



def consultarOrdenParticular (request, ticket):
    ordenesGeneral= ordenGeneral.objects.filter(ticket=ticket).first()
    if ordenesGeneral:
        nombre=""
        user=User.objects.filter(email=ordenesGeneral.proveedor_email).first()
        proveedor=user_data.objects.filter(user_id=user).first()
        if proveedor: 
            nombre=proveedor.name +" "+ proveedor.last_name
            data={"tipo":"Orden general","status":ordenesGeneral.status, "fecha_creacion":ordenesGeneral.fecha_creacion , "ticket":ordenesGeneral.ticket,
                    "dia":ordenesGeneral.day, "time":ordenesGeneral.time, "titulo":ordenesGeneral.tituloPedido,"descripcion":ordenesGeneral.problem_description,
                    "proveedor_nombre":nombre, "reseña_al_proveedor": ordenesGeneral.resena_al_proveedor,
                    "presupuesto":ordenesGeneral.presupuesto_inicial, "pedidoMasInformacion": ordenesGeneral.pedido_mas_información,
                    "respuesta_cliente_pedido_mas_información":ordenesGeneral.respuesta_cliente_pedido_mas_información,
                    }
            return JsonResponse(data, safe=False)
        else:
            return HttpResponse("bad") 
    else:
        ordenEmergency=ordenEmergencia.objects.filter(ticket=ticket).first()
        if ordenEmergency:
                                            
            data={"tipo":"Orden de emergencia","status":ordenEmergency.status, "fecha_creacion":ordenEmergency.fecha_creacion , "ticket":ordenEmergency.ticket,
                "dia":ordenEmergency.day, "time":ordenEmergency.time, "titulo":ordenEmergency.tituloPedido,"descripcion":ordenEmergency.problem_description,
                
                 }
            return JsonResponse(data,safe=False )

        else: 
            return HttpResponse("bad") 


#####################################################################################3
#CHAT

def chatMensaje (request, email,ticket,mensaje,dia,hora):
    if (ticket>=str(1000)):
        chating=chat()
        chating.user=email
        chating.ticket=ticket
        chating.mensaje=mensaje
        chating.day=dia
        chating.time=hora
        chating.save()
        nuevo=nuevo_chat.objects.filter(ticket=ticket).first()
        if nuevo:
            None 
        else: 
            nuevo_mensaje=nuevo_chat()
            mensajeDe=""
            ordenG=ordenGeneral.objects.filter(ticket=ticket).first()
            if ordenG:
                if ordenG.client_email==email:
                    mensajeDe=ordenG.proveedor_email
                else: 
                    mensajeDe=ordenG.client_email
            else: 
                ordenE=ordenEmergencia.objects.filter(ticket=ticket).first()
                if ordenE.client_email==email:
                    mensajeDe=ordenE.proveedor_email
                else: 
                    mensajeDe=ordenE.client_email

            nuevo_mensaje.notify_to=mensajeDe
            nuevo_mensaje.message_from=email
            nuevo_mensaje.ticket=ticket
            nuevo_mensaje.save()
            
    return HttpResponse("ok")

def chatVer (request, ticket,email):
    array=[]
    datosChat = chat.objects.filter(ticket=ticket).all().order_by('daystamp','timestamp')
    if (datosChat):
        for datos in datosChat:
            data={"user":datos.user,"mensaje":datos.mensaje, "dia":datos.day, "hora":datos.time}
            array.append(data)
        if len(array)>0:
            mensaje_sin_leer=nuevo_chat.objects.filter(ticket=ticket).filter(notify_to=email).first()
            if mensaje_sin_leer:
                mensaje_sin_leer.delete()
            return JsonResponse(array,safe=False)
        else:
            return HttpResponse("bad")
    else:
        return HttpResponse("bad")

def chatSinLeer (request,email):
    
    array=[]
    mensaje_sin_leer=nuevo_chat.objects.filter(notify_to=email)
    if mensaje_sin_leer: 
        for data in mensaje_sin_leer:
            data={"de":data.message_from,"ticket":data.ticket}
            array.append(data)
        if len(array)>0:
            return JsonResponse(array,safe=False)
        else:
            return HttpResponse("bad")
    else:
        return HttpResponse("bad")

################################################################################################
#ORDEN DE EMERGENCIA 

@csrf_exempt
def pedirOrdenEmergencia (request):
    if request.method == 'POST':
        picture1=""
        picture2=""
        clienteEmail=request.POST.get("clienteEmail")
        clienteLat=request.POST.get("clienteLat")
        clienteLong=request.POST.get("clienteLong")
        categoria=request.POST.get("categoria")
        descripcion_problema=request.POST.get("descripcion_problema")
        
        if request.FILES.get("imagen1"):
            picture1= request.FILES.get("imagen1")
        if request.FILES.get("imagen2"):
            picture2=request.FILES.get("imagen2")

        if categoria and clienteEmail and clienteLat and clienteLong and descripcion_problema:
            
            array=[]

            datos_proveedores=item.objects.filter(items=categoria).exclude(radius=0).exclude(hace_orden_emergencia=False).order_by('-publicidad','-qualification')
            proveedoresRadioOrdenEmergencia(1,array,datos_proveedores,clienteLat,clienteLong,0,30,15)
                              
            if len(array)<=3:
                
                proveedoresRadioOrdenEmergencia(1,array,datos_proveedores,clienteLat,clienteLong,30,50,6)        
                
                if len(array)==0:
                    return HttpResponse("bad")
                else:
                    ticket = ordenGeneral.objects.count()+ordenEmergencia.objects.count()+1000
                    new=ordenEmergencia()
                    new.status="ENV"
                    new.rubro= categoria
                    new.client_email =clienteEmail
                    #proveedor_email=models.EmailField(blank=True)
                    #fecha_creacion=models.DateField( auto_now_add=True)
                    new.ticket =  ticket
                    new.location_cliente_lat =  clienteLat
                    new.location_cliente_long = clienteLong 
                    new.problem_description = descripcion_problema
                    new.picture1=picture1
                    new.picture2=picture2
                    new.motivo_rechazo=""
                    new.resena_al_proveedor=""    
                    new.resena_al_cliente=""  
                    new.save()
                
                val=notificarProveedoresOrdenEmergencia(ticket, array, categoria, descripcion_problema)
                if val==1:
                    return HttpResponse(ticket)
                else: 
                    return HttpResponse("bad")
            else: 
                ticket= ordenGeneral.objects.count()+ordenEmergencia.objects.count()+1000
                new=ordenEmergencia()
                new.status="ENV"
                new.rubro= categoria
                new.client_email =clienteEmail
                #proveedor_email=models.EmailField(blank=True)
                #fecha_creacion=models.DateField( auto_now_add=True)
                new.ticket =  ticket
                new.location_cliente_lat =  clienteLat
                new.location_cliente_long = clienteLong 
                new.problem_description = descripcion_problema
                new.picture1=picture1
                new.picture2=picture2
                new.motivo_rechazo=""
                new.resena_al_proveedor=""    
                new.resena_al_cliente=""  
                new.save()
                val=notificarProveedoresOrdenEmergencia(ticket, array, categoria, descripcion_problema)
                if val==1:
                    return HttpResponse(ticket)
                else: 
                    return HttpResponse("bad")
        else:
            return HttpResponse("bad")

        
@csrf_exempt
def notificarProveedoresOrdenEmergencia(ticket, array_proveedores, categoria,descripcion_problema): 
    array=[]
    fallo=False
    
    for proveedor in array_proveedores: 
        new=ordenEmergenciaLista()
        new.ticket=ticket
        new.status="CE"
        new.proveedor_email=proveedor["email"]
        new.rubro=categoria
        
        send_orden_emergencia.delay(ticket, proveedor["email"], categoria,descripcion_problema)
        new.save()
        
    return 1            
     
def proveedorAceptaOrdenEmergencia (request, email, ticket): 
    if email!="" and ticket!="":
        email_proveedor=email
        ticket = ticket
        orden=ordenEmergencia.objects.filter(ticket=ticket).first()
        if orden:
            if orden.status=="ENV": 
                orden.status="ACE"
                orden.proveedor_email=email_proveedor
                orden.save()
                lista = ordenEmergenciaLista.objects.filter(ticket=ticket)
                if lista: 
                    for datos in lista:
                        datos.status="OA"
                        datos.save()
                return HttpResponse("ok")
            else:
                return HttpResponse("taken")
        else: 
            return HttpResponse("bad")


def proveedorEnViajeOrdenEmergencia(request, ticket): 
    ticket = ticket
    orden=ordenEmergencia.objects.filter(ticket=ticket).first()
    if orden: 
        orden.status="EVI"
        orden.save()
        return HttpResponse("ok")
    else: 
        return HttpResponse("bad")

def proveedorEnSitioOrdenEmergencia (request, ticket): 
    ticket = ticket
    orden=ordenEmergencia.objects.filter(ticket=ticket).first()
    if orden: 
        orden.status="ENS"
        orden.save()
        return HttpResponse("ok")
    else: 
        return HttpResponse("bad")

def proveedorOrdenEmergenciaRealizada (request, ticket): 
    ticket = ticket
    orden=ordenEmergencia.objects.filter(ticket=ticket).first()
    if orden: 
        orden.status="RED"
        orden.save()
        orden_lista= ordenEmergenciaLista.objects.filter(ticket=ticket).first()
        orden_lista.delete()
        return HttpResponse("ok")
    else: 
        return HttpResponse("bad")

def proveedorRechazaOrdenEmergencia (request, email, ticket): 
    if email!="" and ticket!="":
        email_proveedor=email
        ticket = ticket
        orden=ordenEmergencia.objects.filter(ticket=ticket).first()
        if orden: 
            orden.status="ENV"
            orden.proveedor_email=""
            orden.save()
            ordenLista=ordenEmergenciaLista.objects.filter(ticket=ticket).filter(proveedor_email=email_proveedor).first()
            ordenLista.delete()
            lista=ordenEmergenciaLista.objects.filter(ticket=ticket)
            cantidad=lista.count()
            if (cantidad)!=0:
                for proveedores in lista:
                    proveedores.status="CE" 
                    proveedores.save()
                    send_orden_emergencia.delay(ticket, proveedores.proveedor_email, orden.rubro,orden.problem_description)
                return HttpResponse("ok")
            else:
                return HttpResponse("ok")
        else:
            return HttpResponse("bad")


def clienteRechazaOrdenEmergencia (request, ticket, motivo_rechazo): 
    if ticket != "":
        ticket = ticket
        motivo_rechazo=motivo_rechazo
        orden=ordenEmergencia.objects.filter(ticket=ticket).first()
        if orden: 
            orden.motivo_rechazo= motivo_rechazo
            orden.status="CAN"
            if orden.picture1: 
                #os.remove(orden.picture1.path)
                orden.picture1=""
            if orden.picture2:
                #os.remove(orden.picture2.path)
                orden.picture2=""
            orden.save()
            #aca elimino la lista
            lista = ordenEmergenciaLista.objects.filter(ticket=ticket)
            for datos in lista:
                datos.delete()
            return HttpResponse("ok")
        else: 
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")


@csrf_exempt
def proveedorOrdenEmergenciaCalificar (request): 
    if request.method == 'POST':
        ticket = request.POST.get("ticket")
        reseña=request.POST.get("resena")
        calificacion=request.POST.get("calificacion")
        orden=ordenEmergencia.objects.filter(ticket=ticket).first()
        if orden: 
            orden.calificacion_cliente= calificacion
            orden.resena_al_cliente=reseña
            orden.califico_el_proveedor=True
            orden.save()
            email=orden.client_email
            user=User.objects.filter(email=email).first()
            cliente=user_data.objects.filter(user_id=user).first()
            if cliente:
                calificacion_inicial= cliente.qualification
                cliente.qualification=calificacion_inicial + (int(calificacion)/( (cliente.cantidad_ordenes_realizadas + cliente.cantidad_ordenes_canceladas)+1))
                cliente.cantidad_ordenes_realizadas=cliente.cantidad_ordenes_realizadas+1
                cliente.save()
            return HttpResponse("ok")
        else: 
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")

@csrf_exempt
def clienteOrdenEmergenciaCalificar (request): 
    if request.method == 'POST':
        ticket = request.POST.get("ticket")
        reseña=request.POST.get("resena")
        calificacion=request.POST.get("calificacion")
        orden=ordenEmergencia.objects.filter(ticket=ticket).first()
        rubro=""
        if orden: 
            orden.calificacion_proveedor= calificacion
            orden.resena_al_proveedor=reseña
            orden.califico_el_cliente=True
            orden.save()
            email=orden.proveedor_email
            user=User.objects.filter(email=email).first()
            proveedor=user_data.objects.filter(user_id=user).first()
            if proveedor:
                rubro=item.objects.filter(email=email).filter(items=orden.rubro).first()
                if rubro:
                    calificacion_inicial= rubro.qualification
                    rubro.qualification=calificacion_inicial + (int(calificacion)/( (proveedor.cantidad_ordenes_realizadas + proveedor.cantidad_ordenes_canceladas)+1))
                    proveedor.cantidad_ordenes_realizadas=proveedor.cantidad_ordenes_realizadas+1
                    proveedor.save()
                    rubro.save()
                    return HttpResponse("ok")
                else:
                    return HttpResponse("bad")
            else:
                return HttpResponse("bad")

        else: 
            return HttpResponse("bad")
    else: 
        return HttpResponse("bad")
    
@csrf_exempt
def checkTodasOrdenesEmergenciaAbiertas (request): 
    if request.method == 'POST':
        email = request.POST.get("email")
        tipo= request.POST.get("tipo")
        if tipo=="cliente":
            orden=ordenEmergencia.objects.filter(client_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="RED")
            if orden:
                array=[]
                for datosOrden in orden:
                    array.append({"rubro":datosOrden.rubro,"tipo":"Orden emergencia","status":datosOrden.status, "ticket":datosOrden.ticket})
                if len(array)>0:
                    return JsonResponse(array,safe=False)  
                else:
                    return HttpResponse("bad")         
            else: 
                return HttpResponse("bad")
        elif tipo=="proveedor":
            orden=ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="RED")
            if orden:
                array=[]
                for datosOrden in orden:
                    array.append({"rubro":datosOrden.rubro,"tipo":"Orden emergencia","status":datosOrden.status, "ticket":datosOrden.ticket})
                if len(array)>0:
                    return JsonResponse(array,safe=False)  
                else:
                    return HttpResponse("bad")         
            else: 
                return HttpResponse("bad")
        else: 
            return HttpResponse("bad")


@csrf_exempt
def checkTodasOrdenesEmergenciaFinalizadas (request): 
    if request.method == 'POST':
        email = request.POST.get("email")
        tipo= request.POST.get("tipo")
        if tipo=="cliente":
            orden=ordenEmergencia.objects.filter(client_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="ENV").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
            if orden:
                array=[]
                for datosOrden in orden:
                    array.append({"rubro":datosOrden.rubro,"tipo":"Orden emergencia","status":datosOrden.status, "ticket":datosOrden.ticket})
                if len(array)>0:
                    return JsonResponse(array,safe=False)  
                else:
                    return HttpResponse("bad")         
            else: 
                return HttpResponse("bad")
        elif tipo=="proveedor":
            orden=ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="CAN").exclude(status="REX").exclude(status="ENV").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
            if orden:
                array=[]
                for datosOrden in orden:
                    array.append({"rubro":datosOrden.rubro,"tipo":"Orden emergencia","status":datosOrden.status, "ticket":datosOrden.ticket})
                if len(array)>0:
                    return JsonResponse(array,safe=False)  
                else:
                    return HttpResponse("bad")         
            else: 
                return HttpResponse("bad")
        else: 
            return HttpResponse("bad")

@csrf_exempt
def checkTodasOrdenesEmergenciaCanceladas (request): 
    if request.method == 'POST':
        email = request.POST.get("email")
        tipo= request.POST.get("tipo")
        if tipo=="cliente":
            orden=ordenEmergencia.objects.filter(client_email=email).exclude(status="RED").exclude(status="ENV").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
            if orden:
                array=[]
                for datosOrden in orden:
                    array.append({"rubro":datosOrden.rubro,"tipo":"Orden emergencia","status":datosOrden.status, "ticket":datosOrden.ticket})
                if len(array)>0:
                    return JsonResponse(array,safe=False)  
                else:
                    return HttpResponse("bad")         
            else: 
                return HttpResponse("bad")
        elif tipo=="proveedor":
            orden=ordenEmergencia.objects.filter(proveedor_email=email).exclude(status="RED").exclude(status="ENV").exclude(status="ACE").exclude(status="EVI").exclude(status="ENS")
            if orden:
                array=[]
                for datosOrden in orden:
                    array.append({"rubro":datosOrden.rubro,"tipo":"Orden emergencia","status":datosOrden.status, "ticket":datosOrden.ticket})
                if len(array)>0:
                    return JsonResponse(array,safe=False)  
                else:
                    return HttpResponse("bad")         
            else: 
                return HttpResponse("bad")
        else: 
            return HttpResponse("bad")

@csrf_exempt
def checkOrdenEmergenciaParticular (request): 
        
        ticket = request.POST.get("ticket")
        tipo= request.POST.get("tipo")
        email=request.POST.get("email")
        
        if tipo=="cliente":
            orden=ordenEmergencia.objects.filter(ticket=ticket).first()
            if orden:
                imagen={}
                if orden.picture1:
                    imagen['picture1']="data:image/png;base64,"+base64.b64encode(orden.picture1.read()).decode('ascii')
                else: 
                    imagen['picture1']=""
                if orden.picture2: 
                    imagen['picture2']="data:image/png;base64,"+base64.b64encode(orden.picture2.read()).decode('ascii')
                else:
                    imagen['picture2']=""
                                         
                    data={"tipo":"Orden de emergencia","rubro":orden.rubro,"status":orden.status, "fecha_creacion":orden.fecha_creacion , "ticket":orden.ticket,
                    "descripcion":orden.problem_description,
                    "location_cliente_lat":orden.location_cliente_lat,"locatlocation_cliente_longion_long":orden.location_cliente_long,"proveedor_email":orden.proveedor_email,
                    "picture1":imagen['picture1'], "picture2":imagen['picture2'],"califico_el_cliente":orden.califico_el_cliente,
                    "califico_el_proveedor":orden.califico_el_proveedor,
                    "calificacion_proveedor":orden.calificacion_proveedor,
                    "calificacion_cliente":orden.calificacion_cliente,
                    "resena_al_proveedor":orden.resena_al_proveedor,
                    "resena_al_cliente":orden.resena_al_cliente  }

                    return JsonResponse(data,safe=False)  

            else:
                return HttpResponse("bad")
        elif tipo=="proveedor":
            orden=ordenEmergencia.objects.filter(ticket=ticket).filter(proveedor_email=email).first()
            if orden:
                imagen={}
                if orden.picture1:
                    imagen['picture1']="data:image/png;base64,"+base64.b64encode(orden.picture1.read()).decode('ascii')
                else: 
                    imagen['picture1']=""
                if orden.picture2: 
                    imagen['picture2']="data:image/png;base64,"+base64.b64encode(orden.picture2.read()).decode('ascii')
                else:
                    imagen['picture2']=""
                                         
                    data={"tipo":"Orden de emergencia","rubro":orden.rubro,"status":orden.status, "fecha_creacion":orden.fecha_creacion , "ticket":orden.ticket,"descripcion":orden.problem_description,
                    "location_cliente_lat":orden.location_cliente_lat,"locatlocation_cliente_longion_long":orden.location_cliente_long,"client_email":orden.client_email,
                    "picture1":imagen['picture1'], "picture2":imagen['picture2'],
                    "califico_el_cliente":orden.califico_el_cliente,
                    "califico_el_proveedor":orden.califico_el_proveedor,
                    "calificacion_proveedor":orden.calificacion_proveedor,
                    "calificacion_cliente":orden.calificacion_cliente,
                    "resena_al_proveedor":orden.resena_al_proveedor,
                    "resena_al_cliente":orden.resena_al_cliente  }

                    return JsonResponse(data,safe=False)  

            else:
                return HttpResponse("bad")
           
        else: 
            return HttpResponse("bad")
