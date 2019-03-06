from info.models import User
from . import index_blu

from flask import render_template, session
from flask import current_app


# 2.使用蓝图

@index_blu.route('/')
def index():
    user_id = session.get("user_id")
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    data = {
        "user_info":user.to_dict() if user else None
    }
    return render_template('news/index.html',data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
