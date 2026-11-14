from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UnicahTes(models.Model):
    _name = "unicah.tes"
    _description = "Registro de Trabajo Educativo Social"

    name = fields.Char(
        string="Referencia TES",
        required=True,
    )

    estudiante_id = fields.Many2one(
        "res.partner",
        string="Estudiante",
        required=True,
        domain="[('tipo_cliente', '=', 'estudiante')]",
    )

    fecha_inicio = fields.Date(
        string="Fecha de inicio",
        required=True,
    )

    fecha_fin = fields.Date(
        string="Fecha de finalización",
    )

    estado = fields.Selection(
        [
            ("proceso", "En proceso"),
            ("completado", "Completado"),
        ],
        string="Estado",
        default="proceso",
        required=True,
    )

    actividad_ids = fields.One2many(
        "unicah.tes.actividad",
        "tes_id",
        string="Actividades realizadas",
    )

    horas_realizadas = fields.Float(
        string="Horas realizadas",
        compute="_compute_horas",
    )

    horas_pendientes = fields.Float(
        string="Horas pendientes",
        compute="_compute_horas",
    )

    @api.depends("actividad_ids.horas")
    def _compute_horas(self):
        for tes in self:
            total = sum(tes.actividad_ids.mapped("horas"))
            tes.horas_realizadas = total
            tes.horas_pendientes = max(0, 40 - total)

    @api.constrains("estudiante_id")
    def _check_estudiante(self):
        for tes in self:
            if tes.estudiante_id.tipo_cliente != "estudiante":
                raise ValidationError(
                    "El registro TES solamente puede asignarse a un estudiante."
                )

            duplicado = self.search([
                ("estudiante_id", "=", tes.estudiante_id.id),
                ("id", "!=", tes.id),
            ], limit=1)

            if duplicado:
                raise ValidationError(
                    "Este estudiante ya tiene un registro TES. "
                    "Agregue las nuevas actividades al registro existente."
                )


class UnicahTesActividad(models.Model):
    _name = "unicah.tes.actividad"
    _description = "Actividad de Trabajo Educativo Social"
    _order = "fecha desc"

    name = fields.Char(
        string="Nombre de la actividad",
        required=True,
    )

    tes_id = fields.Many2one(
        "unicah.tes",
        string="Registro TES",
        required=True,
        ondelete="cascade",
    )

    fecha = fields.Date(
        string="Fecha",
        required=True,
        default=fields.Date.context_today,
    )

    horas = fields.Float(
        string="Horas realizadas",
        required=True,
    )

    descripcion = fields.Text(
        string="Descripción",
    )

    @api.constrains("horas")
    def _check_horas(self):
        for actividad in self:
            if actividad.horas <= 0:
                raise ValidationError(
                    "Las horas de una actividad deben ser mayores que cero."
                )
