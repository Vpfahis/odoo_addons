from odoo import http
from odoo.http import request

class RoomSnippetController(http.Controller):

    @http.route('/get_latest_rooms', type='json', auth='public', website=True)
    def get_latest_rooms(self):
        rooms = request.env['hostel.room'].sudo().search([], order='create_date desc')
        room_data = []
        for room in rooms:
            room_data.append({
                'id': room.id,
                'number': room.number,
                'image': room.image,
            })
        return {'rooms': room_data}

class RoomDetailController(http.Controller):
    @http.route(['/room/<int:room_id>'], type='http', auth='public', website=True)
    def room_detail(self, room_id, **kwargs):
        room = request.env['hostel.room'].sudo().browse(room_id)
        return request.render('hostel.room_detail_template', {
            'room': room,
        })
