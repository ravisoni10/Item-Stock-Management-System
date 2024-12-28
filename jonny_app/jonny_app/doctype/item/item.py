# Copyright (c) 2024, ravi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Item(Document):
	def before_save(self):
		if not self.item_code:
			last_item = frappe.db.get_value("Item", filters={}, fieldname="item_code", order_by="item_code desc")
			
			if last_item:
				last_number = int(last_item.replace("ITEM", ""))
				new_item_code = f"ITEM{str(last_number + 1).zfill(4)}"
			else:
				new_item_code = "ITEM0001"

			self.item_code = new_item_code




