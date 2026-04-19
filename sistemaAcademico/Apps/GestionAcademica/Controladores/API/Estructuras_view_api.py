import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfMenu, ConfEmpresa, ConfUsuario
from sistemaAcademico.Apps.GestionAcademica.Serializers.Configuracion.serializers import menuSerializers
from django.db.models import Q

logger = logging.getLogger(__name__)


class Menu_api(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            descripcion = request.data.get('descripcion', '')
            url = request.data.get('url', '')
            lazyname = request.data.get('lazyname', '')
            view = request.data.get('view', '')
            name = request.data.get('name', '')

            queryset = ConfMenu.objects.filter(
                Q(descripcion__contains=descripcion)
                & Q(url=url)
                & Q(view=view)
                & Q(lazy_name=lazyname)
                & Q(name=name)
                & Q(id_genr_estado=97)
            )

            serializacion = menuSerializers(queryset, many=True)
            if queryset.exists():
                return Response(data=serializacion.data, status=status.HTTP_226_IM_USED)
            return Response(data=serializacion.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en Menu_api: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Unidad_Edu(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            nombre = request.data.get('nombre', '')
            razon_social = request.data.get('razon_social', '')
            correo = request.data.get('correo', '')
            identificacion = request.data.get('identificacion', '')

            queryset = ConfEmpresa.objects.filter(
                Q(nombre=nombre)
                | Q(razon_social=razon_social)
                | Q(correo=correo)
                & Q(identificacion=identificacion)
            )

            serializacion = menuSerializers(queryset, many=True)
            if queryset.exists():
                return Response(data=serializacion.data, status=status.HTTP_226_IM_USED)
            return Response(data=serializacion.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en Unidad_Edu: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Usuario(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            usuario = request.data.get('usuario', '')
            queryset = ConfUsuario.objects.filter(Q(usuario=usuario))

            serializacion = menuSerializers(queryset, many=True)
            if queryset.exists():
                return Response(data=serializacion.data, status=status.HTTP_226_IM_USED)
            return Response(data=serializacion.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en Usuario API: {e}")
            return Response(
                {'error': 'Error interno del servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
