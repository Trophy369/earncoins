from flask_admin import BaseView, expose
from flask import url_for, redirect, Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import login_required, current_user
#from ..auth.models import Permission
#from flask.ext.admin import BaseView, expose


from ..decorators import has_role

#from .forms import CKTextAreaField
#
# admin_blueprint = Blueprint(
#     'admin',
#     __name__,
#     #template_folder='../templates/admin',
#     url_prefix="/admin"
# )
#
#
# class CustomView(BaseView):
#     @expose('/')
#     @login_required
#     @has_role('admin')
#     def index(self):
#         return self.render('admin/custom.html')

#     # @expose('/second_page')
#     # @login_required
#     # @permission_required(Permission.ADMIN)
#     # def second_page(self):
#     #     return self.render('admin/second_page.html')
#
#
# class AdminView(ModelView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('earncoins.home'))
#



# class PostView(CustomModelView):
#     form_overrides = dict(text=CKTextAreaField)
#     column_searchable_list = ('text', 'title')
#     column_filters = ('publish_date',)
#
#     create_template = 'admin/post_edit.html'
#     edit_template = 'admin/post_edit.html'


# class CustomFileAdmin(FileAdmin):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.has_role('admin')
