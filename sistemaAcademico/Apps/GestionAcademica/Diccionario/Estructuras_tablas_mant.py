from django.db import models

# from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_conf import ConfUsuario
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
# from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mov import MovDetalleEmpleado
from sistemaAcademico.Apps.Validaciones import (
    validate_cedula, validar_espacios, validate_celular, anio_lectivos,
)


class MantPersona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    identificacion = models.CharField(max_length=50, blank=False, null=False, validators=[validate_cedula])
    fecha_de_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True, validators=[validar_espacios])
    telefono = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True, validators=[validate_celular])
    id_genr_genero = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=False, null=True,
                                       related_name="genero", db_column='id_genr_genero')


    id_genr_pais = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True,
                                     db_column='id_genr_pais')
    id_genr_provincia = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="provincia",
                                          db_column='id_genr_provincia',blank=True, null=True)
    id_genr_ciudad = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="ciudad",
                                       db_column='id_genr_ciudad',blank=True, null=True)
    id_genr_tipo_sangre = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="tipo_de_sangre",
                                            db_column='id_genr_tipo_sangre',blank=True, null=True)
    id_genr_etnia = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE,blank=True, related_name="etnia",
                                      db_column='id_genr_etnia', null=True)
    id_genr_jornada = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="jornada",
                                        db_column='id_genr_jornada', null=True,blank=True)
    id_genr_indigena = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="indigena",
                                         db_column='id_genr_indigena',blank=True, null=True)
    id_genr_idioma_ancestral = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="acestral",
                                                 db_column='id_genr_idioma_ancestral',blank=True, null=True)
    id_genr_categoria_migratoria = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE,
                                                     related_name="categoria_migratoria",
                                                     db_column='id_genr_categoria_migratoria',blank=True, null=True)

    estado = models.ForeignKey(GenrGeneral, default=97, on_delete=models.CASCADE,
                               related_name="fk_persona_estado", db_column='estado')
    imagen = models.ImageField(upload_to='static/usuarios/', blank=False, null=True,
                               default='../../../static/img/texto-menu.pnguser_default_image.svg')
    id_genr_estado_civil = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name="estado_civil", db_column='id_genr_estado_civil')
    fecha_ingreso = models.DateTimeField(null=True, blank=False)
    usuario_ing = models.CharField(max_length=60, blank=False, null=False)
    terminal_ing = models.CharField(max_length=60, blank=False, null=False)

    discapacidad = models.BooleanField(blank=True, null=True)
    discapacidad_renal = models.BooleanField(blank=True, null=True)
    discapacidad_neurologica = models.BooleanField(blank=True, null=True)
    enfermedad_alergica = models.BooleanField(blank=True, null=True)
    asma = models.BooleanField(blank=True, null=True)
    epilepsia = models.BooleanField(blank=True, null=True)
    enfermedad_congenita = models.BooleanField(blank=True, null=True)
    enfermedad_respiratoria = models.BooleanField(blank=True, null=True)
    atencion_psicologica = models.BooleanField(blank=True, null=True)
    id_genr_tipo_usuario = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=False, null=False,
                                             default=19, related_name="persona_tipo_usuario",
                                             db_column='id_genr_tipo_usuario')

    pnombres = models.CharField(max_length=45, blank=True, null=True)
    papellidos = models.CharField(max_length=45, blank=True, null=True)
    pidentificacion = models.CharField(max_length=15, blank=True, null=True)
    pdireccion = models.CharField(max_length=45, blank=True, null=True, validators=[validar_espacios])
    ptelefono = models.CharField(max_length=45, blank=True, null=True)
    pvive_con_usted = models.BooleanField(blank=True, null=True)
    id_genr_estado_laboralp = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, related_name="estado_laboralp",
                                                db_column='id_genr_estado_laboralp', blank=True, null=True)
    mnombres = models.CharField(max_length=45, blank=True, null=True)
    mapellidos = models.CharField(max_length=45, blank=True, null=True)
    midentificacion = models.CharField(max_length=15, blank=True, null=True)
    mdireccion = models.CharField(max_length=45, blank=True, null=True)
    mtelefono = models.CharField(max_length=45, blank=True, null=True, validators=[validate_celular])
    mvive_con_usted = models.BooleanField(blank=True, null=True)
    id_genr_estado_laboralm = models.ForeignKey(GenrGeneral, blank=True, null=True, on_delete=models.CASCADE,
                                                related_name="estado_laboralm", db_column='id_genr_estado_laboralm')
    bono_solidario = models.BooleanField(blank=True, null=True)

    rnombres = models.CharField(max_length=45, blank=True, null=True)
    rapellidos = models.CharField(max_length=45, blank=True, null=True)
    rtelefono = models.CharField(max_length=45, blank=True, null=True, validators=[validate_celular])
    id_genr_tipo_identificacion = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE,
                                                    related_name="identificacion",
                                                    db_column='id_genr_tipo_identificacion', blank=True, null=True)
    ridentificacion = models.CharField(max_length=13, blank=True, null=True)
    tipo_parentesco = models.CharField(max_length=200, blank=True, null=True)
    rvive_con_usted = models.BooleanField(blank=True, null=True)
    rdireccion_trabajo = models.CharField(max_length=200, blank=True, null=True)
    rtelefono_trabajo = models.CharField(max_length=20, blank=True, null=True)
    rcorreo = models.EmailField(max_length=50, blank=True, null=True)
    rhorario_laboral = models.CharField(max_length=40, blank=True, null=True)
    mienbros_hogar = models.IntegerField(blank=True, null=True)



    #Segmento del reporte Datos del Estudiante NUEVOS CAMPOS AGREGADOS
    #estudiantes

    cod_alfnum = models.CharField(max_length=200 ,blank=True, null=True) #Campito para numerico

    edadEst=models.IntegerField(blank=True, null=True)
    sector = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="sector",
                                                 db_column='sector')#Seleccion
    referenciadeubicacion=models.CharField(max_length=200, blank=True, null=True)
    correo_elest=models.CharField(max_length=100, blank=True, null=True)
    nacionalidadEst = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="nacionalidad",
                                                 db_column='nacionalidadEst')#Seleccion
    plantel_procedenciaEst=models.CharField(max_length=150, blank=True, null=True)


    #Segmento del reporte Datos del Representante Legal
    #Representante
    fecha_nacimientoRe=models.DateField(blank=True, null=True)

    edadRe=models.IntegerField(blank=True, null=True)
    generoRe = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="GeneroRe",
                                                 db_column='generoRe')#Seleccion

    paisRe = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="paisRe",
                                                 db_column='paisRe')#Seleccion

    ciudadRe= models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="ciudadRe",
                                                 db_column='ciudadRe')#Seleccion
    direccionRe= models.CharField(max_length=200, blank=True, null=True)
    profesionRe= models.CharField(max_length=100, blank=True, null=True)#Dudad= Seleccion o Escribir
    lugardetrabajoRe= models.CharField(max_length=200, blank=True, null=True)

    #Segmento del reporte Datos de la Mama

    fecha_nacimientoMa = models.DateField(blank=True, null=True)
    edadMam = models.IntegerField(blank=True, null=True)
    generoMam = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="generoMam",
                                                 db_column='generoMam')#Seleccion
    paisMam = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="paisMam",
                                                 db_column='paisMam')#Seleccion
    ciudadMam = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="ciudadMam",
                                                 db_column='ciudadMam')#Seleccion
    correo_elMam=models.EmailField(max_length=50, blank=True, null=True)

    #Segmento del reporte Datos del papa
    fecha_nacimientoPap = models.DateField(blank=True, null=True)
    edadPap = models.IntegerField(blank=True, null=True)
    generoPap = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="generoPap",
                                                 db_column='generoPap')#Seleccion

    paisPap = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="paisPap",
                                                 db_column='paisPap')#Seleccion

    ciudadPap = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=True, null=True, related_name="ciudadPap",
                                                 db_column='ciudadPap')#Seleccion

    correo_elPap = models.EmailField(max_length=50, blank=True, null=True)








    class Meta:
        verbose_name = 'Persona',
        verbose_name_plural = 'Personas',
        db_table = 'mant_persona'

    def __str__(self):
        return self.nombres


