from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_codigo(value):
    if not value or value.strip() == "":
        raise ValidationError(
            _('No se puede crear un modulo sin codigo. Por favor ingrese uno'))
    return value


def longitud(value):
    if len(value) < 6:
        raise ValidationError('El nombre de usuario debe contener al menos 6 caracteres')
    elif len(value) > 12:
        raise ValidationError('El nombre de usuario debe contener maximo 12 caracteres')
    return value


def alfanumerico(value):
    if not value.isalnum():
        raise ValidationError('El nombre de usuario puede contener solo letras y numeros')
    return value


def validate_nombre(value):
    if not value or value.strip() == "":
        raise ValidationError(
            _('%(value)s: El nombre no puede estar vacío'),
            code="invalid",
            params={'value': value},
        )
    return value


def validar_espacios(value):
    if not value or value.strip() == "":
        raise ValidationError(
            _('Este campo no puede estar vacío'),
            code="invalid",
        )
    return value


def longitudPassword(value):
    if len(value) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres')
    elif len(value) > 15:
        raise ValidationError('La contraseña debe tener maximo 15 caracteres')
    return value


def minuscula(value):
    if not any(c.islower() for c in value):
        raise ValidationError('La contraseña debe tener al menos una minuscula')
    return value


def mayuscula(value):
    if not any(c.isupper() for c in value):
        raise ValidationError('La contraseña debe tener al menos una mayuscula')
    return value


def numero(value):
    if not any(c.isdigit() for c in value):
        raise ValidationError('La contraseña debe tener al menos un numero')
    return value


def espacios(value):
    if ' ' in value:
        raise ValidationError('La contraseña no puede contener espacios en blanco')
    return value


def espaciosusu(value):
    if ' ' in value:
        raise ValidationError('El usuario no puede contener espacios en blanco')
    return value


def alfanumericoPassword(value):
    if not value.isalnum():
        raise ValidationError('La contraseña puede contener solo letras y numeros')
    return value


def validate_descripcion(value):
    if not value or value.strip() == "":
        raise ValidationError(
            _('No se puede crear un menu sin un nombre. Por favor ingrese uno'))
    return value


def validate_cedula(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError(
            _('%(value)s no es una cédula válida'),
            code="invalid",
            params={'value': value},
        )
    else:
        impares = int(value[1]) + int(value[3]) + int(value[5]) + int(value[7])
        pares = 0
        for i in range(0, 9):
            if i % 2 == 0:
                res = int(value[i]) * 2
                if res >= 10:
                    res = res - 9
                pares = pares + res
        total = impares + pares
        dig_validador = (((total + 10) // 10) * 10) - total
        if dig_validador == 10:
            dig_validador = 0
        if not (1 <= int(value[0:2]) <= 24 and int(value[-1]) == dig_validador):
            raise ValidationError(
                _('%(value)s no es una cédula válida'),
                code="invalid",
                params={'value': value},
            )


def ruc_natural(value):
    impares = int(value[1]) + int(value[3]) + int(value[5]) + int(value[7])
    pares = 0
    for i in range(0, 9):
        if i % 2 == 0:
            res = int(value[i]) * 2
            if res >= 10:
                res = res - 9
            pares = pares + res
    total = impares + pares
    dig_validador = (((total + 10) // 10) * 10) - total
    if dig_validador == 10:
        dig_validador = 0
    return 1 <= int(value[0:2]) <= 24 and int(value[9]) == dig_validador and int(value[10:13]) >= 1


def ruc_juridica(value):
    coefs = [4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(value[i]) * coefs[i] for i in range(9))
    dig_validador = 0
    residuo = total % 11
    if residuo != 0:
        dig_validador = 11 - residuo
    return 1 <= int(value[0:2]) <= 24 and int(value[2]) == 9 and int(value[9]) == dig_validador and int(value[10:13]) >= 1


def ruc_publica(value):
    coefs = [3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(value[i]) * coefs[i] for i in range(8))
    dig_validador = 0
    residuo = total % 11
    if residuo != 0:
        dig_validador = 11 - residuo
    return 1 <= int(value[0:2]) <= 24 and int(value[2]) == 6 and int(value[8]) == dig_validador and int(value[9:13]) >= 1


def validate_ruc(value):
    if not value.isdigit() or len(value) != 13:
        raise ValidationError(
            _('%(value)s no es un RUC válido'),
            code="invalid",
            params={'value': value},
        )
    if not (ruc_natural(value) or ruc_juridica(value) or ruc_publica(value)):
        raise ValidationError(
            _('%(value)s no es un RUC válido'),
            code="invalid",
            params={'value': value},
        )


def validate_letras(value):
    if not value.replace(' ', '').isalpha():
        raise ValidationError(
            _('%(value)s no contiene únicamente letras'),
            code="invalid",
            params={'value': value},
        )


def validate_fono_convencional(value):
    if not value.isdigit() or len(value) not in (7, 9):
        raise ValidationError(
            _('%(value)s no es un teléfono convencional correcto'),
            code="invalid",
            params={'value': value},
        )


def validate_celular(value):
    if not value.isdigit() or len(value) < 10:
        raise ValidationError(
            _('%(value)s no es un celular correcto'),
            code="invalid",
            params={'value': value},
        )


def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s no es un numero positivo'),
            code="invalid",
            params={'value': value},
        )


class usuario_validar():
    def __init__(self):
        self.errors = []

    def longitud(self, username):
        if len(username) < 6:
            self.errors.append('El nombre de usuario debe contener al menos 6 caracteres')
            return False
        elif len(username) > 12:
            self.errors.append('El nombre de usuario debe contener maximo 12 caracteres')
            return False
        return True

    def alfanumerico(self, username):
        if not username.isalnum():
            self.errors.append('El nombre de usuario puede contener solo letras y numeros')
            return False
        return True

    def validar_usuario(self, username):
        return self.longitud(username) and self.alfanumerico(username)


def pasaporte(value):
    if not value.isalnum():
        raise ValidationError(
            _('%(value)s no es un pasaporte correcto'),
            code="invalid",
            params={'value': value},
        )
    return True


def identificar(value):
    if len(value) == 10:
        validate_cedula(value)
    elif len(value) == 13:
        validate_ruc(value)
    elif value.isalnum():
        pasaporte(value)
    else:
        raise ValidationError(
            _('%(value)s no es una identificacion correcta'),
            code="invalid",
            params={'value': value},
        )


def validar_anio(value):
    """Validador placeholder - implementar lógica de negocio real."""
    return value


def validar_ciclo(value):
    """Validador placeholder - implementar lógica de negocio real."""
    return value


def validate_vacios(value):
    if not value or value.strip() == "":
        raise ValidationError(
            _('Este campo no puede estar vacío'),
            code="invalid",
        )
    return value


def validar_select(value):
    """Validador de selección - verificar que se haya seleccionado una opción válida."""
    return value


def validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    else:
        return False

    for i in range(len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver


def anio_lectivos(value):
    from sistemaAcademico.Apps.GestionAcademica.Diccionario.Estructuras_tablas_mant import MantAnioLectivo
    queryset = MantAnioLectivo.objects.filter(id_genr_estado=97)
    if queryset.exists() and value == 97:
        raise ValidationError('No se puede ingresar otro año lectivo mientras otro aun este activo')
    return value
