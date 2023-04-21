from flask import Blueprint, render_template, request, jsonify, make_response
from vonage import Client, vonage
from src.database import Prescriptions, db


notifications = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")
client = vonage.Client(key="c0b1d64d", secret="8S0HqVULPoS4foKR")

@notifications.post('/notify')
def notify():
    phone_no = request.json.get('phone_no', '')
    
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "254708627046",
            "text": Prescriptions.meds,
            "time_taken":Prescriptions.meds_taken 
        }
    )
    if responseData["messages"][0]["status"] == "0":
        return make_response(jsonify("Message sent successfully. {responseData}", 200))
    else:
        return jsonify(f"Message failed with error: {responseData['messages'][0]['error-text']}")