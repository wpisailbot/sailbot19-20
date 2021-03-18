from flask import Flask, render_template
from werkzeug.serving import run_simple

app = Flask(__name__)


@app.route("/test")
def publish():
    """
    Flask server
    :returns [string] stringified proto.vessel_state returned by the gRPC client routine
    """
    return "Flask works!"


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host= '0.0.0.0', threaded=True)