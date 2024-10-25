# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderInherited(models.Model):
    _inherit = "sale.order.line"

    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")

    @api.onchange("product_id")
    def onchange_product_id(self):
        """Method to set the lowest price unit for the selected product."""
        if self.product_id:
            pricelist_items = (
                self.env["product.pricelist"]
                .search([("partner_id", "=", self.order_id.partner_id.id)])
                .item_ids.filtered(
                    lambda l: l.product_tmpl_id
                    == self.product_id.product_tmpl_id
                )
            )
            if pricelist_items:
                min_price = min(pricelist_items.mapped("fixed_price"))
                min_pricelist_item = pricelist_items.filtered(
                    lambda item: item.fixed_price == min_price
                )
                if min_pricelist_item:
                    self.pricelist_id = min_pricelist_item[-1].pricelist_id.id
                    self.price_unit = min_price
                else:
                    self.pricelist_id = self.order_id.pricelist_id.id
            else:
                self.pricelist_id = (
                    self.order_id.pricelist_id.id
                    if self.order_id.pricelist_id
                    else False
                )
