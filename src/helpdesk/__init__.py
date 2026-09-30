from flask import Flask, render_template

from helpdesk import db
from helpdesk.blueprints import misc, auth

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev")

    app.register_blueprint(misc.bp)
    app.register_blueprint(auth.bp)

    #db.init_db()

    return app
