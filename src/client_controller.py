
from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for, flash, session, current_app
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from typing import Optional
from functools import wraps
import pytz
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import database as db

class Controller():

    """Quản lý các route của client"""
    
    def __init__(self):
        """Khởi tạo controller"""
        self.db_session = db.get_session()
        # self.news_model = NewsModel(self.db_session)
        # self.category_model = CategoryModel(self.db_session)
        # self.user_model = UserModel(self.db_session)
        # # Model cho tin tức quốc tế
        # self.int_news_model = InternationalNewsModel(self.db_session)
        # self.int_category_model = InternationalCategoryModel(self.db_session)

    def checkLogin(self, username, password, remember=False):
        """
        Check login for user
        """

        site = session.get('site')
        if site == 'en':
            categories = self.int_category_model.get_all()
        else:
            categories = self.category_model.get_all()
            
        # # Kiểm tra tài khoản bị khóa trước khi xác thực
        # if self.user_model.is_locked_user(username):
        #     if site == 'en':
        #         flash('Account has been locked. Please contact administrator', 'error')
        #         return redirect(url_for('client.en_user_login'))
        #     else:
        #         flash('Tài khoản đã bị khóa. Vui lòng liên hệ quản trị viên', 'error')
        #         return redirect(url_for('client.user_login'))
        
        # user = self.user_model.authenticate(username, password)
        
        # if user and user.is_active and user.role == db.UserRole.USER:
        #     session['user_id'] = user.id
        #     session['username'] = user.username
        #     session['full_name'] = user.full_name or user.username
        #     session['role'] = user.role.value
            
        #     flash('Đăng nhập thành công', 'success')
        #     return redirect(url_for('client.index'))
        # else:
        #     print('Tên đăng nhập hoặc mật khẩu không đúng')
        #     flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
        #     return redirect(url_for('client.user_login'))


    def register(self, site='vn'):
        """
        Trang đăng ký cho user
        Route: GET /register
        Route: POST /register
        """
        
        if site == 'en':
            categories = self.int_category_model.get_all()
        else:
            categories = self.category_model.get_all()
        
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip()
            
            from utils import validate_email, validate_password, validate_phone
            
            # Validation
            errors = []
            
            # Validate username
            if not username:
                errors.append('Tên đăng nhập không được để trống')
            elif len(username) < 3:
                errors.append('Tên đăng nhập phải có ít nhất 3 ký tự')
            elif self.user_model.get_by_username(username):
                errors.append('Tên đăng nhập đã tồn tại')
            
            # Validate email
            if not validate_email(email):
                errors.append('Email không đúng định dạng')
            elif self.user_model.get_by_email(email):
                errors.append('Email đã được sử dụng')
            
            # Validate phone
            phone_valid, phone_error = validate_phone(phone)
            if not phone_valid:
                errors.append(phone_error)
            
            # Validate password
            password_valid, password_error = validate_password(password)
            if not password_valid:
                errors.append(password_error)
            elif password != confirm_password:
                errors.append('Mật khẩu xác nhận không khớp')
            
            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                try:
                    # Clean phone number
                    phone_clean = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                    
                    user = self.user_model.create(
                        username=username,
                        email=email,
                        password=password,
                        full_name=full_name if full_name else None,
                        phone=phone_clean,
                        role=db.UserRole.USER
                    )
                    
                    flash('Đăng ký thành công! Vui lòng đăng nhập', 'success')
                    return redirect(url_for('client.user_login'))
                except Exception as e:
                    flash('Có lỗi xảy ra khi đăng ký. Vui lòng thử lại', 'error')
        
        return render_template(f'client/{site}/register.html', categories=categories)
