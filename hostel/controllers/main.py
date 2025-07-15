import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.http import serialize_exception as _serialize_exception
from odoo.tools import html_escape

class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name=None, **kw):
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                report_filename = (report_name or 'Report') + '.xlsx'
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(report_filename))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))

class HostelWebsite(http.Controller):
    @http.route('/student_registration', type='http', auth='public', website=True)
    def student_registration(self, **kwargs):
        rooms = request.env['hostel.room'].sudo().search([
            ('state', 'in', ['empty', 'partial']),
            ('available_bed', '>', 0)
        ])
        return request.render('hostel.student_register_template', {
            'rooms': rooms,
            'error': None,
        })

    @http.route('/student/register/submit', type='http', auth='public', website=True, csrf=False)
    def student_register_submit(self, **post):
        name = post.get('name')
        email = post.get('email')
        dob = post.get('dob')
        room_id = int(post.get('room_id')) if post.get('room_id') else None

        rooms = request.env['hostel.room'].sudo().search([
            ('state', 'in', ['empty', 'partial']),
            ('available_bed', '>', 0)
        ])

        email_exists = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        if email_exists:
            return request.render('hostel.student_register_template', {
                'rooms': rooms,
                'error': 'Email already exists. Please use a different one.',
                'form_data': {
                    'name': name,
                    'email': email,
                    'dob': dob,
                    'room_id': room_id
                }
            })

        room = request.env['hostel.room'].sudo().search([
            ('id', '=', room_id),
            ('state', 'in', ['empty', 'partial']),
            ('available_bed', '>', 0)
        ], limit=1)

        if not room:
            return request.render('hostel.student_register_template', {
                'rooms': rooms,
                'error': 'Selected room is not available.',
                'form_data': {
                    'name': name,
                    'email': email,
                    'dob': dob,
                    'room_id': room_id
                }
            })

        student = request.env['hostel.student'].sudo().create({
            'name': name,
            'email': email,
            'dob': dob,
            'room': room.id,
        })

        room.available_bed -= 1
        room.state = 'full' if room.available_bed == 0 else 'partial'

        return request.render('hostel.student_register_success', {
            'student': student
        })
