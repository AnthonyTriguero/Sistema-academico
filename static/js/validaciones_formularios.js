/**
 * Sistema de Validación de Formularios - Client Side
 * Validación en tiempo real con feedback visual
 */

(function($) {
    'use strict';

    // Configuración de validaciones
    const validaciones = {
        required: {
            test: (value) => value.trim() !== '',
            mensaje: 'Este campo es obligatorio'
        },
        email: {
            test: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
            mensaje: 'Ingrese un email válido'
        },
        minLength: {
            test: (value, min) => value.length >= min,
            mensaje: (min) => `Mínimo ${min} caracteres`
        },
        maxLength: {
            test: (value, max) => value.length <= max,
            mensaje: (max) => `Máximo ${max} caracteres`
        },
        numeric: {
            test: (value) => /^\d+$/.test(value),
            mensaje: 'Solo se permiten números'
        },
        alphanumeric: {
            test: (value) => /^[a-zA-Z0-9\s]+$/.test(value),
            mensaje: 'Solo letras y números'
        },
        phone: {
            test: (value) => /^[0-9]{10}$/.test(value.replace(/[\s\-\(\)]/g, '')),
            mensaje: 'Ingrese un teléfono válido (10 dígitos)'
        },
        cedula: {
            test: (value) => {
                // Validación básica de cédula ecuatoriana
                if (!/^\d{10}$/.test(value)) return false;
                
                const digitos = value.split('').map(Number);
                const provincia = parseInt(value.substring(0, 2));
                
                if (provincia < 1 || provincia > 24) return false;
                
                const coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2];
                let suma = 0;
                
                for (let i = 0; i < 9; i++) {
                    let valor = digitos[i] * coeficientes[i];
                    if (valor > 9) valor -= 9;
                    suma += valor;
                }
                
                const digitoVerificador = suma % 10 === 0 ? 0 : 10 - (suma % 10);
                return digitoVerificador === digitos[9];
            },
            mensaje: 'Cédula ecuatoriana inválida'
        },
        password: {
            test: (value) => value.length >= 8 && /[A-Z]/.test(value) && /[a-z]/.test(value) && /[0-9]/.test(value),
            mensaje: 'Mínimo 8 caracteres, incluir mayúsculas, minúsculas y números'
        },
        passwordMatch: {
            test: (value, matchField) => value === $(matchField).val(),
            mensaje: 'Las contraseñas no coinciden'
        },
        date: {
            test: (value) => {
                if (!value) return false;
                const date = new Date(value);
                return date instanceof Date && !isNaN(date);
            },
            mensaje: 'Fecha inválida'
        },
        dateRange: {
            test: (value, min, max) => {
                const date = new Date(value);
                const minDate = min ? new Date(min) : null;
                const maxDate = max ? new Date(max) : null;
                
                if (minDate && date < minDate) return false;
                if (maxDate && date > maxDate) return false;
                return true;
            },
            mensaje: (min, max) => {
                if (min && max) return `Fecha debe estar entre ${min} y ${max}`;
                if (min) return `Fecha debe ser posterior a ${min}`;
                if (max) return `Fecha debe ser anterior a ${max}`;
            }
        },
        url: {
            test: (value) => /^https?:\/\/.+\..+/.test(value),
            mensaje: 'URL inválida'
        },
        positiveNumber: {
            test: (value) => !isNaN(value) && parseFloat(value) > 0,
            mensaje: 'Debe ser un número positivo'
        },
        range: {
            test: (value, min, max) => {
                const num = parseFloat(value);
                return !isNaN(num) && num >= min && num <= max;
            },
            mensaje: (min, max) => `Valor debe estar entre ${min} y ${max}`
        }
    };

    // Clase principal de validación
    class FormValidator {
        constructor(formSelector, options = {}) {
            this.$form = $(formSelector);
            this.options = $.extend({
                validateOnBlur: true,
                validateOnInput: true,
                showSuccessIcon: true,
                scrollToError: true,
                submitButton: 'button[type="submit"]',
                onSuccess: null,
                onError: null
            }, options);
            
            this.init();
        }

        init() {
            const self = this;
            
            // Prevenir submit por defecto
            this.$form.on('submit', function(e) {
                if (!self.validateForm()) {
                    e.preventDefault();
                    
                    if (self.options.scrollToError) {
                        self.scrollToFirstError();
                    }
                    
                    if (self.options.onError) {
                        self.options.onError();
                    }
                    
                    return false;
                }
                
                if (self.options.onSuccess) {
                    self.options.onSuccess();
                }
            });

            // Validación en blur
            if (this.options.validateOnBlur) {
                this.$form.find('input, select, textarea').on('blur', function() {
                    self.validateField($(this));
                });
            }

            // Validación en input (tiempo real)
            if (this.options.validateOnInput) {
                this.$form.find('input, textarea').on('input', function() {
                    const $field = $(this);
                    if ($field.hasClass('is-invalid') || $field.hasClass('is-valid')) {
                        self.validateField($field);
                    }
                });
            }

            // Limpiar validación al cambiar select
            this.$form.find('select').on('change', function() {
                self.validateField($(this));
            });
        }

        validateField($field) {
            const rules = this.getFieldRules($field);
            const value = $field.val();
            let isValid = true;
            let errorMessage = '';

            // Validar cada regla
            for (const rule of rules) {
                const validation = validaciones[rule.type];
                if (!validation) continue;

                let testResult;
                if (rule.params) {
                    testResult = validation.test(value, ...rule.params);
                } else {
                    testResult = validation.test(value);
                }

                if (!testResult) {
                    isValid = false;
                    if (typeof validation.mensaje === 'function') {
                        errorMessage = validation.mensaje(...(rule.params || []));
                    } else {
                        errorMessage = validation.mensaje;
                    }
                    break;
                }
            }

            this.showFieldFeedback($field, isValid, errorMessage);
            return isValid;
        }

        getFieldRules($field) {
            const rules = [];
            
            // Required
            if ($field.prop('required') || $field.data('required')) {
                rules.push({ type: 'required' });
            }

            // Email
            if ($field.attr('type') === 'email' || $field.data('validate') === 'email') {
                rules.push({ type: 'email' });
            }

            // Numeric
            if ($field.attr('type') === 'number' || $field.data('validate') === 'numeric') {
                rules.push({ type: 'numeric' });
            }

            // Phone
            if ($field.data('validate') === 'phone') {
                rules.push({ type: 'phone' });
            }

            // Cedula
            if ($field.data('validate') === 'cedula') {
                rules.push({ type: 'cedula' });
            }

            // Password
            if ($field.attr('type') === 'password' && $field.data('validate') === 'password') {
                rules.push({ type: 'password' });
            }

            // Password Match
            if ($field.data('validate') === 'password-match') {
                rules.push({ 
                    type: 'passwordMatch', 
                    params: [$field.data('match')] 
                });
            }

            // Min Length
            if ($field.attr('minlength') || $field.data('minlength')) {
                const min = parseInt($field.attr('minlength') || $field.data('minlength'));
                rules.push({ type: 'minLength', params: [min] });
            }

            // Max Length
            if ($field.attr('maxlength') || $field.data('maxlength')) {
                const max = parseInt($field.attr('maxlength') || $field.data('maxlength'));
                rules.push({ type: 'maxLength', params: [max] });
            }

            // Date
            if ($field.attr('type') === 'date') {
                rules.push({ type: 'date' });
            }

            // Range
            if ($field.data('validate') === 'range') {
                const min = parseFloat($field.data('min'));
                const max = parseFloat($field.data('max'));
                rules.push({ type: 'range', params: [min, max] });
            }

            // Positive Number
            if ($field.data('validate') === 'positive') {
                rules.push({ type: 'positiveNumber' });
            }

            return rules;
        }

        showFieldFeedback($field, isValid, errorMessage) {
            // Remover clases anteriores
            $field.removeClass('is-valid is-invalid');
            
            // Remover feedback anterior
            $field.siblings('.valid-feedback, .invalid-feedback').remove();

            if (isValid) {
                $field.addClass('is-valid');
                if (this.options.showSuccessIcon) {
                    $field.after('<div class="valid-feedback d-block"><i class="fas fa-check-circle"></i> Correcto</div>');
                }
            } else {
                $field.addClass('is-invalid');
                $field.after(`<div class="invalid-feedback d-block"><i class="fas fa-exclamation-circle"></i> ${errorMessage}</div>`);
            }
        }

        validateForm() {
            let isValid = true;
            const self = this;

            this.$form.find('input, select, textarea').each(function() {
                const $field = $(this);
                
                // Saltar campos ocultos o deshabilitados
                if ($field.is(':hidden') || $field.is(':disabled')) {
                    return;
                }

                if (!self.validateField($field)) {
                    isValid = false;
                }
            });

            return isValid;
        }

        scrollToFirstError() {
            const $firstError = this.$form.find('.is-invalid').first();
            if ($firstError.length) {
                $('html, body').animate({
                    scrollTop: $firstError.offset().top - 100
                }, 300);
                $firstError.focus();
            }
        }

        reset() {
            this.$form[0].reset();
            this.$form.find('.is-valid, .is-invalid').removeClass('is-valid is-invalid');
            this.$form.find('.valid-feedback, .invalid-feedback').remove();
        }
    }

    // Exponer al objeto global
    window.FormValidator = FormValidator;

    // Auto-inicializar formularios con clase .needs-validation
    $(document).ready(function() {
        $('.needs-validation').each(function() {
            new FormValidator(this);
        });
    });

})(jQuery);
