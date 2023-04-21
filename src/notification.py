from flask import Blueprint, render_template, request, jsonify, make_response
from vonage import Client, vonage
from src.database import Prescriptions, db
from flask_jwt_extended import get_jwt_identity, jwt_required


notifications = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")
client = vonage.Client(key="c0b1d64d", secret="8S0HqVULPoS4foKR")

@notifications.get('/notify')
@jwt_required()
def notify():
    current_user = get_jwt_identity()
    prescriptions=Prescriptions.query.filter_by(user_id=current_user).first()
    
    
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Prescription Buddy",
            "to": "254708627046",
            "text": prescriptions, 
        }
    )
    if responseData["messages"][0]["status"] == "0":
        return make_response(jsonify("Message sent successfully. {responseData}", 200))
    else:
        return jsonify(f"Message failed with error: {responseData['messages'][0]['error-text']}")