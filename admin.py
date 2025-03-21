from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, Select2Widget
from flask_admin.menu import MenuLink
from flask_login import current_user
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_admin.model import InlineFormAdmin
from config import Config
from models import  User,Player,PlayerImg, db


# Кастомна головна сторінка адмінки
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return super().index()


# Обмежений доступ до адмінки
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class UserAdmin(AdminModelView):
    column_list = ["id", "username","counter"]
    column_labels = {"username": "Логін"}
    can_edit = False  # Вимикаємо можливість редагування
    can_create = False  # Вимикаємо можливість створення нових користувачів
    can_view_details = True  # Дозволяємо перегляд користувача




class PlayerAdmin(ModelView):
    column_list = ['id', 'name', 'ac', 'speed', 'init', 'hp_max', 'hp', 'lv', 'user_id']
    column_labels = {
        'name': "Ім'я",
        'ac': "КБ",
        'speed': "Швидкість",
        'init': "Ініціатива",
        'hp_max': "Макс. Здоров'я",
        'hp': "Поточне Здоров'я",
        'lv': "Рівень",
        'user_id': "ID Користувача"
    }
    form_columns = ['name', 'ac', 'speed', 'init', 'hp_max', 'hp', 'lv', 'user_id']
    column_searchable_list = ['name']
    column_filters = ['lv', 'ac','user_id']
 

class PlayerImgAdmin(ModelView):
    column_list = ['id', 'filename', 'player_img_id']
    column_labels = {
        'filename': "Назва файлу",
        'player_img_id': "ID Персонажа"
    }
    form_columns = ['filename', 'player_img_id']
    column_searchable_list = ['filename']
    can_edit = False  # Вимикаємо можливість редагування
    can_create = False  # Вимикаємо можливість створення нових користувачів
    can_view_details = True 
# Створюємо об'єкт адмінки
admin = Admin(
    name="Адмінка",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),
)

admin.add_link(MenuLink(name="🏠 Перейти до енкаунтуру", url="/"))
admin.add_link(MenuLink(name="🚪 Вийти", url="/logout"))
admin.add_view(PlayerAdmin(Player, db.session, name='Персонажі', endpoint='players'))

admin.add_view(PlayerImgAdmin(PlayerImg, db.session, name='Зображення', endpoint='player_images'))
admin.add_view(UserAdmin(User, db.session, name="Користувачі"))