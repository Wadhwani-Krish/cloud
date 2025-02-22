import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, render_template

#from flask_cors import CORS

oauth = OAuth()

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    # Load configurations
    app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
    app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")
    app.config["SECRET_KEY"] = os.environ.get('secret_key')

    # Initialize OAuth
    oauth.init_app(app)

    # Register Google OAuth
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        access_token_url="https://oauth2.googleapis.com/token",
        access_token_params=None,
        client_kwargs={"scope": "openid email profile"},
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    )

    # create and configure the app & creates the database mapping
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('secret_key'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('database_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MYSQL_HOST=os.environ.get('host'),
        MYSQL_USER=os.environ.get('MySQL_user'),
        MYSQL_PASSWORD=os.environ.get('MySQL_password'),
        MYSQL_DB=os.environ.get('MySQL_database')
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass





    # a simple page that says hello to test the connection
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        return render_template('base.html')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)


    return app
