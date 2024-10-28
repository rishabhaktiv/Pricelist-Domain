# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderExtended(models.Model):
    _inherit = "purchase.order"

    partner_sale_order_id = fields.Many2one(
        "sale.order", string="Sale", copy=False
    )