class MantRepresentante(models.Model):
    id_representante = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(MantPersona, on_delete=models.CASCADE, blank=False, null=False,
                                   db_column='id_persona')
    usuario_ing = models.CharField(max_length=45, blank=False, null=False)
    fecha_ingreso = models.DateTimeField(blank=False, null=False)
    terminal_ing = models.CharField(max_length=45, blank=False, null=False)
    id_genr_nivel_formacion = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=False, null=False,
                                                db_column='id_genr_nivel_formacion')
    ingresos_totales = models.FloatField(blank=False, null=False)
    id_usuario = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Representante',
        verbose_name_plural = 'Representantes',
        db_table = 'mant_representante'

    def __str__(self):
        return self.id_persona.nombres, self.id_persona.apellidos


class MantEstudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(MantPersona, on_delete=models.CASCADE, blank=False, null=False,
                                   related_name="fk_estudiante_persona", db_column='id_persona')
    tipo_estudiante = models.CharField(max_length=45, blank=False, null=False)
    fecha_ingreso = models.DateTimeField(blank=False, null=True)
    usuario_ing = models.CharField(max_length=45, blank=False, null=False)
    terminal_ing = models.CharField(max_length=45, blank=False, null=False)

    class Meta:
        verbose_name = 'Estudiante',
        verbose_name_plural = 'Estudiantes',
        db_table = 'mant_estudiante'

    def __str__(self):
        return self.id_persona.nombres, self.id_persona.apellidos


