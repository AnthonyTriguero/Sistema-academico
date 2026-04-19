from django.db import models
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_genr import GenrGeneral
from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantPersona
from sistemaAcademico.Apps.Validaciones import *


class ConfEmpresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=False,
                              unique=True, null=False,validators=[validate_nombre])
    razon_social = models.CharField(
        max_length=200, blank=False, null=False, validators=[validar_espacios])
    id_genr_tipo_identificacion = models.ForeignKey(
        GenrGeneral, blank=False,null=False, on_delete=models.CASCADE, db_column='id_genr_tipo_identificacion', validators=[validar_select])
    identificacion = models.CharField(unique=True, max_length=50, blank=False, null=False,validators=[identificar,espacios])
    direccion = models.CharField(
        max_length=50, blank=False, null=False,validators=[validar_espacios])
    representante_legal = models.CharField(
        max_length=50, blank=False, null=False,validators=[validar_espacios])
    correo = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(
        max_length=10, blank=False, null=False, validators=[validate_celular])
    fecha_creacion = models.DateField(blank=True, null=True)

    # related_name='estado El atributo related_name especifica el nombre de la relación inversa del modelo de usuario a su modelo.
    # si hay mas de dos claves foraneas que referencian a la misma tabla se debe usar related_name'
    id_genr_estado = models.ForeignKey(
        GenrGeneral, on_delete=models.CASCADE, default=97, related_name='estado_empresa', db_column='estado')
    # ------------------------------------------------------------------------------------------------------------------------

    fecha_ingreso = models.DateField(blank=True, null=True, )
    usuario_ing = models.CharField(max_length=45, blank=True, null=True)
    terminal_ing = models.CharField(max_length=45, blank=True, null=True)


    class Meta:
        verbose_name = 'Empresa',
        verbose_name_plural = 'Empresas',
        db_table = 'conf_empresa'


    def __str__(self):
        return self.nombre


class ConfModulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, validators=[
                              validate_codigo], unique=True)
    nombre = models.CharField(blank=False, validators=[
                              validate_nombre], null=False, max_length=25, unique=True)
    id_genr_estado = models.ForeignKey(
        GenrGeneral, on_delete=models.CASCADE, default=97, db_column='id_genr_estado')

    class Meta:
        verbose_name = 'Modulo',
        verbose_name_plural = 'Modulos',
        db_table = 'conf_modulo'

    def __str__(self):
        return self.nombre, self.codigo

    def __unicode__(self):
        return self.id_modulo, self.id_genr_estado

    def get_absolute(self):
        return reversed('modulo-detal', kwargs={'pk': self.id_modulo})


class ConfRol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, blank=False, null=False)
    nombre = models.CharField(max_length=45, blank=False, null=False)
    id_genr_estado = models.ForeignKey(
        GenrGeneral, default=97, on_delete=models.CASCADE, blank=False, null=False, db_column='id_genr_estado')

    class Meta:
        verbose_name = 'Rol',
        verbose_name_plural = 'Roles',
        db_table = 'conf_rol'

    def __str__(self):
        return self.nombre
    
    def __unicode__(self):
        return self.id_rol


class ConfMenu(models.Model):
    ICONO_CHOICES = [
        ('fas fa-fw fa-cog', 'Icono Configuraciones'),
        ('fas fa-fw fa-wrench', 'Icono Reportes Especiales'),
        ('fas fa-fw fa-chart-area', 'Icono Registor Notas'),
        ('fas fa-fw fa-table', 'Icono Matricula'),
        ('fas fa-fw fa-folder', 'Icono Admisiones'),
        ('#', 'Ninguno')
    ]
    id_menu = models.AutoField(primary_key=True)
    id_padre = models.IntegerField(blank=False, null=False)
    orden = models.IntegerField(blank=True, default=0)
    descripcion = models.CharField(max_length=45, blank=True, validators=[
                                   validate_descripcion], unique=True, null=True, db_column='descripcion')
    id_genr_estado = models.ForeignKey(
        GenrGeneral, on_delete=models.CASCADE, default=97, db_column='id_genr_estado')
    url = models.CharField(blank=False, null=False, max_length=60)
    icono = models.CharField(max_length=50, blank=False,
                             choices=ICONO_CHOICES, null=False)
    lazy_name = models.CharField(max_length=60, blank=False)
    name = models.CharField(max_length=60, blank=False)
    view = models.CharField(max_length=45, blank=False, null=False)

    class Meta:
        verbose_name = 'Menu',
        verbose_name_plural = 'Menu',
        db_table = 'conf_menu'
        ordering = ['orden']

    def __str__(self):
        return self.descripcion 

    def __int__(self):
        return self.orden, self.id_padre
    
    def __unicode__(self):
        return self.id_menu




class ConfUsuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=45, unique=True, blank=False, null=False, validators=[
                               validate_nombre, longitud, alfanumerico, espaciosusu])
    clave = models.CharField(max_length=256, blank=False, null=False, validators=[
                             longitudPassword, minuscula, mayuscula, numero, espacios, alfanumericoPassword])
    id_persona = models.ForeignKey(
        MantPersona, on_delete=models.CASCADE, db_column='id_persona')
    id_genr_tipo_usuario = models.ForeignKey(
        GenrGeneral, on_delete=models.CASCADE, related_name="fk_usuario_tipo_usuario", db_column='id_genr_tipo_usuario')
    id_genr_estado = models.ForeignKey(GenrGeneral, default=97, on_delete=models.CASCADE,
                                       related_name="fk_usuario_estado", db_column='id_genr_estado')
    id_rol= models.ManyToManyField(ConfRol, db_table="conf_usuario_rol",related_name="fk_rol",)

    class Meta:
        verbose_name = 'Usuario',
        verbose_name_plural = 'Usuarios',
        db_table = 'conf_usuario'

    def __str__(self):
        return self.usuario


