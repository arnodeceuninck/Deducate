from flask import render_template, request, session
from app.chats import bp
from app.models import User
from flask_login import current_user, login_required


@bp.route('/chats', methods=['GET'])
@login_required
def chats():
    session['name'] = current_user.name
    session['room'] = 1

    id = request.args.get("id")
    user = User.query.get_or_404(id)
    return render_template("chat/cc_chat.html", user=user)
