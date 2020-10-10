from flask import request, abort, jsonify
from flask_cors import *
import sqlite3
from api import formatResource
import hashlib
from datetime import datetime

class MemberAPI(formatResource):
    @cross_origin()
    def post(self, action):
        if action == 'create':
            return self.create()
        elif action == 'edit':
            return self.edit()
        elif action == 'delete':
            return self.delete()
        elif action == 'manage':
            return self.manage()
        elif action == 'login':
            return self.login()
        elif action == 'verify':
            return self.verify()
        else:
            abort(404)

    @cross_origin()
    def get(self, action):
        if action == 'origin':
            return self.origin()
        else:
            abort(404)

    ## create origin account
    def origin(self):
        role = 0
        time = datetime.now()
        expired = int(datetime.timestamp(time))
        name = '卢贤明'
        avatar = ''
        account = 'admin'
        pwd = '123456'
        password = hashlib.md5(pwd.encode()).hexdigest()
        bunch = name + str(expired)
        token = hashlib.md5(bunch.encode()).hexdigest()

        try:
            with sqlite3.connect('doc.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO member (role, token, expired, name, avatar, account, password) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(role, token, expired, name, avatar, account, password))

                ## Returns the data origin
                data = {
                    'account': account,
                    'password': password,
                    'role': role,
                    'token': token,
                    'expired': expired,
                    'name': name,
                    'avatar': avatar
                }
                return self.render_json(code=200, status=True, data=data, message='账户创建成功~')
        except:
            return self.render_json(code=100, message='账户名已存在~')

    ## create account
    def create(self):
        role = request.form['role']
        time = datetime.now()
        expired = int(datetime.timestamp(time))
        name = request.form['name']
        avatar = request.form['avatar']
        account = request.form['account']
        password = request.form['password']
        bunch = name + str(expired)
        token = hashlib.md5(bunch.encode()).hexdigest()

        try:
            with sqlite3.connect('doc.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO member (role, token, expired, name, avatar, account, password) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(role, token, expired, name, avatar, account, password))

                ## Returns the data created
                try:
                    cursor.execute("""
                    SELECT id, role, name, avatar, account FROM member WHERE token='{}' AND expired='{}'
                    """.format(token, expired))

                    id, role, name, avatar, account = cursor.fetchone()
                    data = {
                        'id': id,
                        'role': role,
                        'name': name,
                        'avatar': avatar,
                        'account': account
                    }
                    return self.render_json(code=200, status=True, data=data, message='账户创建成功~')
                except:
                    return self.render_json(code=100, message='账户创建失败~')
        except:
            return self.render_json(code=100, message='账户名已存在~')

    ## edit account
    def edit(self):
        id = request.form['id']
        role = request.form['role']
        time = datetime.now()
        expired = int(datetime.timestamp(time))
        name = request.form['name']
        avatar = request.form['avatar']
        account = request.form['account']
        password = request.form['password']
        bunch = name + str(expired)
        token = hashlib.md5(bunch.encode()).hexdigest()

        try:
            with sqlite3.connect('doc.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE member SET role='{}', token='{}', expired='{}', name='{}', avatar='{}', password='{}' WHERE account='{}'
                """.format(role, token, expired, name, avatar, password, account))

                data = {
                    'id': id,
                    'role': role,
                    'name': name,
                    'avatar': avatar,
                    'account': account
                }
                return self.render_json(code=200, status=True, data=data, message='账户编辑成功~')
        except:
            return self.render_json(code=100, message='账户编辑失败~')

    ## delete account
    def delete(self):
        id = request.form['id']

        if id == 1:
            return self.render_json(code=100, message='超级账户不允许删除~')
        else:
            try:
                with sqlite3.connect('doc.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                    DELETE FROM member WHERE id='{}'
                    """.format(id))
                    return self.render_json(code=200, status=True, message='账户删除成功~')
            except:
                return self.render_json(code=100, message='账户删除失败~')

    ## manage account
    def manage(self):
        token = request.form['token']
        expired = request.form['expired']

        ## Verify permissions
        try:
            with sqlite3.connect('doc.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT role FROM member WHERE token='{}' AND expired='{}'
                """.format(token, expired))

                role = cursor.fetchone()[0]
                if role == 0:
                    try:
                        cursor.execute("""
                        SELECT id, role, name, avatar, account FROM member
                        """)
                        list = cursor.fetchall()
                        data = []
                        for row in list:
                            item = {
                                'id': row[0],
                                'role': row[1],
                                'name': row[2],
                                'avatar': row[3],
                                'account': row[4]
                            }
                            data.append(item)
                        return self.render_json(code=200, status=True, data=data)
                    except:
                        return self.render_json(code=100, message='数据校验失败~')
                else:
                    return self.render_json(code=100, status=False, message='您没有操作权限~')
        except:
            return self.render_json(code=100, message='接口请求失败~')

    ## login account
    def login(self):
        account = request.form['account']
        pwd = request.form['password']
        password = hashlib.md5(pwd.encode()).hexdigest()

        try:
            with sqlite3.connect('doc.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT role, token, expired FROM member WHERE account='{}' AND password='{}'
                """.format(account, password))

                role, token, expired = cursor.fetchone()

                data = {
                    'role': role,
                    'token': token,
                    'expired': expired
                }
                return self.render_json(code=200, data=data)
        except:
            return self.render_json(code=100, message='账户密码错误~')

    ## verify account
    def verify(self):
        token = request.form['token']
        expired = request.form['expired']

        try:
            with sqlite3.connect('doc.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT role, name FROM member WHERE token='{}' AND expired='{}'
                """.format(token, expired))

                role, name = cursor.fetchone()
                stamp = datetime.now()
                poke = int(datetime.timestamp(stamp))
                past = poke - int(expired)

                # token过期
                if past >= 60:
                    bunch = name + str(poke)
                    comd = hashlib.md5(bunch.encode()).hexdigest()
                    try:
                        cursor.execute("""
                        UPDATE member SET token='{}', expired='{}' WHERE token='{}' AND expired='{}'
                        """.format(comd, poke, token, expired))
                        data = {
                            'role': role,
                            'token': comd,
                            'expired': poke
                        }
                        return self.render_json(code=200, status=False, data=data)
                    except:
                        return self.render_json(code=100, message='未知错误~')
                # token未过期
                else:
                    data = {
                        'role': role
                    }
                    return self.render_json(code=200, status=True, data=data)
        except:
            return self.render_json(code=100, message='未知错误~')