from app import db, login_manager
from app.models.auth import (
    User,
)  # noqa


# Менеждер загрузки пользователей
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
