from django.urls import path

# Vistas principales (login, inicio, salir, etc.)
from .views import login, salir, inicio, timeout, pantalla_principal

# API
from .Controladores.API.Estructuras_view_api import Menu_api, Unidad_Edu, Usuario

# Configuraciones
from .Controladores.Configuraciones.estructura_view_SMTP import smtp_view, smtp_edit, smtp_reenviar
from .Controladores.Configuraciones.Estructura_view_reportes import (
    reporte_usuarios, reporte_roles, reporte_horarioEst, reporte_horarioprofe,
)
from .Controladores.Configuraciones.Estructura_view_empresa import (
    empresas, NuevaEmpre, UpdateEmpre, eliminar_empresa,
)
from .Controladores.Configuraciones.Estructura_view_usuarios import (
    Usuarios, CreateUsuario, UpdateUsuario, eliminar_usuario,
)
from .Controladores.Configuraciones.Estructura_view_menu import (
    Menu, CreateMenu, UpdateMenu, eliminar_menu,
)
from .Controladores.Configuraciones.Estructura_view_acciones import (
    Acciones, Add_Accion, Edit_acciones,
)
from .Controladores.Configuraciones.Estructura_view_modulo import (
    Modulo, NuevoModulo, UpdateModulo, eliminar_modulo,
)
from .Controladores.Configuraciones.Estructura_view_permisos import (
    ListPermisos, CreatePermiso, UpdatePermisos,
)
from .Controladores.Configuraciones.Estructura_view_roles import (
    Roles, nuevo_rol, editar_rol, eliminar_rol,
)

# Mantenimiento
from .Controladores.Mantenimiento.Estructura_view_mantenimientos import (
    Empleado, Estudiante, Estudiantes, NuevoEstudiante, NuevoEmpleado,
    UpdateEmpleado, UpdateEstudiante, ConsultarEstudiante, ConsultarEmpleado,
    eliminar_estudiante, eliminar_empleado,
)
from .Controladores.Mantenimiento.Estructura_view_reportes import (
    reporte_estudiante, reporte_empleado, Reportepor_estudiante,
)
from .Controladores.Mantenimiento.Estructura_view_consultas import consultas
from .Controladores.Mantenimiento.Estructura_view_movimientos import movimientos
from .Controladores.Mantenimiento.Estructura_view_procesos import procesos

# Reportes especiales
from .Controladores.Reportes_especiales.Estructura_view_reportes import reportes

# Matriculación
from .Controladores.Matriculacion.View_estudiante import (
    filtro_estudiantes, filtro_estudiantes_lista,
    FilterEstudinatesestado, FilterTipoEstudinates,
)
from .Controladores.Matriculacion.Estructura_view_aniolectivo import (
    List_AnioLectivo, CreateAniolectivo, UpdateAniolectivo, eliminar_Aniolectivo,
)
from .Controladores.Matriculacion.asignacion_curso import (
    ListaAnioElectivoCurso, Create_Mov_Aniolectivo_curso,
    Update_Mov_Aniolectivo_curso, eliminar_Asignacion_Curso,
)
from .Controladores.Matriculacion.Estructura_view_curso import (
    ListaCurso, CreateCurso, UpdateCurso, DeleteCurso,
)
from .Controladores.Matriculacion.Estructura_view_horasDocentes import CreateHorasDocentes
from .Controladores.Matriculacion.Estructura_view_horario_curso import (
    HorarioCurso, ListViewHorario, CrearHorarioCurso, UpdateHorario, deleteHorario,
)
from .Controladores.Matriculacion.Asignacion_materia_curso import (
    Listar_materia_curso, Crear_materia_curso, Editar_materia_curso, eliminar_materia_curso,
)
from .Controladores.Matriculacion.estructura_view_materiaProfesor import MovMateriProfesorList
from .Controladores.Matriculacion.Estructura_view_asignacionprof import (
    List_docente, List_docente_asignado, List_docente_sin_asignar, eliminar_profesor,
)
from .Controladores.Matriculacion.estructura_view_genr_general import (
    General, CreateGeneral, UpdateGeneral,
)
from .Controladores.Matriculacion.Estructura_view_registronotas import (
    List_Notas, CrearRegistroNotas, ListarMateria, Update_notas,
    ListarMateria2, Update_notas2, Update_notasSupre, Delete_notas,
)
from .Controladores.Matriculacion.Estructura_view_file import Upload_File
from .Controladores.Matriculacion.Estructura_view_file_ex import Upload_FileEX

# Autocomplete
from .Filters.filters_admision import GEN_autocomplete, TID_autocomplete

