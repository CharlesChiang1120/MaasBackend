from flask import request, jsonify
from flask_restx import Api
from resources.user import Users, User, UserGet, UserPickupLocation
from resources.activity import Activities
from resources.sharecar import ShareCar
from flask_swagger_ui import get_swaggerui_blueprint
from server import create_app
from werkzeug.exceptions import HTTPException

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={ 
        'app_name': "Test application"
    },
)

app = create_app()
api = Api(app)

app.register_blueprint(swaggerui_blueprint)

api.add_resource(Users, '/users')
api.add_resource(User, '/user')
api.add_resource(UserGet, '/user/<string:name>')
api.add_resource(Activities, '/activity')
api.add_resource(UserPickupLocation, '/userlocation')
api.add_resource(ShareCar, '/sharecarevent')


@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({
            "message": e.description,
            "error": str(e)
        }).data
        response.content_type = "application/json"
        return response

    # Handle other exceptions
    return jsonify({
        "message": "An unexpected error occurred",
        "error": str(e)
    }), 500

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='127.0.0.1', port=5000)
