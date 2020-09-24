from flask import request, abort, jsonify
from flask_restful import Resource
from flask_cors import *

class MemberAPI(Resource):
    @cross_origin()
    def post(self, action):
        if action == 'create':
            return self.create()
        elif action == 'login':
            return self.login()
        elif action == 'verify':
            return self.verify()
        else:
            abort(404)

    ## create account
    def create(self):
        account = request.form['account']
        password = request.form['password']
        data = {'role': 0}
        return jsonify(status=True, data=data)

    ## login account
    def login(self):
        account = request.form['account']
        password = request.form['password']
        data = {'role': 0}
        return jsonify(status=True, data=data)

    ## verify account
    def verify(self):
        token = request.form['token']
        expired = request.form['expired']
        data = {'role': 0}
        return jsonify(status=True, data=data)