from flask import request, abort, jsonify
# from flask_restful import Resource
from flask_cors import *

from api import formatResource

from sqlalchemy import create_engine

class MemberAPI(formatResource):
    @cross_origin()
    def get(self, action):
        if action == 'create':
            return self.create()
        elif action == 'manage':
            return self.manage()
        elif action == 'login':
            return self.login()
        elif action == 'verify':
            return self.verify()
        else:
            abort(404)

    ## create account
    def create(self):
        # role = request.form['role']
        # token = 'token'
        # expired = 3225345234
        # account = request.form['account']
        # password = request.form['password']

        role = 'aaa'
        token = 'token'
        expired = 1111
        account = 'cccc'
        password = 'dddd'

        engine = create_engine('sqlite:///test.db')
        con = engine.connect()
        sql = "INSERT INTO member (role, token, expired, account, password) VALUES ('{}', '{}', '{}', '{}', '{}')".format(role, token, expired, account, password)
        res = con.execute(sql)
        data = list(res)

        return self.render_json(code=200, data=data)

    def manage(self):
        token = request.form['token']
        expired = request.form['expired']

        engine = create_engine('sqlite:///test.db')
        con = engine.connect()
        sql = "SELECT * FROM member"
        res = con.execute(sql)

        data = [{'1': 1}, {'2': 2}, {'3': 3}]
        # for row in res:
        #     data[3] = row
        # for row in res:
        #     data = row.account
            # list = {
            #     "role": row.role,
            #     "token": row.token,
            #     "expired": row.expired,
            #     "account": row.account,
            #     "password": row.password,
            # }
            # data = list

        return self.render_json(code=200, data=data)

    ## login account
    def login(self):
        account = request.form['account']
        password = request.form['password']

        engine = create_engine('sqlite:///test.db')
        con = engine.connect()
        sql = "SELECT password FROM member WHERE account='{}'".format(account)
        con.execute(sql)

        return self.render_json(code=200, data=password)

    ## verify account
    def verify(self):
        token = request.form['token']
        expired = request.form['expired']
        data = {'role': 0}
        return jsonify(status=True, data=data)