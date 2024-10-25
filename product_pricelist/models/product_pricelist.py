# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductPricelistInherited(models.Model):
    _inherit = "product.pricelist"

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    partner_id = fields.Many2one("res.partner", string="Customer")
    current_date = fields.Datetime(
        string="Current Date", default=fields.Datetime.now
    )

    @api.model
    def _search(
        self, domain, offset=0, limit=None, order=None, access_rights_uid=None
    ):
        """Methods for filter the fields related to the model"""
        if (
            "partner_id" in self._context
            and self._context.get("partner_id")
            and "date_order" in self._context
            and self._context.get("date_order")
        ):
            partner_id = self._context["partner_id"]
            date_order = self._context["date_order"]
            domain += [
                ("start_date", "<=", date_order),
                "|",
                ("partner_id", "=", False),
                ("partner_id", "=", partner_id),
                "|",
                ("end_date", "=", False),
                ("end_date", ">=", date_order),
            ]
        return super()._search(domain, offset, limit, order, access_rights_uid)
