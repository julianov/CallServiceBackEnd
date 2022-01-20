"""callservices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from callserviceapp.views import Buscar, addRubro, agregarFotoOrden, askPersonalInfo, cambiarEstadoOrden, completeInfo, completeInfoRubros, consultarOrdenes, consultarTodasLasOrdenesCliente, datosCliente, datosProveedor, deleteRubro, finalizarOrdenCliente, finalizarOrdenProveedor, homeCliente, homeClientePedirDatos, login, masInfoOrdenCliente, masInfoOrdenProveedor, modificarRubro, nuevaInfoPersonal, pedirOrdenGeneral, presupuestoCliente, presupuestoProveedor,register, requestRubros, restarPassword, setNewPassword, verReseñas

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('admin/', admin.site.urls),

    path('home/cliente/<lat>/<long>', homeCliente),
    path('home/cliente/pedirdatos/<email>/<rubro>/<tipoPedido>/<lat>/<long>', homeClientePedirDatos),
    
    path('registro/<type>/<email>/<password>', register),

    path('completarinfo/completar',completeInfo),
    path('cambiarInfoPersonal', nuevaInfoPersonal),

    path('completarinfo/rubros/<modo>/<tipo>/<email>',completeInfoRubros),
    path('completarinfo/pedirrubros/<tipo>/<email>/<rubro>',requestRubros),
    path('completarinfo/subirrubro',addRubro), 
    path('completarinfo/eliminarRubro', deleteRubro),
    path('completarinfo/modificarRubro', modificarRubro),

    path('askpersonalinfo/<type>/<email>', askPersonalInfo),

    path('login/ingresar/<email>/<password>', login),
    path('login/restaurar/codigo/<email>', restarPassword),
    path('login/restaurar/setpassword/<email>/<codigo>/<password>', setNewPassword),

    path('search/<tipo>/<dato>', Buscar),

    path('resena/<email>/<cantida>/<tipo>',verReseñas),
    

    path('orden/ordengeneral', pedirOrdenGeneral), #GENERAR ORDEN POR PARTE DEL CLIENTE   
    path('orden/misordenes/<tipo>/<email>', consultarOrdenes),  #lista de ordenes de un proveedor
    path('orden/datocliente/<n_ticket>/<tipo_orden>',datosCliente),
    path('orden/datoproveedor/<n_ticket>/<tipo_orden>',datosProveedor),
    path('orden/cambiarestado/<n_ticket>/<tipo_orden>/<nuevo_estado_orden>',cambiarEstadoOrden),
    path('orden/agregarfoto',agregarFotoOrden),
    path('orden/masInfo/proveedor',masInfoOrdenProveedor),
    path('orden/masInfo/cliente',masInfoOrdenCliente),
    path('orden/presupuesto/proveedor',presupuestoProveedor),
    path('orden/presupuesto/cliente',presupuestoCliente),
    path('orden/finalizar/proveedor',finalizarOrdenProveedor),
    path('orden/finalizar/cliente',finalizarOrdenCliente),

    path('orden/consultarOrdenes/<email>', consultarTodasLasOrdenesCliente),  #lista de ordenes de un proveedor





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)