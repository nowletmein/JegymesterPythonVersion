from apiflask import APIFlask
from app.extensions import db
from flask_migrate import Migrate
from config import Config

def create_app(config_class=Config):    
    # Use a specific name like 'flask_app' to avoid conflict with the package name 'app'
    flask_app = APIFlask(__name__, 
                         json_errors=True, 
                         title="Jegymester API",
                         docs_path="/swagger")
    
    flask_app.config.from_object(config_class)
    
    db.init_app(flask_app)
    
    from flask_migrate import Migrate
    migrate = Migrate(flask_app, db, render_as_batch=True)
    
    with flask_app.app_context():
        import app.models 
    
    from app.blueprints import bp as bp_main
    flask_app.register_blueprint(bp_main, url_prefix='/api')

    return flask_app