from flask import Flask


def create_app():

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'derek'

    from api.views.controllers import red_flag_blueprint as red_flag_blueprint
    from api.views.controllers import user_blueprint as user_blueprint

    app.register_blueprint(red_flag_blueprint)
    app.register_blueprint(user_blueprint)

    return app
