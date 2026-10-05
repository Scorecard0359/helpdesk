from flask import Flask, render_template

from helpdesk import db, models
from helpdesk.blueprints import misc, auth

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DASQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
    )

    app.register_blueprint(misc.bp)
    app.register_blueprint(auth.bp)

    with app.app_context():
        db.create_all()

    db.init_app(app)

    return app
