from django.contrib import admin
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import (
    ConfUsuario, ConfEmpresa, ConfModulo, ConfRol, ConfMenu,
    ConfPermiso, ConfModulo_menu, ConfAccion,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantPersona
# Register your models here.


class GenrGeneralAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'tipo', 'codigo', 'idgenr_general']
    list_display = ('idgenr_general', 'tipo', 'codigo', 'nombre',)


admin.site.register(GenrGeneral, GenrGeneralAdmin)


class ConfUsuarioAdmin(admin.ModelAdmin):
    search_fields = ['usuario']
    list_display = ('id_usuario', 'usuario', 'clave', 'id_persona',
                    'id_genr_tipo_usuario', 'id_genr_estado',)


admin.site.register(ConfUsuario, ConfUsuarioAdmin)


class ConfEmpresaAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'correo', 'telefono', 'identificacion']
    list_display = ('id_empresa', 'nombre', 'razon_social', 'id_genr_tipo_identificacion', 'identificacion',
                    'direccion', 'representante_legal', 'correo', 'telefono', 'fecha_creacion', 'id_genr_estado')


admin.site.register(ConfEmpresa, ConfEmpresaAdmin)


class ConfModuloAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nombre']
    list_display = ('id_modulo', 'codigo', 'nombre', 'id_genr_estado',)


admin.site.register(ConfModulo, ConfModuloAdmin)


class ConfRolAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'codigo', 'id_genr_estado']
    list_display = ('id_rol', 'codigo', 'nombre', 'id_genr_estado')


admin.site.register(ConfRol, ConfRolAdmin)


class ConfMenuAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'codigo',
                     'descripcion', 'id_genr_estado', 'view']
    list_display = ('id_menu', 'id_padre', 'orden', 'descripcion',
                    'id_genr_estado', 'url', 'lazy_name', 'name', 'view')


admin.site.register(ConfMenu, ConfMenuAdmin)


class ConfPermisoAdmin(admin.ModelAdmin):
    search_fields = ['id_permiso']
    list_display = ('id_permiso','menu', 'id_rol','acciones',)


admin.site.register(ConfPermiso)


class ConfModulo_menuAdmin(admin.ModelAdmin):
    search_fields = ['id_modulo_menu']
    list_display = ('id_modulo_menu', 'id_modulo', 'id_menu',)


admin.site.register(ConfModulo_menu, ConfModulo_menuAdmin)


admin.site.register(ConfAccion)


class ConfPersonaAdmin(admin.ModelAdmin):
    search_fields = ['id_persona', 'nombres', 'apellidos', 'identificacion']

    list_display = ('id_persona', 'nombres', 'apellidos', 'fecha_de_nacimiento', 'estado', 'foto', 'id_genr_genero',
                    'id_genr_pais', 'id_genr_tipo_identificacion', 'id_genr_estado_civil', 'identificacion', 'telefono',
                    'correo', 'fecha_ingreso', 'usuario_ing', 'terminal_ing', 'id_genr_tipo_sangre', 'id_genr_etnia', 'direccion', 'id_genr_jornada', 'id_genr_indigena',
                    'id_genr_idioma_ancestral', 'celular', 'lugar_nacimiento', 'id_genr_provincia', 'id_genr_ciudad', 'id_genr_categoria_migratoria', 'discapacidad', 'discapacidad_renal',
                    'discapacidad_neurologica', 'enfermedad_alergica', 'asma', 'epilepsia', 'enfermedad_congenita', 'enfermedad_respiratoria', 'atencion_psicologica', 'bono_solidario', 'mienbros_hogar',
                    'id_genr_tipo_usuario', 'id_genr_estado_laboralp', 'pnombres', 'papellidos', 'pidentificacion', 'pdireccion', 'ptelefono', 'pvive_con_usted', 'id_genr_estado_laboralm', 'mnombres', 'mapellidos',
                    'mdireccion', 'mtelefono', 'midentificacion', 'mvive_con_usted', 'rnombres', 'rapellidos', 'rapellidos', 'rtelefono', 'id_genr_tipo_parentesco', 'rvive_con_usted', 'ridentificacion',)


admin.site.register(MantPersona)
