# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
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
                    self.pricelist_id = min_pricelist_item.pricelist_id.id
                    self.price_unit = min_price
                else:
                    self.pricelist_id = self.order_id.pricelist_id.id
            else:
                self.pricelist_id = (
                    self.order_id.pricelist_id.id
                    if self.order_id.pricelist_id
                    else False
                )

    @api.onchange("pricelist_id")
    def onchange_pricelist_id(self):
        """Method to update the price unit based on the selected pricelist."""
        if self.pricelist_id:
            pricelist_items = self.pricelist_id.item_ids.filtered(
                lambda l: l.product_tmpl_id == self.product_id.product_tmpl_id
            )
            self.price_unit = pricelist_items[0].fixed_price \
                if pricelist_items else self.product_id.list_price
        else:
            self.price_unit = self.product_id.list_price
