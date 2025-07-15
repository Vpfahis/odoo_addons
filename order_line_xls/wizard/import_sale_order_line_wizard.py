from odoo import models, fields,_
from odoo.exceptions import UserError
from io import BytesIO
import base64
import openpyxl


class ImportSaleOrderLineWizard(models.TransientModel):
    _name = 'import.sale.order.line.wizard'
    _description = 'Import Sale Order Lines Wizard'

    file = fields.Binary("File")
    file_name = fields.Char("File Name")
    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)

    def import_lines(self):
        if not self.file:
            raise UserError("No file uploaded")
        try:
            workbook = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), data_only=True)
            sheet = workbook.active

            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                name, qty, uom_name, description, price = row

                qty = float(qty)
                price = float(price)

                product = self.env['product.product'].search([('name', '=', str(name).strip())], limit=1)
                if not product:
                    raise UserError(f"Row {i}: Product '{name}' not found.")

                uom = self.env['uom.uom'].search([('name', '=', str(uom_name).strip())], limit=1)
                if not uom:
                    raise UserError(f"Row {i}: UoM '{uom_name}' not found.")

                existing_line = None
                for line in self.order_id.order_line:
                    if line.product_id.id == product.id and line.price_unit == price:
                        existing_line = line
                        break

                if existing_line:
                    existing_line.write({
                        'product_uom_qty': existing_line.product_uom_qty + qty,
                        'price_unit': price,
                    })
                else:
                    self.order_id.order_line.create({
                        'order_id': self.order_id.id,
                        'product_id': product.id,
                        'product_uom_qty': qty,
                        'product_uom': uom.id,
                        'name': description,
                        'price_unit': price,
                    })
        except:
            raise UserError(_('Please insert a valid file'))

