from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tes_ids = fields.One2many(
        "unicah.tes",
        "estudiante_id",
        string="Registros TES",
    )
