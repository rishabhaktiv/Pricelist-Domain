# -*- coding: utf-8 -*-

{
    "name": "Product Pricelist",
    "version": "17.0.1.0.3",
    "category": "Product",
    "summary": "Price of Product",
    "description": """
        Product Pricelist
        ========================================
        This module filtered the pricelist of products based on the partners
        and dates
        """,
    "author": "Aktiv Software",
    "company": "Aktiv Software",
    "website": "https://www.aktivsoftware.com",
    "depends": ["sale_management", "product"],
    "data": [
        "views/product_pricelist_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}
