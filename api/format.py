from flask import jsonify
from flask_restful import Resource

class formatResource(Resource):

    def __init__(self):
        pass

    @staticmethod
    def render_json(code=0, status=None, data=None, message=None):
        return formatResource.json(code=code, status=status, data=data, message=message)

    @staticmethod
    def json(code=0, status=None, data=None, message=None):
        return jsonify({
            'code': code,
            'status': status,
            'data': data,
            'message': message
        })