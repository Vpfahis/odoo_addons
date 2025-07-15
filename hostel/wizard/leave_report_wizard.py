import io
import json
import xlsxwriter
from odoo import models, fields
from odoo.tools import json_default

class LeaveReport(models.TransientModel):
    _name = 'leave.report'
    _description = 'Student Leave Report Wizard'

    room_ids = fields.Many2many('hostel.room', string='Rooms')
    student_ids = fields.Many2many('hostel.student', string='Students')
    leave_date = fields.Date(string='Start Date')
    arrival_date = fields.Date(string='Arrival Date')

    def print_leave_report(self):
        data = {
            'room_ids': self.room_ids.ids,
            'student_ids': self.student_ids.ids,
            'leave_date': self.leave_date,
            'arrival_date': self.arrival_date,
        }

        return self.env.ref('hostel.leave_report_action_pdf').report_action(self, data=data)

    def print_xlsx_leave_report(self):
        data = {
            'room_ids': self.room_ids.ids,
            'student_ids': self.student_ids.ids,
            'leave_date': self.leave_date,
            'arrival_date': self.arrival_date,
        }
        return {
            'type' : 'ir.actions.report',
            'data' : {
                'model' : 'leave.report',
                'options' : json.dumps(data, default=json_default),
                'output_format' : 'xlsx',
                'report_name' : 'Leave Report Excel'
            },
            'report_type' : 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        report_data = self.env['report.hostel.leave_report_template']._get_report_values([], data)
        records = report_data.get('data_lines', [])
        student_id, room_id = report_data.get('student_id'), report_data.get('room_id')
        leave_date, arrival_date = report_data.get('leave_date'), report_data.get('arrival_date')

        show_student = not student_id
        show_room = not room_id

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Leave Report")

        title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#ADD8E6'})
        subtitle_fmt = workbook.add_format({'font_size': 10, 'align': 'left', 'valign': 'vcenter'})
        header_fmt = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D3D3D3'})
        text_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
        date_fmt = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1, 'align': 'center', 'valign': 'vcenter'})

        headers = ['SL.No']
        col_widths = [6]
        if show_student:
            headers.append('Student')
            col_widths.append(20)
        if show_room:
            headers.append('Room')
            col_widths.append(15)
        headers += ['Leave Date', 'Arrival Date', 'Duration (days)']
        col_widths += [15, 15, 18]

        start_col = 2
        row_cursor = 5
        total_cols = len(headers)

        sheet.merge_range(row_cursor, start_col, row_cursor, start_col + total_cols - 1, 'Student Leave Report',title_fmt)
        row_cursor += 2

        subtitle_lines = []
        if room_id:
            room = self.env['hostel.room'].browse(room_id)
            subtitle_lines.append(f"Room: {room.number}")
        if student_id:
            student = self.env['hostel.student'].browse(student_id)
            subtitle_lines.append(f"Student: {student.name}")
        if leave_date:
            subtitle_lines.append(f"Start Date: {leave_date}")
        if arrival_date:
            subtitle_lines.append(f"Arrival Date: {arrival_date}")

        for line in subtitle_lines:
            sheet.merge_range(row_cursor, start_col, row_cursor, start_col + total_cols - 1, line, subtitle_fmt)
            row_cursor += 1

        row_cursor += 1
        sheet.write_row(row_cursor, start_col, headers, header_fmt)
        row_cursor += 1

        for idx, line in enumerate(records, 1):
            col = start_col
            values = [idx]
            if show_student:
                values.append(line.get('student', ''))
            if show_room:
                values.append(line.get('room', ''))
            values += [
                line.get('start_date') or '',
                line.get('arrival_date') or '',
                line.get('duration') or 0
            ]
            for i, val in enumerate(values):
                fmt = date_fmt if 'Date' in headers[i] else text_fmt
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