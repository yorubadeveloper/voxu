from flask import Blueprint, render_template

from voxu.database import db
from .models import get_http_request_log_table_class

voxu_blueprint = Blueprint('voxu', __name__, url_prefix='/voxu')


@voxu_blueprint.route('/logs')
def logs():
    HTTPRequestLog = get_http_request_log_table_class()
    logs = db.session.query(HTTPRequestLog).all()
    db.session.close()
    return render_template('logs.html', logs=logs)
