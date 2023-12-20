#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """defines new not found page"""
    response_data = '{\n\t"error": "Not found"\n}\n'
    response = app.response_class(
        response=response_data,
        status=404,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
