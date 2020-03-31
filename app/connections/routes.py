from flask import render_template, flash, redirect, url_for, request, session
from app import db
from flask_login import current_user
from app.connections import bp
from app.models import ContactRequest, ConnectStatus


@bp.route('/request', methods=['GET'])
def connection_request():
    receiver_id = request.args.get("id")
    if current_user.connection(receiver_id):
        flash("One of you has already requested a connection")
    else:
        connection_request = ContactRequest(sender_id=current_user.id, receiver_id=receiver_id)
        db.session.add(connection_request)
        db.session.commit()
        flash("Request sent")
    return redirect(url_for("auth.index"))


@bp.route('/request_reply', methods=['GET'])
def request_reply():
    reply = request.args.get("reply")
    sender_id = request.args.get("id")
    con_request = ContactRequest.query.filter_by(sender_id=sender_id, receiver_id=current_user.id).first()
    if reply == "accept":
        con_request.status = ConnectStatus.accepted
        flash("Request accepted")
    elif reply == "reject":
        con_request.status = ConnectStatus.rejected
        flash("Request rejected")
    db.session.commit()
    return redirect(url_for("auth.index"))
