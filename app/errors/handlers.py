from flask import render_template
from app.errors import bp


@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html', title='Page not found'), 404


@bp.errorhandler(405)
def method_not_allowed(e):
    return render_template('errors/405.html', title='Method not allowed'), 405


# Function for deliberatly creating an error (for testing the error mailing system)
@bp.route('/internal_server_error')
def internal_server_error():
    return render_template("errors/500.html", title="Internal error")


@bp.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', title='Internal error'), 500
