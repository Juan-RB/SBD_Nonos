from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from SBDcrud.models import Usuario,Trabajadores

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['codUser', 'get_nomTra', 'get_nomPer']

    def get_nomTra(self, obj):
        return obj.codTra.nomTra

    get_nomTra.short_description = 'Nombre del Trabajador'

    def get_nomPer(self, obj):
        return obj.codPer.nomPer

    get_nomPer.short_description = 'Nombre del Perfil'


class TrabajadoresAdmin(admin.ModelAdmin):
    list_display =['get_codTra','get_rutTra','get_dirTra','get_dirTel','get_emailTra','get_nomComuna']


    def get_codTra(self,obj):
        return obj.codTra
    
    get_codTra.short_description = 'Codigo del trabajador'

    def get_rutTra(self,obj):
        return obj.rutTra
    
    get_rutTra.short_description = 'Rut del trabajador'

    def get_dirTra(self,obj):
        return obj.dirTra
    
    get_dirTra.short_description = 'Direccion del trabajador'

    def get_dirTel(self,obj):
        return obj.telTra
        
    get_dirTel.short_description = 'Telefono del trabajador'

    
    def get_emailTra(self,obj):
        return obj.emailTra
        
    get_emailTra.short_description = 'Email del trabajador'

    def get_nomComuna(self, obj):
        return obj.codCom.nomCom
    
    get_nomComuna.short_description = 'Nombre de la Comuna'
    



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Trabajadores, TrabajadoresAdmin)
