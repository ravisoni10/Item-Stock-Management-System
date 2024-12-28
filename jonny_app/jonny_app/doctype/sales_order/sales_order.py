# Copyright (c) 2024, ravi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class SalesOrder(Document):
    def validate(self):
        self.order_date = datetime.now()
        total_amount = 0
        for item in self.sale_child:
            item.amount = item.quantity * item.rate
            total_amount += item.amount
        self.total_amount = total_amount

    def on_submit(self):
        for item in self.sale_child:
            self.update_stock(item.item, -item.quantity)

    def update_stock(self, item_code, qty):
        item = frappe.get_doc("Item", item_code)
        if item.stock_quantity + qty < 0:
            frappe.throw(f"Insufficient stock for Item: {item.item_name} "
                         f" stock Availble {item.stock_quantity} "   )

        item.stock_quantity += qty
        item.save()