urlpatterns = [
    # --- Autenticación ---
    path('', login, name='login'),
    path('salir/', salir, name='logout'),
    path('inicio/', inicio, name='inicio'),
    path('timeout/', timeout, name='timeout'),
    path('Pantalla_principal/', pantalla_principal, name='pantalla_principal'),

    # --- Configuraciones ---
    path('usuarios/', Usuarios.as_view(), name='usuarios'),
    path('nuevo_usuario/', CreateUsuario.as_view(), name='nuevo_usuario'),
    path('editar_usuario/<int:pk>/', UpdateUsuario.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:id>', eliminar_usuario, name='eliminar_usuario'),

    path('roles/', Roles.as_view(), name='roles'),
    path('nuevo_rol/', nuevo_rol, name='nuevo_rol'),
    path('editar_rol/<int:id>', editar_rol, name='editar_rol'),
    path('eliminar_rol/<int:id>', eliminar_rol, name='eliminar_rol'),

    path('menu/', Menu.as_view(), name='menu'),
    path('nuevo_menu/', CreateMenu.as_view(), name='nuevo_menu'),
    path('editar_menu/<int:pk>', UpdateMenu.as_view(), name='editar_menu'),
    path('eliminar_registro/<int:id>', eliminar_menu, name='eliminar_menu'),

    path('modulo/', Modulo.as_view(), name='modulo'),
    path('nuevo_modulo/', NuevoModulo.as_view(), name='nuevo_modulo'),
    path('editar_modulo/<int:pk>/', UpdateModulo.as_view(), name='editar_modulo'),
    path('eliminar_modulo/<int:id>', eliminar_modulo, name='eliminar_modulo'),

    path('empresas/', empresas, name='empresas'),
    path('nueva_empresa/', NuevaEmpre.as_view(), name='nueva_empresa'),
    path('editar_empresa/<int:pk>/', UpdateEmpre.as_view(), name='editar_empresa'),
    path('eliminar/<int:id>', eliminar_empresa, name='eliminar'),

    path('permisos/', ListPermisos.as_view(), name='permisos'),
    path('agregar_permisos/', CreatePermiso.as_view(), name='agregar_per'),
    path('agregar_permisos/<int:id>', CreatePermiso.as_view(), name='agregar_per'),
    path('editar_permiso/<int:pk>', UpdatePermisos.as_view(), name='editar_permiso'),

    path('acciones/', Acciones.as_view(), name='acciones'),
    path('nueva_accion/', Add_Accion.as_view(), name='nueva_accion'),
    path('editar_accion/<int:pk>/', Edit_acciones.as_view(), name='editar_accion'),

    path('agregar_smtp/', smtp_view, name='agregar_smtp'),
    path('editar_smtp/<int:pk>', smtp_edit.as_view(), name='edit_smtp'),
    path('usuario_temp/<int:pk>', smtp_reenviar, name='usuario_temp'),

    # --- Admisión / Mantenimiento ---
    path('empleado/', Empleado.as_view(), name='empleado'),
    path('estudiante/', Estudiante.as_view(), name='estudiante'),
    path('movimientos/', movimientos, name='movimientos'),
    path('consultas/', consultas, name='consultas'),
    path('procesos/', procesos, name='procesos'),
    path('reportes/', reportes, name='reportes'),
    path('registro_estudiante/', NuevoEstudiante.as_view(), name='registro_estudiante'),
    path('registro_empleado/', NuevoEmpleado.as_view(), name='registro_empleado'),
    path('editar_empleado/<int:pk>/', UpdateEmpleado.as_view(), name='editar_empleado'),
    path('editar_estudiante/<int:pk>/', UpdateEstudiante.as_view(), name='editar_estudiante'),
    path('consultar_estudiante/<int:pk>/', ConsultarEstudiante.as_view(), name='consultar_estudiante'),
    path('consultar_empleado/<int:pk>/', ConsultarEmpleado.as_view(), name='consultar_empleado'),
    path('eliminar_estudiante/<int:id>', eliminar_estudiante, name='eliminar_estudiante'),
    path('eliminar_empleado/<int:id>', eliminar_empleado, name='eliminar_empleado'),
    path('estudiantes/<int:pk>/', Estudiantes.as_view(), name='estudiantes'),

    # --- Reportes ---
    path('reporte_usuarios/', reporte_usuarios, name='reporte_usuarios'),
    path('reporte_roles/', reporte_roles, name='reporte_roles'),
    path('reporte_horarioestudy/', reporte_horarioEst, name='reporte_horarioestudy'),
    path('Horario_profesor/', reporte_horarioprofe, name='Horario_profesor'),
    path('reporte_estudiante/', reporte_estudiante, name='reporte_estudiante'),
    path('reporte_empleado/', reporte_empleado, name='reporte_empleado'),

    # --- Autocomplete ---
    path('TID_autocomplete/', TID_autocomplete.as_view(), name='TID_autocomplete'),
    path('GEN_autocomplete/', GEN_autocomplete.as_view(), name='GEN_autocomplete'),

    # --- Matriculación: Año Lectivo ---
    path('anio_lectivo/', List_AnioLectivo.as_view(), name='anio_lectivo'),
    path('Crear_Aniolectivo/', CreateAniolectivo.as_view(), name='crearAniolectivo'),
    path('Editar_Aniolectivo/<int:pk>', UpdateAniolectivo.as_view(), name='editarAniolectivo'),
    path('Eliminar_Aniolectivo/<int:id>', eliminar_Aniolectivo, name='eliminarAniolectivo'),

    # --- Matriculación: Asignación Curso ---
    path('asignacion_curso/', ListaAnioElectivoCurso.as_view(), name='asignacion_curso'),
    path('crear_asigancion_curso/', Create_Mov_Aniolectivo_curso.as_view(), name='crear_asigancion_curso'),
    path('editar_esignacion_curso/<int:pk>', Update_Mov_Aniolectivo_curso.as_view(), name='editar_esignacion_curso'),
    path('eliminar_asig_curso/<int:id>', eliminar_Asignacion_Curso, name='eliminar_asig_curso'),

    # --- Matriculación: Materia/Curso ---
    path('asignacion_materia_curso/', Listar_materia_curso.as_view(), name='asignacion_materia_curso'),
    path('crear_materia_curso/', Crear_materia_curso.as_view(), name='crear_materia_curso'),
    path('editar_materia_curso/<int:pk>', Editar_materia_curso.as_view(), name='editar_materia_curso'),
    path('eliminar_materia_curso/<int:id>', eliminar_materia_curso, name='eliminar_materia_curso'),

    # --- Tabla General ---
    path('general/', General.as_view(), name='general'),
    path('crear_general', CreateGeneral.as_view(), name='crear_general'),
    path('editar_general/<int:pk>', UpdateGeneral.as_view(), name='editar_general'),

    # --- Horas Docentes ---
    path('horas_docentes/', CreateHorasDocentes.as_view(), name='horas_docentes'),

    # --- Asignación Materias/Profesores ---
    path('horario_mod/<int:pk>', MovMateriProfesorList.as_view(), name='horario_mod'),
    path('asignacion_materiasprof/', List_docente.as_view(), name='asignacion_materiasprof'),
    path('eliminar_profesor/<int:id>', eliminar_profesor, name='eliminar_profesor'),
    path('profesoresAsignados', List_docente_asignado.as_view(), name='profesoresAsignados'),
    path('profesoresSinAsignar', List_docente_sin_asignar.as_view(), name='profesoresSinAsignar'),

    # --- Horarios por Curso ---
    path('horario_curso/', HorarioCurso.as_view(), name='horario_curso'),
    path('lista_horario/', ListViewHorario.as_view(), name='lista_horario'),
    path('crear_horariocurso/', CrearHorarioCurso.as_view(), name='crear_horariocurso'),
    path('editar_horario/<int:pk>', UpdateHorario.as_view(), name='editar_horario'),
    path('eliminar_horario/<int:id>', deleteHorario, name='eliminar_horario'),

    # --- Cursos ---
    path('cursos/', ListaCurso.as_view(), name='cursos'),
    path('create_curso/', CreateCurso.as_view(), name='create_curso'),
    path('edit_curso/<int:pk>', UpdateCurso.as_view(), name='edit_curso'),
    path('eliminar_curso/<int:pk>', DeleteCurso.as_view(), name='eliminar_curso'),

    # --- Registro de Notas ---
    path('registronotas/', List_Notas.as_view(), name='registro_notas'),
    path('CrearRegistroNotas/', CrearRegistroNotas.as_view(), name='Crear_RegistroNotas'),
    path('listarMateria/', ListarMateria.as_view(), name='listar_materia'),
    path('actualizar_notas/<int:pk>', Update_notas.as_view(), name='actualizar_registro_notas'),
    path('listarMateria2/', ListarMateria2.as_view(), name='listar_materia2'),
    path('actualizar_notas2/<int:pk>', Update_notas2.as_view(), name='actualizar_registro_notas2'),
    path('actualizar_notasSupre/<int:pk>', Update_notasSupre.as_view(), name='actualizar_registro_notasSupre'),
    path('eliminar_registronotas/<int:pk>', Delete_notas.as_view(), name='eliminar_registro_notas'),

    # --- Filtros de Estudiantes ---
    path('estudiantes_filtro/', filtro_estudiantes, name='estudiante_filtro'),
    path('estudiantes_lista/', filtro_estudiantes_lista, name='estudiante_lista'),
    path('tipo_estudiantes/<int:pk>', FilterTipoEstudinates.as_view(), name='tipo_estudiantes'),
    path('matriculacion_estados/<int:pk>', FilterEstudinatesestado.as_view(), name='matriculacion_estados'),

    # --- Importar Excel ---
    path('read_file/', Upload_File.as_view(), name='read_file'),
    path('read_file_ex/', Upload_FileEX.as_view(), name='read_file_ex'),
    path('ficha_matricula/<int:pk>', Reportepor_estudiante.as_view(), name='ficha_reporte'),

    # --- API REST ---
    path('api_menu/', Menu_api.as_view(), name='api_menu'),
    path('api_modulo/', Modulo.as_view(), name='api_modulo'),
]
