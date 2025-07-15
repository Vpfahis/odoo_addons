from odoo import models, api
from odoo.exceptions import UserError


class StudentReportAbstract(models.AbstractModel):
    _name = 'report.hostel.student_report_template'  # Must match the report_name with prefix 'report.'

    @api.model
    def _get_report_values(self, docids, data=None):
        student_ids = data.get('student_ids', [])
        room_ids = data.get('room_ids', [])

        query = """
            SELECT s.id, s.name, s.payment_state_stored AS payment_state,
                   r.number AS room_name,
                   COALESCE(SUM(inv.amount_residual), 0) AS pending_amount
            FROM hostel_student s
            LEFT JOIN hostel_room r ON s.room = r.id
            LEFT JOIN account_move inv ON inv.student_id = s.id AND inv.state = 'posted'
            WHERE 1=1
        """
        params = []

        if student_ids:
            query += " AND s.id = ANY(%s)"
            params.append(student_ids)

        if room_ids:
            query += " AND s.room = ANY(%s)"
            params.append(room_ids)

        query += " GROUP BY s.id, r.number, s.payment_state_stored ORDER BY s.name"

        self.env.cr.execute(query, params)
        records = self.env.cr.dictfetchall()

        if not records:
            raise UserError("No data available for the selected filter(s).")

        return {
            'docs': records,
            'doc_ids': [r['id'] for r in records],
            'doc_model': 'hostel.student',
            'student_id': student_ids[0] if len(student_ids) == 1 else False,
            'room_id': room_ids[0] if len(room_ids) == 1 else False,
        }


