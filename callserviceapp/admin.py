from django.contrib import admin
from .models import Proveedor, campañaPublicidad, chat, client, company, item_company, ordenEmergencia, ordenGeneral 
from .models import serviceProvider 
from .models import order 
from .models import item 


# Register your models here.
admin.site.register(client)
admin.site.register(serviceProvider)
admin.site.register(item)
admin.site.register(company)
admin.site.register(item_company)

admin.site.register(Proveedor)
admin.site.register(ordenGeneral)
admin.site.register(ordenEmergencia)
admin.site.register(chat)
admin.site.register(order)

admin.site.register(campañaPublicidad)

