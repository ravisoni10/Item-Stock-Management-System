# Copyright (c) 2024, ravi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class PurchaseOrder(Document):
    def validate(self):
        self.order_date = datetime.now()
        totat_amount = 0
        for item in self.purchase_child:
            item.amount = item.quantity * item.rate
            totat_amount += item.amount
        self.totat_amount = totat_amount

    def on_submit(self):
        
        for item in self.purchase_child:
            self.update_stock(item.item, item.quantity)
        
            

    def update_stock(self, item_code, qty):
        item = frappe.get_doc("Item", item_code)
        item.stock_quantity += qty
        item.save()