class ConfModulo_menu(models.Model):
    id_modulo_menu = models.AutoField(primary_key=True)
    id_modulo = models.ForeignKey(
        ConfModulo, on_delete=models.CASCADE, related_name="fk_modmen_modulo", db_column='id_modulo')
    id_menu = models.ForeignKey(
        ConfMenu, on_delete=models.CASCADE, related_name="fk_modmen_menu", db_column='id_menu')
    id_genr_estado = models.ForeignKey(
        GenrGeneral, on_delete=models.CASCADE, db_column='id_genr_estado', default='97')

    class Meta:
        verbose_name = 'Modulo_Menu'
        verbose_name_plural = 'Modulos_Menus'
        db_table = 'conf_modulo_menu'

    def __unicode__(self):
        return self.id_modulo_menu, self.id_menu, self.id_modulo, self.id_genr_estado


class ConfAccion(models.Model):
    ACCIONES_CHOICES = [
        ('Agregar', 'Agregar Registros'),
        ('Editar', 'Editar Registros'),
        ('Eliminar', 'Eliminar Registros'),
        ('Imprimir', 'Imprimir Registros'),
    ]

    id_accion = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(ConfRol,on_delete=models.CASCADE,db_column='rol',default=1)
    descripcion = models.CharField(max_length=50,choices=ACCIONES_CHOICES,blank=False,null=False)
    id_menu = models.ManyToManyField(ConfMenu,db_table='conf_accion_menu')

    class Meta:
        verbose_name = 'Accion'
        verbose_name_plural = 'Acciones'
        db_table = 'conf_accion'
        
    
    def __str__(self):
        return self.descripcion



class UsuarioTemp(models.Model):
    id_usuario_temp = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=45, unique=True, blank=False, null=False, validators=[
                               validate_nombre,])
    clave = models.CharField(max_length=256, blank=False, null=False, validators=[
                               numero, espacios, ])
    fecha_limite = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateField(
        blank=True, null=True, auto_now=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    id_rol= models.ForeignKey(ConfRol,db_column='id_rol',related_name="fk_usuario_temp",default=8,on_delete=models.CASCADE)
    id_persona = models.ForeignKey(MantPersona,db_column="id_persona",related_name='fk_persona_usuario_tem',null=True,blank=False,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Usuario_temp'
        verbose_name_plural = 'Usuarios_temps'
        db_table = 'conf_usuarios_temp'

    def __str__(self):
        return self.usuario, self.correo

    def __unicode__(self):
        return self.id_usuario_temp


class ConfPermiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    menu = models.ManyToManyField(
        ConfMenu, related_name="fk_permiso_modmenu", db_table='conf_permiso_menu')
    id_rol = models.ForeignKey(ConfRol, on_delete=models.CASCADE,
                               related_name="fk_permiso_rol", db_column='id_rol',blank=False, null=False)
    class Meta:
        verbose_name = 'Permiso',
        verbose_name_plural = 'Permisos',
        db_table = 'conf_permiso'
    

    def __unicode__(self):
        return self.id_rol,self.acciones

         

"""
class ConfDetallePermiso(models.Model):
    id_detalle_permiso = models.AutoField(primary_key=True)
    id_permiso = models.ForeignKey(ConfPermiso, on_delete=models.CASCADE,
                                   related_name="fk_det_permiso_cab_permiso", db_column='id_permiso')
    id_menu = models.ForeignKey(ConfMenu, on_delete=models.CASCADE,
                                related_name="fk_det_permiso_menu", db_column='id_menu')
    id_accion = models.ForeignKey(ConfAccion, on_delete=models.CASCADE,
                                  related_name="fk_det_permiso_accion", db_column='id_accion')
    id_genr_estado = models.ForeignKey(
        GenrGeneral, default=97, on_delete=models.CASCADE, db_column='id_genr_estado')

    class Meta:
        verbose_name = 'Detalle Permiso',
        verbose_name_plural = 'Detalle Permisos',
        db_table = 'conf_detalle_permiso'

    def __int__(self):
        return self.id_detalle_permiso

    def __unicode__(self):
        return self.id_menu, self.id_permiso, self.id_accion

"""
class ConfCorreosSmpt(models.Model):
    id_correos_smpt = models.AutoField(primary_key=True)
    ssl = models.CharField(max_length=30, blank=False, null=False,default='True')
    dominio = models.CharField(max_length=30, blank=False, null=False)
    puerto = models.CharField(max_length=20, blank=False, null=False)
    usuario_c = models.CharField(
        max_length=100, blank=False, null=False, unique=True)
    contrasenia_c = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    id_genr_estado = models.ForeignKey(GenrGeneral, default=97, on_delete=models.CASCADE,
                                       db_column='id_genr_estado')

    class Meta:
        verbose_name = 'Correos Smpt',
        verbose_name_plural = 'Correos Smpt',
        db_table = 'conf_correos_smpt'

    def __int__(self):
        return self.id_correos_smpt

    def __str__(self):
        return self.usuario_c, self.contrasenia_c
