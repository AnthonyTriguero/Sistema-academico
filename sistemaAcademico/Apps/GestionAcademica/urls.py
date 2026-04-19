import pickle
from django.db import models
from django.urls import path

from sistemaAcademico.Apps.GestionAcademica.Controladores.API.Estructuras_view_api import *
from sistemaAcademico.Apps.GestionAcademica.Controladores.Configuraciones.estructura_view_SMTP import smtp_view, \
    smtp_edit, smtp_reenviar
from sistemaAcademico.Apps.GestionAcademica.Controladores.Configuraciones.Estructura_view_reportes import *
from sistemaAcademico.Apps.GestionAcademica.Controladores.Reportes_especiales.Estructura_view_reportes import *
from sistemaAcademico.Apps.GestionAcademica.Filters.filters_admision import GEN_autocomplete, TID_autocomplete
from sistemaAcademico.Apps.GestionAcademica.Controladores.Matriculacion.Estructura_view_aniolectivo import *
from sistemaAcademico.Apps.GestionAcademica.Controladores.Matriculacion.asignacion_curso import *
from .Controladores.Matriculacion.Estructura_view_curso import ListaCurso, CreateCurso, UpdateCurso, DeleteCurso
from .Controladores.Matriculacion.Estructura_view_horasDocentes import CreateHorasDocentes
from sistemaAcademico.Apps.GestionAcademica.Controladores.Matriculacion.Estructura_view_horario_curso import *
from sistemaAcademico.Apps.GestionAcademica.Controladores.Matriculacion.Asignacion_materia_curso import *

from .Controladores.Matriculacion.estructura_view_materiaProfesor import *
from .Controladores.Matriculacion.Estructura_view_asignacionprof import *

from .Controladores.Matriculacion.estructura_view_genr_general import *
from .Controladores.Reportes_especiales.Estructura_view_reportes import reportes
from .Controladores.Matriculacion.Estructura_view_registronotas import *
from .views import *
from .Controladores.Configuraciones.Estructura_view_acciones import *
from .Controladores.Mantenimiento.Estructura_view_mantenimientos import *
from .Diccionario.Estructuras_tablas_conf import *
from .Diccionario.Estructuras_tablas_mant import *
from .Diccionario.Estructuras_tablas_mov import *
from django.views.decorators.cache import cache_page
from sistemaAcademico.Apps.GestionAcademica.Controladores.Matriculacion.Estructura_view_file import Upload_File
from sistemaAcademico.Apps.GestionAcademica.Controladores.Matriculacion.Estructura_view_file_ex import Upload_FileEX



