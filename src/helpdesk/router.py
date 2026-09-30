from flask import Blueprint, render_template, abort

blueprint = Blueprint("router", __name__, static_folder='static')

@blueprint.route("/")
def page_index():
    return render_template("index.html")
