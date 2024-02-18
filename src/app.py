from flask import Flask

from api.db import init_db_app
from api.routes import bp

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(bp, url_prefix='/example')

init_db_app(app)

if __name__ == '__main__':
    app.run(debug=True)
