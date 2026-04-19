"""
Comando para verificar campos DateTimeField que puedan tener valores como strings.
Uso: python manage.py check_datetime_fields
"""
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
import datetime


class Command(BaseCommand):
    help = 'Verifica campos DateTimeField que puedan tener valores como strings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Intenta corregir los valores encontrados',
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']
        
        self.stdout.write(self.style.SUCCESS('Verificando campos DateTimeField...'))
        
        # Obtener todos los modelos de la app GestionAcademica
        app_config = apps.get_app_config('GestionAcademica')
        models_to_check = app_config.get_models()
        
        total_issues = 0
        total_fixed = 0
        
        for model in models_to_check:
            # Obtener campos DateTimeField y DateField
            datetime_fields = [
                field for field in model._meta.get_fields()
                if isinstance(field, (models.DateTimeField, models.DateField))
                and not field.auto_now and not field.auto_now_add
            ]
            
            if not datetime_fields:
                continue
            
            model_name = f"{model._meta.app_label}.{model._meta.object_name}"
            
            try:
                # Verificar algunos registros
                sample_size = min(100, model.objects.count())
                if sample_size == 0:
                    continue
                
                records = model.objects.all()[:sample_size]
                
                for record in records:
                    for field in datetime_fields:
                        value = getattr(record, field.name)
                        
                        # Verificar si el valor es string
                        if value is not None and isinstance(value, str):
                            total_issues += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  ⚠ {model_name}.{field.name} (ID: {record.pk}): '
                                    f'valor es string "{value}"'
                                )
                            )
                            
                            if fix_mode:
                                # Intentar convertir
                                try:
                                    # Manejar casos especiales de MySQL
                                    if value in ('0000-00-00', '0000-00-00 00:00:00', '0000-00-00 00:00:00.000000'):
                                        # Establecer como None (NULL en BD)
                                        setattr(record, field.name, None)
                                        record.save(update_fields=[field.name])
                                        total_fixed += 1
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f'    ✓ Corregido a NULL (valor inválido de MySQL)'
                                            )
                                        )
                                        continue
                                    
                                    if isinstance(field, models.DateTimeField):
                                        formats = [
                                            '%Y-%m-%d %H:%M:%S',
                                            '%Y-%m-%d %H:%M:%S.%f',
                                            '%Y-%m-%d',
                                        ]
                                        converted = None
                                        for fmt in formats:
                                            try:
                                                converted = datetime.datetime.strptime(value, fmt)
                                                break
                                            except ValueError:
                                                continue
                                        
                                        if converted:
                                            setattr(record, field.name, converted)
                                            record.save(update_fields=[field.name])
                                            total_fixed += 1
                                            self.stdout.write(
                                                self.style.SUCCESS(
                                                    f'    ✓ Corregido a {converted}'
                                                )
                                            )
                                    
                                    elif isinstance(field, models.DateField):
                                        converted = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                                        setattr(record, field.name, converted)
                                        record.save(update_fields=[field.name])
                                        total_fixed += 1
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f'    ✓ Corregido a {converted}'
                                            )
                                        )
                                
                                except Exception as e:
                                    self.stdout.write(
                                        self.style.ERROR(
                                            f'    ✗ Error al corregir: {e}'
                                        )
                                    )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error al verificar {model_name}: {e}'
                    )
                )
        
        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('RESUMEN'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if total_issues == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    '✓ No se encontraron problemas con campos DateTimeField'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Se encontraron {total_issues} campos con valores como string'
                )
            )
            
            if fix_mode:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Se corrigieron {total_fixed} de {total_issues} campos'
                    )
                )
                if total_fixed < total_issues:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠ {total_issues - total_fixed} campos no pudieron ser corregidos'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        'Ejecuta con --fix para intentar corregir los valores'
                    )
                )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'Nota: Los conversores personalizados en __init__.py '
                'ahora manejan automáticamente la conversión de strings a datetime'
            )
        )
