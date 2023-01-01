from django.contrib import admin
from .models import  campañaPublicidad, chat, ordenEmergencia, ordenEmergenciaLista, ordenGeneral, user_data, validation_token 
from .models import item 


# Register your models here.
admin.site.register(user_data)
admin.site.register(item)
admin.site.register(validation_token)
admin.site.register(ordenGeneral)
admin.site.register(ordenEmergencia)
admin.site.register(ordenEmergenciaLista)

admin.site.register(chat)

admin.site.register(campañaPublicidad)

