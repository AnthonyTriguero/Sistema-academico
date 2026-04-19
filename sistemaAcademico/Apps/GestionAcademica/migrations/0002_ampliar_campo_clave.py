"""
Migración para ampliar el campo 'clave' de 45 a 256 caracteres.
Necesario para soportar hashes PBKDF2 (reemplazo de SHA1).
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionAcademica', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confusuario',
            name='clave',
            field=models.CharField(max_length=256, blank=False, null=False),
        ),
        migrations.AlterField(
            model_name='usuariotemp',
            name='clave',
            field=models.CharField(max_length=256, blank=False, null=False),
        ),
    ]
