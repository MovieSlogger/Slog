from flask import jsonify
from flask_restful import Resource

class formatResource(Resource):

    def __init__(self):
        pass

    @staticmethod
    def render_json(code=0, data=None, message=None):
        return formatResource.json(code=code, data=data, message=message)

    @staticmethod
    def json(code=0, message=None, data=None):
        return jsonify({
            'code': code,
            'data': data,
            'message': message
        })