from odoo import models, api
from odoo.exceptions import UserError


class StudentLeaveReportAbstract(models.AbstractModel):
    _name = 'report.hostel.leave_report_template'
    _description = 'Student Leave Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        student_ids = data.get('student_ids', [])
        room_ids = data.get('room_ids', [])
        leave_date = data.get('leave_date')
        arrival_date = data.get('arrival_date')

        query = """
            SELECT 
                hsl.id AS id,
                hs.name AS student,
                hr.number AS room,
                hsl.leave_date AS start_date,
                hsl.arrival_date,
                (hsl.arrival_date - hsl.leave_date) AS duration
            FROM hostel_student_leave hsl
            JOIN hostel_student hs ON hsl.student_id = hs.id
            LEFT JOIN hostel_room hr ON hs.room = hr.id
            WHERE hsl.state = 'approved'
        """
        params = []

        if student_ids:
            query += " AND hsl.student_id = ANY(%s)"
            params.append(student_ids)

        if room_ids:
            query += " AND hs.room = ANY(%s)"
            params.append(room_ids)

        if leave_date:
            query += " AND hsl.leave_date >= %s"
            params.append(leave_date)

        if arrival_date:
            query += " AND hsl.arrival_date <= %s"
            params.append(arrival_date)

        query += " ORDER BY hsl.leave_date"

        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        if not results:
            raise UserError("No data available for the selected filter(s).")

        return {
            'doc_ids': [r['id'] for r in results],
            'doc_model': 'hostel.student.leave',
            'data_lines': results,
            'student_id': student_ids[0] if len(student_ids) == 1 else False,
            'room_id': room_ids[0] if len(room_ids) == 1 else False,
            'leave_date': leave_date,
            'arrival_date': arrival_date,
        }