urlpatterns = [
    path('', login, name='login'),
    path('salir/', salir, name='logout'),
    path('inicio/', inicio, name='inicio'),
    path('usuarios/', Usuarios.as_view(), name='usuarios'),
    path('roles/', Roles.as_view(), name='roles'),
    path('menu/', Menu.as_view(), name='menu'),
    path('modulo/', Modulo.as_view(), name='modulo'),
    path('empresas/', empresas, name='empresas'),
    # Opciones para el modulo de Admision
    path('empleado/', Empleado.as_view(), name='empleado'),
    path('estudiante/', Estudiante.as_view(), name='estudiante'),
    path('movimientos/', movimientos, name='movimientos'),
    path('consultas/', consultas, name='consultas'),
    path('procesos/', procesos, name='procesos'),
    path('reportes/', reportes, name='reportes'),
    path('editar_smtp/<int:pk>', smtp_edit.as_view(), name='edit_smtp'),
    # ----------------REGISTROS--------------
    path('nueva_empresa/', NuevaEmpre.as_view(), name='nueva_empresa'),
    path('usuario_temp/<int:pk>', smtp_reenviar, name='usuario_temp'),
    path('nuevo_usuario/', CreateUsuario.as_view(), name='nuevo_usuario'),
    path('nuevo_rol/', nuevo_rol, name='nuevo_rol'),
    # path('nuevo_menu/', nuevo_menu, name='nuevo_menu'),
    path('nuevo_menu/', CreateMenu.as_view(), name='nuevo_menu'),
    path('nuevo_modulo/', NuevoModulo.as_view(), name='nuevo_modulo'),
    path('agregar_permisos/<int:id>', CreatePermiso.as_view(), name='agregar_per'),
    # ------- Url de permisos
    path('agregar_permisos/', CreatePermiso.as_view(), name='agregar_per'),
    path('editar_permiso/<int:pk>', UpdatePermisos.as_view(), name='editar_permiso'),
    path('permisos/', ListPermisos.as_view(), name='permisos'),
    # ---Url de Acciones
    path('acciones/', Acciones.as_view(), name='acciones'),
    path('nueva_accion/', Add_Accion.as_view(), name='nueva_accion'),
    path('editar_accion/<int:pk>/', Edit_acciones.as_view(), name='editar_accion'),

    # Url de Usuarios temporales
    path('agregar_smtp/', smtp_view, name='agregar_smtp'),
    path('agregar_smtp/' + 'timeout/', timeout, name='timeout_agregar_smtp'), 
    # -------------EDICION---------------------
    # path('editar_empresa/<int:id>', editar_empresa, name='editar_empresa'),
    path('editar_modulo/<int:pk>/', UpdateModulo.as_view(), name='editar_modulo'),
    path('editar_empresa/<int:pk>/', UpdateEmpre.as_view(), name='editar_empresa'),
    path('editar_usuario/<int:pk>/', UpdateUsuario.as_view(), name='editar_usuario'),
    # path('editar_usuario/(?P<pk>[0-9]+)\\/$',UpdateUsuario.as_view(), name='editar_usuario'),
    path('editar_rol/<int:id>', editar_rol, name='editar_rol'),
    path('editar_menu/<int:pk>', UpdateMenu.as_view(), name='editar_menu'),
    # path('editar_menu/<int:id>', editar_menu, name='editar_menu'),
    # path('editar_modulo/<int:id>', editar_modulo, name='editar_modulo'),
    path('eliminar_modulo/<int:id>', eliminar_modulo, name='eliminar_modulo'),
    # ------------ELIMINACION----------------------
    path('eliminar_registro/<int:id>', eliminar_menu, name='eliminar_menu'),
    path('eliminar/<int:id>', eliminar_empresa, name='eliminar'),
    path('eliminar_usuario/<int:id>', eliminar_usuario, name='eliminar_usuario'),
    path('eliminar_rol/<int:id>', eliminar_rol, name='eliminar_rol'),
    # ---------------------------------------------
    path('Pantalla_principal/', pantalla_principal, name='pantalla_principal'),
    # --------------timeout-------
    path('timeout/', timeout, name='timeout'),
    path('inicio/' + 'timeout/', timeout, name='timeout_inicio'),
    path('acciones/' + 'timeout/', timeout, name='timeout_acciones'),
    path('Nueva_Accion/' + 'timeout/', timeout, name='timeou_Nueva_Accion'),
    path('editar_accion/' + 'timeout/', timeout, name='timeout_editar_accion'),
    path('perfiles/' + 'timeout/', timeout, name='timeout_perfiles'),
    path('menu/' + 'timeout/', timeout, name='timeout_menu'),
    path('eliminar_registro/' + 'timeout/', timeout, name='timeout_eliminar_registro'),
    path('modulo/' + 'timeout/', timeout, name='timeout_modulo'),
    path('editar_modulo/' + 'timeout/', timeout, name='timeout_editar_modulo'),
    path('usuarios/' + 'timeout/', timeout, name='timeout_usuarios'),
    path('empresas/' + 'timeout/', timeout, name='timeout_empresas'),
    path('nueva_empresa/' + 'timeout/', timeout, name='timeout_nueva_empresa'),
    path('eliminar/' + 'timeout/', timeout, name='timeout_eliminar'),
    path('editar_empresa/' + 'timeout/', timeout, name='timeout_editar_empresa'),
    path('movimientos/' + 'timeout/', timeout, name='timeout_movimientos'),
    path('mantenimiento/' + 'timeout/', timeout, name='timeout_mantenimiento'),
    path('roles/' + 'timeout/', timeout, name='timeout_roles'),
    path('nuevo_rol/' + 'timeout/', timeout, name='timeout_nuevo_rol'),
    path('editar_rol/' + 'timeout/', timeout, name='timeout_editar_rol'),
    path('eliminar_rol/' + 'timeout/', timeout, name='timeout_eliminar_rol'),
    path('permisos/' + 'timeout/', timeout, name='timeout_permisos'),
    path('agregar_permisos/' + 'timeout/', timeout, name='timeout_agregar_permisos'),
    path('editar_permiso/' + 'timeout/', timeout, name='timeout_editar_permiso'),
    path('nuevo_modulo/' + 'timeout/', timeout, name='timeout_nuevo_modulo'),
    path('estudiante/' + 'timeout/', timeout, name='timeout_estudiante'),
    path('empleado/' + 'timeout/', timeout, name='timeout_empleado'),  
   
    
    # -----Rest-framework-APIS
    path('api_menu/', Menu_api.as_view(), name='api_menu'),
    path('api_modulo/', Modulo.as_view(), name='api_modulo'),
    # Opciones para el modulo de Mantenimiento
    # Crear
    path('registro_estudiante/', NuevoEstudiante.as_view(), name='registro_estudiante'),
    path('registro_empleado/', NuevoEmpleado.as_view(), name='registro_empleado'),
    # Editar
    path('editar_empleado/<int:pk>/', UpdateEmpleado.as_view(), name='editar_empleado'),
    path('editar_empleado' + 'timeout/', timeout, name='timeout_editar_empleado'),
    path('editar_estudiante/<int:pk>/', UpdateEstudiante.as_view(), name='editar_estudiante'),
    path('consultar_estudiante/<int:pk>/', ConsultarEstudiante.as_view(), name='consultar_estudiante'),
    path('consultar_empleado/<int:pk>/', ConsultarEmpleado.as_view(), name='consultar_empleado'),
    # Eliminar
    path('eliminar_estudiante/<int:id>', eliminar_estudiante, name='eliminar_estudiante'),
    path('eliminar_estudiante/' + 'timeout/', timeout, name='timeout_eliminar_estudiante'),
    path('eliminar_empleado/<int:id>', eliminar_empleado, name='eliminar_empleado'),
    path('eliminar_empleado/' + 'timeout/', timeout, name='timeout_eliminar_empleado'),
    # ------------Reportes de Configuraciones---------------
    path('reporte_usuarios/', reporte_usuarios, name='reporte_usuarios'),
    path('reporte_usuarios/' + 'timeout/', timeout, name='timeout_reporte_usuarios'),   
    path('reporte_roles/', reporte_roles, name='reporte_roles'),
    path('reporte_roles/' + 'timeout/', timeout, name='timeout_reporte_roles'), 
    path('reporte_horarioestudy/', reporte_horarioEst, name='reporte_horarioestudy'),
    path('Horario_profesor/', reporte_horarioprofe, name='Horario_profesor'),
    # ------------Reportes de Mantenimiento---------------
    path('reporte_estudiante/', reporte_estudiante, name='reporte_estudiante'),
    path('reporte_estudiante/' + 'timeout/', timeout, name='timeout_reporte_estudiante'),
    path('reporte_empleado/', reporte_empleado, name='reporte_empleado'),
    path('reporte_empleado/' + 'timeout/', timeout, name='timeout_reporte_empleado'),
    # ---------Django-Autocomplete-Filters----------
    path('TID_autocomplete/', TID_autocomplete.as_view(), name='TID_autocomplete'),
    path('GEN_autocomplete/', GEN_autocomplete.as_view(), name='GEN_autocomplete'),
    # --------------Matriculacion-------------------
    path('anio_lectivo/', List_AnioLectivo.as_view(), name='anio_lectivo'),
    path('Editar_Aniolectivo/<int:pk>', UpdateAniolectivo.as_view(), name='editarAniolectivo'),
    path('Crear_Aniolectivo/', CreateAniolectivo.as_view(), name='crearAniolectivo'),
    path('Eliminar_Aniolectivo/<int:id>', eliminar_Aniolectivo, name='eliminarAniolectivo'),
    path('anio_lectivo/' + 'timeout/' ,timeout, name='timeout_anio_lectivo'),
    path('Crear_Aniolectivo/' + 'timeout/' ,timeout, name='timeout_Crear_Aniolectivo'),
    path('Eliminar_Aniolectivo/' + 'timeout/' ,timeout, name='timeout_Crear_Aniolectivo'),

    # ------Matriculacion - Asignacion de curso - año electivo-----------
    path('asignacion_curso/', ListaAnioElectivoCurso.as_view(), name='asignacion_curso'),
    path('crear_asigancion_curso/', Create_Mov_Aniolectivo_curso.as_view(), name='crear_asigancion_curso'),
    path('editar_esignacion_curso/<int:pk>', Update_Mov_Aniolectivo_curso.as_view(), name='editar_esignacion_curso'),
    path('eliminar_asig_curso/<int:id>', eliminar_Asignacion_Curso, name='eliminar_asig_curso'),

    path('asignacion_curso/' + 'timeout/' ,timeout, name='timeout_asignacion_curso'),
    path('crear_asigancion_curso/' + 'timeout/' ,timeout, name='timeout_crear_asigancion_curso'),
    path('eliminar_asig_curso/' + 'timeout/' ,timeout, name='timeout_eliminar_asig_curso'),
    path('editar_esignacion_curso/' + 'timeout/' ,timeout, name='timeout_editar_esignacion_curso'),

    # --------Matriculacion - Asignar - MAteria - Curso------------------
    path('asignacion_materia_curso/', Listar_materia_curso.as_view(), name='asignacion_materia_curso'),
    path('crear_materia_curso/', Crear_materia_curso.as_view(), name='crear_materia_curso'),
    path('editar_materia_curso/<int:pk>', Editar_materia_curso.as_view(), name='editar_materia_curso'),
    path('eliminar_materia_curso/<int:id>', eliminar_materia_curso, name='eliminar_materia_curso'),

    path('asignacion_materia_curso/' + 'timeout/' ,timeout, name='timeout_asignacion_materia_curso'),
    path('eliminar_materia_curso/' + 'timeout/' ,timeout, name='timeout_eliminar_materia_curso'),

    # ------Matriculacion - Tabla general-----------
    path('general/', General.as_view(), name='general'),
    path('crear_general', CreateGeneral.as_view(), name='crear_general'),
    path('editar_general/<int:pk>', UpdateGeneral.as_view(), name='editar_general'),
    path('general/' + 'timeout/' ,timeout, name='timeout_general'),
    path('crear_general/' + 'timeout/' ,timeout, name='timeout_crear_general'),
    path('editar_general/' + 'timeout/' ,timeout, name='timeout_editar_general'),
    # ----------- Asignacion horas a docentes ---------------
    path('horas_docentes/', CreateHorasDocentes.as_view(), name='horas_docentes'),
    path('horas_docentes/' + 'timeout/' ,timeout, name='timeout_horas_docentes'),
    # ----------- Asignacion materias a docentes ------------------------------
    path('horario_mod/<int:pk>', MovMateriProfesorList.as_view(), name='horario_mod'),
    path('asignacion_materiasprof/', List_docente.as_view(), name='asignacion_materiasprof'),
    path('eliminar_profesor/<int:id>', eliminar_profesor, name='eliminar_profesor'),
    path('profesoresAsignados', List_docente_asignado.as_view(), name= 'profesoresAsignados'),
    path('profesoresSinAsignar', List_docente_sin_asignar.as_view(), name= 'profesoresSinAsignar'),
    path('asignacion_materiasprof/' + 'timeout/' ,timeout, name='timeout_asignacion_materiasprof'),
    path('profesoresAsignados/' + 'timeout/' ,timeout, name='timeout_profesoresAsignados'),
    path('profesoresSinAsignar/' + 'timeout/' ,timeout, name='timeout_profesoresSinAsignar'),
    path('eliminar_profesor/' + 'timeout/' ,timeout, name='timeout_eliminar_profesor'),

    # ----------- Ingreso horario por cursos ---------------
    path('horario_curso/', HorarioCurso.as_view(), name='horario_curso'),
    path('lista_horario/', ListViewHorario.as_view(), name='lista_horario'),
    path('crear_horariocurso/', CrearHorarioCurso.as_view(), name='crear_horariocurso'),
    path('editar_horario/<int:pk>', UpdateHorario.as_view(), name='editar_horario'),
    path('eliminar_horario/<int:id>', deleteHorario, name='eliminar_horario'),
    path('lista_horario/' + 'timeout/' ,timeout, name='timeout_lista_horario'),
    path('eliminar_horario/' + 'timeout/' ,timeout, name='timeout_eliminar_horario'),

    #------------ CURSOS -------------------------------
    path('cursos/', ListaCurso.as_view(), name='cursos'),
    path('create_curso/', CreateCurso.as_view(), name='create_curso'),
    path('edit_curso/<int:pk>', UpdateCurso.as_view(), name='edit_curso'),
    path('eliminar_curso/<int:pk>', DeleteCurso.as_view(), name='eliminar_curso'),
    path('create_curso/' + 'timeout/' ,timeout, name='timeout_create_curso'),
    path('eliminar_curso/' + 'timeout/' ,timeout, name='timeout_eliminar_curso'),
    path('cursos/' + 'timeout/' ,timeout, name='timeout_cursos'),
    # ---------registro notas ---------------------------
    path('registronotas/', List_Notas.as_view(), name='registro_notas'),

    # Nota 1 Quimestre
    path('CrearRegistroNotas/', CrearRegistroNotas.as_view(), name='Crear_RegistroNotas'),
    path('listarMateria/', ListarMateria.as_view(), name='listar_materia'),
    path('actualizar_notas/<int:pk>', Update_notas.as_view(), name='actualizar_registro_notas'),

    # NOTA 2 QUIMESTRE
    path('listarMateria2/', ListarMateria2.as_view(), name='listar_materia2'),
    path('actualizar_notas2/<int:pk>', Update_notas2.as_view(), name='actualizar_registro_notas2'),

    # Si se Queda
    path('actualizar_notasSupre/<int:pk>', Update_notasSupre.as_view(), name='actualizar_registro_notasSupre'),

    # Eliminar Nota Definitivamente
    path('eliminar_registronotas/<int:pk>', Delete_notas.as_view(), name='eliminar_registro_notas'),

    path('estudiantes_filtro/',filtro_estudiantes,name='estudiante_filtro'),
    path('estudiantes_lista/',filtro_estudiantes_lista,name="estudiante_lista"),
    path('tipo_estudiantes/<int:pk>',FilterTipoEstudinates.as_view(),name='tipo_estudiantes'),
    path('matriculacion_estados/<int:pk>',FilterEstudinatesestado.as_view(),name='matriculacion_estados'),

    #------------ subir excel ---------
    path('read_file/',Upload_File.as_view(),name='read_file'),
    path('read_file_ex/',Upload_FileEX.as_view(),name='read_file_ex'),
    path('ficha_matricula/<int:pk>',Reportepor_estudiante.as_view(),name='ficha_reporte'),

    path('estudiantes/<int:pk>/', Estudiantes.as_view(), name='estudiantes'),


]