class MantAnioLectivo(models.Model):
    id_anio_lectivo = models.AutoField(primary_key=True)
    anio = models.IntegerField(blank=False, null=False, unique=True)
    ciclo = models.IntegerField(blank=False, null=False, unique=True)
    fecha_incio_ciclo = models.DateField(blank=False, null=False)
    fecha_fin_ciclo = models.DateField(blank=False, null=False)
    id_genr_estado = models.ForeignKey(GenrGeneral, on_delete=models.CASCADE, blank=False, null=False,
                                       related_name="fk_aniolectivo_estado", db_column='id_genr_estado',
                                       validators=[anio_lectivos])

    class Meta:
        verbose_name = 'Año lectivo',
        verbose_name_plural = 'Año lectivo',
        db_table = 'mant_anio_lectivo'

    def __str__(self):
        return str(self.anio)


class MantEmpleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(MantPersona, on_delete=models.CASCADE, blank=False, null=False,
                                   related_name="fk_empleado_persona", db_column='id_persona')
    # id_detalle_empleado = models.ForeignKey('MovDetalleEmpleado', on_delete=models.CASCADE, blank=False, null=False,

    #                                     related_name="fk_empleado_detalle", db_column='id_detalle_empleado')
    id_anio_lectivo = models.ForeignKey(MantAnioLectivo, on_delete=models.CASCADE, blank=False, null=False,

                                        related_name="fk_empleado_anio_lectivo", db_column='id_anio_lectivo')
    id_usuario = models.ForeignKey('ConfUsuario', on_delete=models.CASCADE, blank=False, null=True,
                                   related_name="fk_empleado_usuario", db_column='id_usuario')

    fecha_ingreso = models.DateTimeField(blank=False, null=True)
    usuario_ing = models.CharField(max_length=45, blank=False, null=False)
    terminal_ing = models.CharField(max_length=45, blank=False, null=False)

    class Meta:
        verbose_name = 'Empleado',
        verbose_name_plural = 'Empleados',
        db_table = 'mant_empleado'

    def __str__(self):
        return self.id_persona.nombres + " " + self.id_persona.apellidos
