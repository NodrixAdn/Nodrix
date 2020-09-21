from odoo import api, fields, models, _
from odoo.exceptions import Warning
import binascii
import tempfile
import xlrd
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)
import io

try:
	import xlrd
except ImportError:
	_logger.debug('Cannot `import xlrd`.')
try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')
		
class importar_productos_ventas(models.TransientModel):

	_name='order.line.wizard'

	sale_order_file=fields.Binary(string="Abrir Archivo")
	import_option = fields.Selection([('csv', 'CSV'),('xls', 'XLS')],string='Seleccionar',default='xls')
	import_prod_option = fields.Selection([('barcode', 'Código de barras'),('code', 'Código interno'),('name', 'Nombre del producto')],string='Buscar Producto por ',default='barcode')

	def importar_productos(self):
		res = False
		if self.import_option == 'csv':
			keys = ['f_alta_ped', 'SAZON', 'Consec.','Code_B', 'Producto', 'cant_Ped', 'unidad', 'Surtido', 'cant_surt', 'Tipo']
			try:
				csv_data = base64.b64decode(self.sale_order_file)
				data_file = io.StringIO(csv_data.decode("utf-8"))
				data_file.seek(0)
				file_reader = []
				csv_reader = csv.reader(data_file, delimiter=',')
				file_reader.extend(csv_reader)

			except Exception:
				raise Warning(_("Selecciona un archivo válido"))

			values = {}
			for i in range(len(file_reader)):
				field = list(map(str, file_reader[i]))
				values = dict(zip(keys, field))
				if values:
					if i < 3:
						continue
					else:
						if field[0]=="" or not field:
							print("row_ no break", i)
							return res
						values.update({
									'product' : field[3].split('.')[0],
									'name' : field[4],
									'quantity' : field[5],
									'uom' : field[6],
									'row': i
								})
						print(values)
						res = self.create_order_line(values)
		else:
			try:
				fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
				fp.write(binascii.a2b_base64(self.sale_order_file))
				fp.seek(0)
				values = {}
				workbook = xlrd.open_workbook(fp.name)
				sheet = workbook.sheet_by_name('PRODUCTOS SURTIDOS')
			except Exception:
				raise Warning(_("Selecciona un archivo válido"))

			for row_no in range(sheet.nrows):
				val = {}
				print("numero", sheet.nrows)
				if row_no <= 0:
					fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
				else:
					row_no=row_no+2
					line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
					if line[0]=="":
						print("row_ no break", row_no)
						return res
					values.update({
									'product' : line[3].split('.')[0],
									'name' : line[4],
									'quantity' : line[5],
									'uom' : line[6],
									'row': row_no
								})
					res = self.create_order_line(values)
		return res

	def create_order_line(self,values):
		if not values:
			return True

		sale_order_brw = self.env['sale.order'].browse(self._context.get('active_id'))
		product=values.get('product')
		uom=values.get('uom')
		row=values.get('row')
		uom_obj_search=self.env['uom.uom'].search([('name','=',uom)])
		print(uom_obj_search.factor)
		print(uom_obj_search.factor_inv)
		if not uom_obj_search:
				raise Warning(_('La unidad de medida "%s" no esta disponible en el sistema. Fila: %s') % (uom,row ))
		print(product)
		print(values['product'])
		print(values['name'])
		if self.import_prod_option == 'barcode':
			product_obj_search=self.env['product.product'].search([('barcode',  '=',values['product'])])
		elif self.import_prod_option == 'code':
			product_obj_search=self.env['product.product'].search([('default_code', '=',values['product'])])
		else:
			product_obj_search=self.env['product.product'].search([('name', '=',values['name'])])
			
		if product_obj_search:
			product_id=product_obj_search
		else:
			raise Warning(_('%s %s No se encontro el producto". Fila: %s') % (values.get('product'),values.get('name'),row))
			
		if sale_order_brw.state == 'draft' or sale_order_brw.state == 'sent' :
			order_lines=self.env['sale.order.line'].create({
											'order_id':sale_order_brw.id,
											'product_id':product_id.id,
											'name':product_id.name,
											'product_uom_qty':values.get('quantity'),
											'price_unit':product_id.lst_price*uom_obj_search.factor_inv,
											'product_uom':uom_obj_search.id,
											})
		elif sale_order_brw.state != 'sent' or sale_order_brw.state != 'draft':
			raise UserError(_('No se puede importar datos en una orden validada o confirmada'))
		return True