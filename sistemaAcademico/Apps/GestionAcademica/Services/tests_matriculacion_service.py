"""
Tests unitarios para el servicio de matriculación.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import Mock, patch, MagicMock

from sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service import MatriculacionService
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import (
    MovMatriculacionEstudiante,
)
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario


class MatriculacionServiceTest(TestCase):
    """Tests para MatriculacionService."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        # Mock del usuario
        self.usuario = Mock(spec=ConfUsuario)
        self.usuario.usuario = 'test_user'
        
        # Mock del estado
        self.estado_matriculado = Mock(spec=GenrGeneral)
        self.estado_matriculado.nombre = 'MATRICULADO'
        
        self.estado_pendiente = Mock(spec=GenrGeneral)
        self.estado_pendiente.nombre = 'PENDIENTE'
        
        # Mock de la matriculación
        self.matricula = Mock(spec=MovMatriculacionEstudiante)
        self.matricula.id_estudiante = 1
        self.matricula.estado = self.estado_pendiente
        self.matricula.id_mov_anioelectivo_curso.id_mov_anioelectivo_curso = 1
    
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.GenrGeneral')
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.Mov_Aniolectivo_curso')
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.MovDetalleMateriaCurso')
    def test_matricular_estudiante_sin_materias(self, mock_detalle, mock_curso, mock_genr):
        """Test cuando el curso no tiene materias asignadas."""
        # Configurar mocks
        mock_genr.objects.filter.return_value.exists.return_value = True
        mock_curso.objects.get.return_value = Mock()
        mock_detalle.objects.filter.return_value.exists.return_value = False
        
        # Ejecutar
        exito, errores = MatriculacionService.matricular_estudiante(
            self.matricula, self.usuario
        )
        
        # Verificar
        self.assertFalse(exito)
        self.assertIn("no tiene materias asignadas", errores[0])
    
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.GenrGeneral')
    def test_matricular_estudiante_sin_quimestres(self, mock_genr):
        """Test cuando no hay quimestres configurados."""
        # Configurar mock
        mock_genr.objects.filter.return_value.exists.return_value = False
        
        # Ejecutar
        exito, errores = MatriculacionService.matricular_estudiante(
            self.matricula, self.usuario
        )
        
        # Verificar
        self.assertFalse(exito)
        self.assertIn("quimestres configurados", errores[0])
    
    def test_matricular_estudiante_ya_matriculado(self):
        """Test cuando el estudiante ya está matriculado."""
        # Configurar
        self.matricula.estado = self.estado_matriculado
        
        # Ejecutar
        exito, errores = MatriculacionService.matricular_estudiante(
            self.matricula, self.usuario
        )
        
        # Verificar
        self.assertTrue(exito)
        self.assertEqual(len(errores), 0)
    
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.Mov_Aniolectivo_curso')
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.MovDetalleMateriaCurso')
    @patch('sistemaAcademico.Apps.GestionAcademica.Services.matriculacion_service.Mov_Materia_profesor')
    def test_validar_cambio_estado_sin_profesor(self, mock_profesor, mock_detalle, mock_curso):
        """Test validación cuando hay materias sin profesor."""
        # Configurar mocks
        mock_curso.objects.get.return_value = Mock()
        
        materia_mock = Mock()
        materia_mock.__str__ = Mock(return_value='Matemáticas')
        mock_detalle.objects.filter.return_value = [materia_mock]
        mock_profesor.objects.filter.return_value.exists.return_value = False
        
        # Ejecutar
        es_valido, mensaje = MatriculacionService.validar_cambio_estado(
            self.matricula, self.estado_matriculado
        )
        
        # Verificar
        self.assertFalse(es_valido)
        self.assertIn("no tienen profesor asignado", mensaje)
