"""
Middleware de autenticación centralizado.
Reemplaza las verificaciones manuales de sesión en cada vista.
"""
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)

# URLs que no requieren autenticación
URLS_PUBLICAS = [
    '',           # login
    'timeout/',
]


class AuthenticationMiddleware:
    """
    Verifica que el usuario tenga sesión activa.
    Redirige a timeout/ si no está autenticado.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lstrip('/')

        # Permitir acceso a URLs públicas, admin, static y media
        es_publica = (
            path in URLS_PUBLICAS
            or path.startswith('admin/')
            or path.startswith('static/')
            or path.startswith('media/')
            or path.startswith('__debug__/')
        )

        if not es_publica and 'usuario' not in request.session:
            logger.warning(f"Acceso no autorizado a /{path}")
            return HttpResponseRedirect('/timeout/')

        response = self.get_response(request)
        return response
