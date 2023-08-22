from app.model.models import User,Role
from .. import create_app
from .. import db


if __name__ == "__main__":

    app = create_app()

    with app.app_context():
        db.session.query(User).delete()
        db.session.query(Role).delete()

        role = Role(
            id = 1,
            permission_id = 1,
            permission_name= '考生',
            description = '参加考试，查阅成绩',
            create_time = 'Fri Aug  4 15:25:09 2023'
        )
        db.session.add(role)
        db.session.commit()

        role = Role(
            id=2,
            permission_id = 2,
            permission_name= '考官',
            description = '出题，批改试卷，试卷管理',
            create_time = 'Fri Aug  4 15:25:09 2023'
        )
        db.session.add(role)
        db.session.commit()

        role = Role(
            id=3,
            permission_id = 3,
            permission_name= '管理员',
            description = '系统管理',
            create_time = 'Fri Aug  4 15:25:09 2023'
        )
        db.session.add(role)
        db.session.commit()

        user = User(
            id = 1,
            account = 'admin',
            password = 'pbkdf2:sha256:600000$xP1yP8X4eNNMSJXx$1fcc68d4f609e71be2d991dc38a81f116b78850a2a98714fda65f534937aa1b0',
            permission_id = '3',
            email = 'admin@scut.edu.cn'
        )
        db.session.add(user)
        db.session.commit()

        user = User(
            id = 2,
            account = 'TA',
            password = 'pbkdf2:sha256:600000$xP1yP8X4eNNMSJXx$1fcc68d4f609e71be2d991dc38a81f116b78850a2a98714fda65f534937aa1b0',
            permission_id = '2',
            email = 'TA@scut.edu.cn'
        )
        db.session.add(user)
        db.session.commit()

