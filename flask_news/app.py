# -*- coding: UTF-8 -*-
from __future__ import unicode_literals     # Python提供了__future__模块，把下一个新版本的特性导入到当前版本，于是我们就可以在当前版本中测试一些新版本的特性
import datetime     #导入时间模块
import requests
import feedparser   #此模块可以方便的获取RSS订阅源的信息
from flask import Flask, render_template, request, make_response
#render_template模块根据用户模板返回信息给templates里面的页面
#make_response用于创建自定义响应类 比默认的响应类Response更灵活
#request用于提取请求中用post或者get提交的参数

app = Flask(__name__)   #创建程序实例 即Flask类的对象

RSS_FEED = {
            "zhihu": "https://www.zhihu.com/rss",
            "netease": "http://news.163.com/special/00011K6L/rss_newsattitude.xml",
            "songshuhui": "http://songshuhui.net/feed",
            "ifeng": "http://news.ifeng.com/rss/index.xml"}     #可以选择的RSS网站

DEFAULTS = {'city': '北京',
            'publication': 'songshuhui'}    #默认的选择

WEATHERS = {"北京": 101010100,
            "上海": 101020100,
            "广州": 101280101,
            "深圳": 101280601}


#利用request获取参数 若参数为空则返回默认值
def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route('/')
def home():
    publication = get_value_with_fallback('publication')
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    articles = get_news(publication)

    # 此处创建自定义响应类，并利用render_template渲染templates中的模板，将数据传递过去
    response = make_response(render_template('home.html', articles=articles, weather=weather))
    expires = datetime.datetime.now() +datetime.timedelta(days=365)
    response.set_cookie('publication', publication, expires=expires)
    response.set_cookie('city', city, expires=expires)
    return response


def get_weather(city):
    code = WEATHERS.get('city', 101010100)
    url = "http://www.weather.com.cn/data/sk/{0}.html".format(code)

    r = requests.get(url)
    r.encoding = "utf-8"
    data = r.json()["weatherinfo"]
    return dict(city=data['city'], temperature=data['temp'], description=data['WD'])


def get_news(publication):
    feed = feedparser.parse(RSS_FEED[publication])      #对网页进行解析
    return feed['entries']      #返回一组文章条目 是list


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)