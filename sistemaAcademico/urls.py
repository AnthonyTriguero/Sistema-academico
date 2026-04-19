"""sistemaAcademico URL Configuration"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views import static
from sistemaAcademico.Apps.GestionAcademica.views import Error404, handler_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('sistemaAcademico.Apps.GestionAcademica.urls', 'Academico'))),
]

# Debug toolbar solo en desarrollo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', static.serve,
            {'document_root': settings.STATIC_ROOT}, name='static'),
    ]

# Error handlers
handler404 = Error404.as_view()
handler500 = handler_500

# Media files
from django.contrib.staticfiles.urls import static as static_url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static_url(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
