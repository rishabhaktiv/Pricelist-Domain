# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    note = fields.Text(string="Product Details")
    is_check = fields.Boolean(string="Check")

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """Method to set the price unit for the selected product."""
        if self.order_line:
            for line in self.order_line:
                pricelist_items = (
                    self.env["product.pricelist"]
                    .search([("partner_id", "=", self.partner_id.id)])
                    .item_ids.filtered(
                        lambda l: l.product_tmpl_id
                        == line.product_id.product_tmpl_id
                    )
                )
                if pricelist_items:
                    min_price = min(pricelist_items.mapped("fixed_price"))
                    min_pricelist_item = pricelist_items.filtered(
                        lambda item: item.fixed_price == min_price
                    )
                    if min_pricelist_item:
                        line.pricelist_id = min_pricelist_item[
                            -1
                        ].pricelist_id.id
                        line.price_unit = min_price
                    else:
                        line.pricelist_id = self.pricelist_id.id
                else:
                    line.pricelist_id = (
                        self.pricelist_id.id if self.pricelist_id else False
                    )
                line.onchange_pricelist_id()

    @api.depends("partner_id", "company_id")
    def _compute_pricelist_id(self):
        """Method to compute the pricelist"""
        for order in self:
            if order.state != "draft" or not order.partner_id:
                order.pricelist_id = False
                continue

            pricelist_ids = order._get_applicable_pricelists()

            order = order.with_company(order.company_id)
            order.pricelist_id = pricelist_ids[0] if pricelist_ids else False

    def _get_applicable_pricelists(self):
        """Utility method to get pricelists based on partner, date, and
        company."""
        return self.env["product.pricelist"].search(
            [
                ("start_date", "<=", self.date_order),
                "|",
                ("partner_id", "=", False),
                ("partner_id", "=", self.partner_id.id),
                "|",
                ("end_date", "=", False),
                ("end_date", ">=", self.date_order),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", self.company_id.id),
            ]
        )

    def get_product_details(self):
        """Method to get the product details."""
        product_list = (
            self.env["product.template"]
            .search([])
            .filtered(lambda l: l.categ_id and l.categ_id
                      .property_cost_method == "standard")
        )
        if product_list:
            product_name_list = product_list.mapped("name")
            product_category_list = product_list.mapped("categ_id.name")
            internal_ref_list = product_list.mapped("default_code")
            self.note = (
                product_name_list + product_category_list + internal_ref_list
            )
            self.is_check = True
