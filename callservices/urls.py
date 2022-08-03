from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from callserviceapp.views import agregarFotoOrden, askPersonalInfo, buscar, cambiarEstadoOrden, cambiarfechaordengeneral, chatMensaje, chatSinLeer, chatVer, clienteRechazaOrdenEmergencia, completeInfo, completeInfoRubros, consultarOrdenParticular, consultarOrdenes, consultarTodasLasOrdenes, consultarTodasLasOrdenesCanceladas, consultarTodasLasOrdenesCurso, consultarTodasLasOrdenesFinalizadas, datosCliente, datosProveedor, deleteRubro, finalizarOrdenCliente, finalizarOrdenProveedor, homeCliente, homeClientePedirDatos, login, masInfoOrdenCliente, masInfoOrdenProveedor, modificarRubro, nuevaInfoPersonal, pedirOrdenEmergencia, pedirOrdenGeneral, presupuestoCliente, presupuestoProveedor, proveedorAceptaOrdenEmergencia, proveedorEnViajeOrdenEmergencia, proveedorRechazaOrdenEmergencia, proveedorUbicacion, register, requestRubros, restarPassword, setNewPassword, verReseñas,addRubro 

from callserviceapp import views

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('admin/', admin.site.urls),

    path('home/cliente/<lat>/<long>', homeCliente),
    path('home/cliente/pedirdatos/<email>/<rubro>/<tipoPedido>/<lat>/<long>', homeClientePedirDatos),

    path('proveedor/ubicacion/<email>/<lat>/<long>', proveedorUbicacion),
    
    path('registro/', register),

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

    path('search/<tipo>/<dato>', buscar),

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
    path('orden/cambiarfecharubrogeneral',cambiarfechaordengeneral),
    path('orden/finalizar/cliente',finalizarOrdenCliente),

    path('orden/consultarOrdenes/<tipo>/<email>', consultarTodasLasOrdenes),  #todas las ordenes de un cliente cambiar si se cambian los estados de la orden de emergencia. 
    path('orden/consultarOrdenesCanceladas/<tipo>/<email>', consultarTodasLasOrdenesCanceladas),  #todas las ordenes de un cliente cambiar si se cambian los estados de la orden de emergencia. 
    path('orden/consultarOrdenesCurso/<tipo>/<email>', consultarTodasLasOrdenesCurso),  #todas las ordenes de un cliente cambiar si se cambian los estados de la orden de emergencia. 
    path('orden/consultarOrdenesFinalizadas/<tipo>/<email>', consultarTodasLasOrdenesFinalizadas),  #todas las ordenes de un cliente cambiar si se cambian los estados de la orden de emergencia. 

    path('orden/consultarOrdenParticular/<ticket>', consultarOrdenParticular),   

    path('chat/mensaje/<email>/<ticket>/<mensaje>/<dia>/<hora>', chatMensaje),
    path('chat/<ticket>/<email>', chatVer),
    path('chatsinleer/<email>', chatSinLeer),

    path('orden/ordenEmergencia/', pedirOrdenEmergencia), #GENERAR ORDEN POR PARTE DEL CLIENTE   
    path('orden/ordenEmergencia/proveedorAcepta/<email>/<ticket>', proveedorAceptaOrdenEmergencia),
    path('orden/ordenEmergencia/rechazarOrdenCliente', clienteRechazaOrdenEmergencia),
    path('orden/ordenEmergencia/rechazarOrdenProveedor/<email>/<ticket>', proveedorRechazaOrdenEmergencia),
    path('orden/ordenEmergencia/proveedorEnViaje/<ticket>', proveedorEnViajeOrdenEmergencia),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)