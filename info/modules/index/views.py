from info.utils.response_code import RET
from . import index_blu

from flask import render_template, session, request, jsonify
from flask import current_app

from info import constants
from info.models import User, News, Category


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

        # 获取点击排行数据
    news_list = None
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())


    # 获取新闻分类数据
    categories = Category.query.all()
    # 定义列表保存分类数据
    categories_dicts = []

    for category in categories:
        # 拼接内容
        categories_dicts.append(category.to_dict())




    data = {
        "user_info":user.to_dict() if user else None,
        "click_news_list":click_news_list,
        "categories":categories_dicts,
    }
    return render_template('news/index.html',data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')


@index_blu.route('/news_list')
def get_news_list():
    """
    获取指定分类的新闻列表
    1. 获取参数
    2. 校验参数
    3. 查询数据
    4. 返回数据
    :return:
    """

    # 1. 获取参数
    args_dict = request.args
    page = args_dict.get("page", '1')
    per_page = args_dict.get("per_page", constants.HOME_PAGE_MAX_NEWS)
    category_id = args_dict.get("cid", '1')

    # 2. 校验参数
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3. 查询数据并分页
    filters = []
    # 如果分类id不为1，那么添加分类id的过滤
    if category_id != "1":
        filters.append(News.category_id == category_id)
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
        # 获取查询出来的数据
        items = paginate.items
        # 获取到总页数
        total_page = paginate.pages
        current_page = paginate.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    news_li = []
    for news in items:
        news_li.append(news.to_basic_dict())
    data = {
        'news_dict_li':news_li,
        'total_page':total_page,
        'current_page':current_page,
    }

    # 4. 返回数据
    return jsonify(errno=RET.OK, errmsg="OK", data=data)