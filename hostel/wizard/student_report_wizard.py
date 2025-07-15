import io
import json
import xlsxwriter
from odoo import models, fields
from odoo.tools import json_default

class StudentReport(models.TransientModel):
    _name = 'student.report'
    _description = 'A report of students'

    room_ids = fields.Many2many('hostel.room',string="Room")
    student_ids = fields.Many2many('hostel.student',string="Students")

    def print_student_report(self):
        data = {
            'student_ids': self.student_ids.ids,
            'room_ids': self.room_ids.ids,
        }
        return self.env.ref('hostel.student_report_action_pdf').report_action(self, data=data)

    def print_xlsx_student_report(self):
        data = {
            'model': 'student.report',
            'student_ids': self.student_ids.ids,
            'room_ids': self.room_ids.ids,
        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'student.report',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Student Excel Report',
            },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        report_model = self.env['report.hostel.student_report_template']
        report_data = report_model._get_report_values([], data)
        records = report_data.get('docs', [])
        student_id = report_data.get('student_id')
        room_id = report_data.get('room_id')

        show_student = not student_id
        show_room = not room_id

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Student Report")

        title_fmt = workbook.add_format({'bold': True, 'font_size': 16, 'bg_color': '#8cd4d2', 'align': 'center', 'valign': 'vcenter'})
        subtitle_fmt = workbook.add_format({'font_size': 10, 'align': 'left', 'valign': 'vcenter'})
        header_fmt = workbook.add_format({'bg_color': '#D3D3D3', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        text_fmt = workbook.add_format({'font_size': 10, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        currency_fmt = workbook.add_format({'num_format': '#,##0.00', 'font_size': 10, 'border': 1, 'align': 'center', 'valign': 'vcenter'})

        headers = ['SL.No']
        col_widths = [6]
        if show_student:
            headers.append('Name')
            col_widths.append(20)
        headers.append('Pending Amount')
        col_widths.append(15)
        if show_room:
            headers.append('Room')
            col_widths.append(15)
        headers.append('Invoice Status')
        col_widths.append(18)

        total_cols = len(headers)
        start_col = 2
        row_cursor = 5

        sheet.merge_range(row_cursor, start_col, row_cursor, start_col + total_cols - 1, "Student Report", title_fmt)
        row_cursor += 2

        if student_id:
            student_name = self.env['hostel.student'].browse(student_id).name
            sheet.merge_range(row_cursor, start_col, row_cursor, start_col + total_cols - 1, f"Student: {student_name}",
                              subtitle_fmt)
            row_cursor += 1
        if room_id:
            room_number = self.env['hostel.room'].browse(room_id).number
            sheet.merge_range(row_cursor, start_col, row_cursor, start_col + total_cols - 1, f"Room: {room_number}",
                              subtitle_fmt)
            row_cursor += 1

        row_cursor += 1
        sheet.write_row(row_cursor, start_col, headers, header_fmt)
        row_cursor += 1

        selection = dict(self.env['hostel.student']._fields['payment_state'].selection)
        for idx, rec in enumerate(records, start=1):
            col = start_col
            row_vals = [idx]
            if show_student:
                row_vals.append(rec['name'])
            row_vals.append(rec['pending_amount'])
            if show_room:
                row_vals.append(rec['room_name'] or '')
            row_vals.append(selection.get(rec['payment_state'], ''))

            for i, val in enumerate(row_vals):
                fmt = currency_fmt if headers[i] == 'Pending Amount' else text_fmt
                sheet.write(row_cursor, col + i, val, fmt)
            row_cursor += 1

        sheet.set_column(0, 1, 4)
        for i, width in enumerate(col_widths):
            sheet.set_column(start_col + i, start_col + i, width)
        sheet.set_column(start_col + len(col_widths), start_col + len(col_widths) + 1, 4)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

