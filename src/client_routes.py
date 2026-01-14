
"""
client router - define routes for client
"""

from flask import Blueprint, render_template, request, jsonify, abort, make_response

import base
import client_controller
import json


# Create Blueprint for client with url_prefix is empty to redirect route
# and template_folder for html files in folder client
client_bp = Blueprint('client', __name__, 
                     url_prefix='',
                     template_folder='templates')


controller = client_controller.Controller


class Home(base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        
        values = {
            'title': 'News - Page News' if site == 'en' else 'News - Trang Tin Tức',
            'site': site
        }
        return render_template('client/home.html', **values)


class Search(base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        
        values = {
            'title': 'News - Page News' if site == 'en' else 'News - Trang Tin Tức',
            'site': site
        }
        return render_template('client/search.html', **values)


class Category(base.BaseView):
    
    def get(self, category_slug):
        
        site = request.args.get('site', 'vn')
        
        values = {
            'title': 'News - Page News' if site == 'en' else 'News - Trang Tin Tức',
            'site': site,
            'category': category_slug
        }
        return render_template('client/category.html', **values)


class Categories(base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 10)
        
        data = {
            'success': True,
            'data': [],
        }
        
        jsondata = json.JSONEncoder().encode(data)
        
        return jsondata


class NewsDetail(base.BaseView):
    
    def get(self, news_slug):
        
        site = request.args.get('site', 'vn')
        
        values = {
            'title': 'News - Page News' if site == 'en' else 'News - Trang Tin Tức',
            'site': site,
        }
        return render_template('client/news_detail.html', **values)


class LatestNews(base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 10)
        
        data = {
            'success': True,
            'data': [],
        }
        
        jsondata = json.JSONEncoder().encode(data)
        
        return jsondata


class FeaturedNews(base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 10)
        
        data = {
            'success': True,
            'data': [],
        }
        
        jsondata = json.JSONEncoder().encode(data)
        
        return jsondata


class HotNews(base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        
        data = {
            'success': True,
            'data': [],
        }
        
        jsondata = json.JSONEncoder().encode(data)
        
        return jsondata


class Login(controller, base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
 
        if site == 'en':
            categories = self.int_category_model.get_all()
        else:
            categories = self.category_model.get_all()

        values = {
            'title': 'News - Page News' if site == 'en' else 'News - Trang Tin Tức',
            'site': site,
            'categories': categories
        }
        return render_template('client/login.html', **values)
    
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') == 'on' else False

        self.checkLogin(username, password, remember=remember)


class Register(controller, base.BaseView):
    
    def get(self):
        
        site = request.args.get('site', 'vn')
        
        values = {
            'title': 'News - Page News' if site == 'en' else 'News - Trang Tin Tức',
            'site': site,
        }
        return render_template('client/login.html', **values)
    
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') == 'on' else False

        self.checkLogin(username, password, remember=remember)


class Introducing(base.BaseView):
    
    def get(self):
        pass


class Security(base.BaseView):
    
    def get(self):
        pass


class Term(base.BaseView):
    
    def get(self):
        pass


class Contact(base.BaseView):
    
    def get(self):
        pass


class Guide(base.BaseView):
    
    def get(self):
        pass


client_bp.add_url_rule('/', 'home0', Home.as_view('home0'))
client_bp.add_url_rule('/home', 'home1', Home.as_view('home1'))
client_bp.add_url_rule('/search', 'search', Search.as_view('search'))
client_bp.add_url_rule('/category/<category_slug>', 'category', Category.as_view('category'))
client_bp.add_url_rule('/category/list', 'category_list', Categories.as_view('category_list'))
client_bp.add_url_rule('/news/<news_slug>', 'news', NewsDetail.as_view('news'))
client_bp.add_url_rule('/latest-news', 'latestnews', LatestNews.as_view('latestnews'))
client_bp.add_url_rule('/featured-news', 'featurednews', FeaturedNews.as_view('featurednews'))
client_bp.add_url_rule('/hot-news', 'hotnews', HotNews.as_view('hotnews'))
client_bp.add_url_rule('/signin', 'login', Login.as_view('login'))
client_bp.add_url_rule('/signup', 'register', Login.as_view('register'))
client_bp.add_url_rule('/introducing', 'introducing', Introducing.as_view('introducing'))
client_bp.add_url_rule('/security', 'security', Security.as_view('security'))
client_bp.add_url_rule('/term', 'term_of_service', Term.as_view('term_of_service'))
client_bp.add_url_rule('/contact', 'contact', Contact.as_view('contact'))
client_bp.add_url_rule('/guide', 'guide', Guide.as_view('guide'))
