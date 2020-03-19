from django.contrib import admin
from . import models

# Register your models here.
class PreguntaAdmin(admin.ModelAdmin):
    fields = ('titulo', 'autor', 'cuerpo', 'etiquetas', 'votos_positivos')
    list_display = ('id', 'slug', 'titulo', 'votos_positivos', 'autor',)

class RespuestaAdmin(admin.ModelAdmin):
    fields = ('autor', 'cuerpo', 'discusion', 'votos_positivos')
    list_display = (
        'id', 'slug', 'cuerpo', 'autor', 'discusion',
        'votos_positivos', 'votos_negativos', 'created'
    )


admin.site.register(models.Pregunta, PreguntaAdmin)
admin.site.register(models.Respuesta, RespuestaAdmin)
