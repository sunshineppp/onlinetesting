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
            account = 'zwt',
            password = 'pbkdf2:sha256:600000$UAv1BWz0LibA6cpA$7f658dc8f34dd2db4759be70ea92e05f49e4fdbe24680d7aaaabe69859872253',
            permission_id = '3',
            email = 'zwt@qq.com'
        )
        db.session.add(user)
        db.session.commit()

        user = User(
            id = 2,
            account = 'zwt1',
            password = 'pbkdf2:sha256:600000$UAv1BWz0LibA6cpA$7f658dc8f34dd2db4759be70ea92e05f49e4fdbe24680d7aaaabe69859872253',
            permission_id = '2',
            email = 'zwt1@qq.com'
        )
        db.session.add(user)
        db.session.commit()

