from flask import Blueprint, request, jsonify, make_response
from src.database import Prescriptions, db
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required


prescriptions = Blueprint("prescriptions", __name__, url_prefix="/api/v1/prescriptions")

@prescriptions.route('/', methods=['POST', 'GET'])
@jwt_required() #makin this route available to logged in users only
def med_prescriptions():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        meds = request.get_json().get('meds', '')
        phone_no = request.get_json().get('phone_no', '')


        if Prescriptions.query.filter_by(phone_no=phone_no).first():
            return jsonify({
                'error': 'Prescription already administered'
            }), 409

        prescriptions=Prescriptions(meds=meds, phone_no=phone_no, user_id=current_user)
        db.session.add(prescriptions)
        db.session.commit()

        return jsonify({
            'id': prescriptions.id,
            'meds': prescriptions.meds,
            'tracking': prescriptions.tracking,
            'phone_no': prescriptions.phone_no,
            'medication_time': prescriptions.medication_time,
            'meds_taken': prescriptions.meds_taken,
        }), 201

    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        prescriptions=Prescriptions.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)

        data=[]

        for prescription in prescriptions.items :
            data.append({
                'id': prescription.id,
                'meds': prescription.meds,
                'tracking': prescription.tracking,
                'phone_no': prescription.phone_no,
                'medication_time': prescription.medication_time,
                'meds_taken': prescription.meds_taken,
            })

        meta = {
            "page": prescriptions.page,
            'pages': prescriptions.pages,
            'total_count': prescriptions.total,
            'prev_page': prescriptions.prev_num,
            'next_page': prescriptions.next_num,
            'has_next': prescriptions.has_next,
            'has_prev': prescriptions.has_prev,

        }

        return jsonify({'data': data, "meta": meta}), 200


@prescriptions.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()

    prescriptions = Prescriptions.query.filter_by(user_id=current_user, id=id).first()

    if not prescriptions:
        return jsonify({'message': 'Item not found'}), 404

    return jsonify({
        'id': prescriptions.id,
        'tracking': prescriptions.tracking,
        'meds':prescriptions.meds,
        'medication_time': prescriptions.medication_time,
        'meds_taken': prescriptions.meds_taken,
    }), 200

@prescriptions.delete("/<int:id>")
@jwt_required()
def delete_prescriptions(id):
    current_user = get_jwt_identity()

    prescriptions = Prescriptions.query.filter_by(user_id=current_user, id=id).first()

    if not prescriptions:
        return make_response(jsonify({'message': 'Item not found'}), 404)

    db.session.delete(prescriptions)
    db.session.commit()

    return jsonify({}), 204


@prescriptions.put('/<int:id>')
@prescriptions.patch('/<int:id>')
@jwt_required()
def editprescriptions(id):
    current_user = get_jwt_identity()

    prescriptions = Prescriptions.query.filter_by(user_id=current_user, id=id).first()

    if not prescriptions:
        return jsonify({'message': 'Item not found'}), 404

    meds = request.get_json().get('meds', '')
    phone_no = request.get_json().get('phone_no', '')


    prescriptions.phone_no = phone_no
    prescriptions.meds = meds

    db.session.commit()

    return jsonify({
        'id': prescriptions.id,
        'url': prescriptions.url,
        'short_url': prescriptions.short_url,
        'visit': prescriptions.visits,
        'body': prescriptions.body,
        'created_at': prescriptions.created_at,
        'updated_at': prescriptions.updated_at,
    }), 200
