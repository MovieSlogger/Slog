from flask import Flask
from flask_restful import Api
from database import init_db
from api import MemberAPI

app = Flask(__name__)
slog = Api(app)
init_db()

slog.add_resource(MemberAPI, '/api/member/<string:action>')

if __name__ == '__main__':
    app.run(debug=True)