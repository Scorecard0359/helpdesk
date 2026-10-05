from flask import Flask, render_template

from helpdesk import db
from helpdesk.blueprints import misc, auth

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'helpdesk.sqlite'),
    )

    app.register_blueprint(misc.bp)
    app.register_blueprint(auth.bp)

    db.init_app(app)

    return app
