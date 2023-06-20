from flask import Flask, redirect
import os
from src.auth import auth
from src.prescriptions import prescriptions
from src.database import db
from flask_jwt_extended import JWTManager
from src.notification import notifications


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY "),
            SQLALCHEMY_DATABASE_URI= os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )
    else :
        app.config.from_mapping(test_config) 

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(prescriptions)
    app.register_blueprint(notifications)

    @app.get('/<prescriptions>')
    def redirect_to_prescription(prescriptions):
        prescription=Prescription.query.filter_by(prescriptions=prescriptions).first_or_404()

        if prescription:
            prescription.visits = prescription.visits+1
            db.session.commit()

            return redirect(prescription.url)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error': 'Not found'}),404

    return app
