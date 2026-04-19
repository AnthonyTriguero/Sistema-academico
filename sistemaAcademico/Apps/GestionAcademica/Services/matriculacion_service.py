"""
Servicio de matriculación de estudiantes.
Contiene la lógica de negocio para el proceso de matriculación.
"""
import logging
import socket
from typing import List, Tuple
from django.utils import timezone

from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import (
    MovMatriculacionEstudiante, Mov_Aniolectivo_curso, MovDetalleMateriaCurso,
    Mov_Materia_profesor, MovDetalleRegistroNotas, MovCabRegistroNotas,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario

logger = logging.getLogger(__name__)


class MatriculacionService:
    """Servicio para gestionar la lógica de negocio de matriculación."""

    @staticmethod
    def matricular_estudiante(
        matricula: MovMatriculacionEstudiante,
        usuario: ConfUsuario
    ) -> Tuple[bool, List[str]]:
        """
        Matricula un estudiante creando sus registros de notas.
        
        Args:
            matricula: Instancia de MovMatriculacionEstudiante
            usuario: Usuario que realiza la matriculación
            
        Returns:
            Tuple[bool, List[str]]: (éxito, lista_de_errores)
        """
        errores = []
        
        # Verificar si ya está matriculado
        if matricula.estado.nombre == 'MATRICULADO':
            logger.info(f"Estudiante {matricula.id_estudiante} ya está matriculado")
            return True, []
        
        # Obtener quimestres
        quimestres = GenrGeneral.objects.filter(tipo='QUI')
        if not quimestres.exists():
            errores.append("No se encontraron quimestres configurados en el sistema")
            return False, errores
        
        # Obtener curso y materias
        id_aniolectivo_curso = matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso
        curso = Mov_Aniolectivo_curso.objects.get(id_mov_anioelectivo_curso=id_aniolectivo_curso)
        materias_curso = MovDetalleMateriaCurso.objects.filter(
            id_mov_anio_lectivo_curso=curso.id_mov_anioelectivo_curso
        )
        
        if not materias_curso.exists():
            errores.append(f"El curso no tiene materias asignadas")
            return False, errores
        
        # Crear registros de notas para cada materia
        for detalle_materia in materias_curso:
            try:
                # Verificar que la materia tenga profesor asignado
                materia_profesor = Mov_Materia_profesor.objects.filter(
                    id_detalle_materia_curso=detalle_materia.id_detalle_materia_curso
                ).first()
                
                if not materia_profesor:
                    error_msg = f"La materia '{detalle_materia}' no tiene un profesor asignado"
                    logger.warning(error_msg)
                    errores.append(error_msg)
                    continue
                
                # Crear registros de notas por quimestre
                MatriculacionService._crear_registros_notas_por_quimestre(
                    matricula=matricula,
                    materia_profesor=materia_profesor,
                    detalle_materia=detalle_materia,
                    quimestres=quimestres,
                    usuario=usuario
                )
                
            except Exception as e:
                error_msg = f"Error al procesar materia '{detalle_materia}': {str(e)}"
                logger.error(error_msg, exc_info=True)
                errores.append(error_msg)
        
        # Si hay errores críticos, no se completa la matriculación
        if errores:
            return False, errores
        
        logger.info(f"Estudiante {matricula.id_estudiante} matriculado exitosamente")
        return True, []
    
    @staticmethod
    def _crear_registros_notas_por_quimestre(
        matricula: MovMatriculacionEstudiante,
        materia_profesor: Mov_Materia_profesor,
        detalle_materia: MovDetalleMateriaCurso,
        quimestres,
        usuario: ConfUsuario
    ) -> None:
        """
        Crea los registros de notas para cada quimestre.
        
        Args:
            matricula: Matriculación del estudiante
            materia_profesor: Relación materia-profesor
            detalle_materia: Detalle de la materia del curso
            quimestres: QuerySet de quimestres
            usuario: Usuario que realiza la operación
        """
        anio_lectivo = Mov_Aniolectivo_curso.objects.get(
            id_mov_anioelectivo_curso=detalle_materia.id_mov_anio_lectivo_curso.id_mov_anioelectivo_curso
        )
        
        for quimestre in quimestres:
            # Crear detalle de registro de notas
            detalle_registro = MovDetalleRegistroNotas(
                id_matriculacion_estudiante=matricula,
                id_materia_profesor=materia_profesor,
                id_general_quimestre=quimestre,
            )
            detalle_registro.save()
            
            # Crear cabecera de registro de notas
            cabecera_registro = MovCabRegistroNotas(
                id_detalle_registro_notas=detalle_registro,
                id_mov_anioelectivo_curso=anio_lectivo,
                promedio_curso_1q=0,
                promedio_curso_2q=0,
                promedio_curso_general=0,
                fecha_ingreso=timezone.now(),
                usuario_ing=usuario.usuario,
                terminal_ing=socket.gethostname(),
            )
            cabecera_registro.save()
            
            logger.debug(
                f"Registro de notas creado: Estudiante={matricula.id_estudiante}, "
                f"Materia={materia_profesor}, Quimestre={quimestre}"
            )
    
    @staticmethod
    def validar_cambio_estado(
        matricula: MovMatriculacionEstudiante,
        nuevo_estado: GenrGeneral
    ) -> Tuple[bool, str]:
        """
        Valida si se puede cambiar el estado de una matriculación.
        
        Args:
            matricula: Matriculación a validar
            nuevo_estado: Nuevo estado a aplicar
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        # Si el nuevo estado es MATRICULADO, validar requisitos
        if nuevo_estado.nombre == 'MATRICULADO':
            # Verificar que el curso tenga materias
            id_aniolectivo_curso = matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso
            curso = Mov_Aniolectivo_curso.objects.get(id_mov_anioelectivo_curso=id_aniolectivo_curso)
            materias_curso = MovDetalleMateriaCurso.objects.filter(
                id_mov_anio_lectivo_curso=curso.id_mov_anioelectivo_curso
            )
            
            if not materias_curso.exists():
                return False, "El curso no tiene materias asignadas"
            
            # Verificar que todas las materias tengan profesor
            materias_sin_profesor = []
            for materia in materias_curso:
                tiene_profesor = Mov_Materia_profesor.objects.filter(
                    id_detalle_materia_curso=materia.id_detalle_materia_curso
                ).exists()
                
                if not tiene_profesor:
                    materias_sin_profesor.append(str(materia))
            
            if materias_sin_profesor:
                return False, f"Las siguientes materias no tienen profesor asignado: {', '.join(materias_sin_profesor)}"
        
        return True, ""
