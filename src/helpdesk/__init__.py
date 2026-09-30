from flask import Flask, render_template

from helpdesk.router import blueprint as bp

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="temp")
app.register_blueprint(bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
