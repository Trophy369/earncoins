# from flask_admin import BaseView, expose, Admin
# from flask import url_for, redirect, request
# #from flask_admin.contrib.sqla import ModelView
# #from flask_admin.contrib.fileadmin import FileAdmin
# from flask_login import login_required, current_user
# #from ..auth.models import Permission
# #from flask.ext.admin import BaseView, expose
#
# from ..decorators import has_role
#
# #from flask_admin import Admin
# from .. import db
# #from webapp.auth.models import Post, Comment, Reminder, Tag
# from flask_admin import Admin, expose, BaseView, AdminIndexView
# from flask_admin.contrib.sqla import ModelView
# from ..auth.models import User, Role
#
#
# # class CustomView(BaseView):
# #     @expose('/')
# #     @login_required
# #     @has_role('admin')
# #     def index(self):
# #         return self.render('admin/custom.html')
#
#     # @expose('/second_page')
#     # @login_required
#     # @permission_required(Permission.ADMIN)
#     # def second_page(self):
#     #     return self.render('admin/second_page.html')
#
#
# # class AdminView(ModelView):
# #     def is_accessible(self):
# #         return current_user.has_role('admin')
# #
# #     def inaccessible_callback(self, name, **kwargs):
# #         return redirect(url_for('auth.login', next=request.url))
#
#
#
#
# admin = Admin('Admin area', index_view=HomeAdminView())
#
#
# def create_module(app, **kwargs):
#
#     admin.init_app(app)
#     from webapp.auth.models import User, Referrer, Role, Transactions, Investments
#     admin.add_view(ModelView(User, db.session))
#     admin.add_view(ModelView(Referrer, db.session))
#     admin.add_view(ModelView(Role, db.session))
#     admin.add_view(ModelView(Transactions, db.session))
#     admin.add_view(ModelView(Investments, db.session))
#
#
#
