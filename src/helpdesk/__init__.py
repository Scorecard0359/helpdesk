from flask import Flask, render_template

from helpdesk.db import db
from helpdesk.blueprints import misc, auth

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
    )

    app.register_blueprint(misc.bp)
    app.register_blueprint(auth.bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
