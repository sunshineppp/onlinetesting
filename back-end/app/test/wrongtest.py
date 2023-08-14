from app.model.models import User,Role,UserExam
from .. import create_app
from .. import db
import time


if __name__ == "__main__":

    app = create_app()

    with app.app_context():

        db.session.query(UserExam).delete()
        db.session.commit()

        user = UserExam(
            id = 1,
            user_id = 1,
            testpaper_id = 1,
            question_id = 1,
            answer = '2',
            correct = True,
            score = 5.0,
            exam_time = time.asctime(time.localtime())
        )
        db.session.add(user)
        db.session.commit()

        user = UserExam(
            id = 2,
            user_id = 1,
            testpaper_id = 1,
            question_id = 2,
            answer = '5',
            correct = False,
            score = 0,
            exam_time = time.asctime(time.localtime())
        )
        db.session.add(user)
        db.session.commit()

        user = UserExam(
            id = 3,
            user_id = 1,
            testpaper_id = 1,
            question_id = 3,
            answer = 'Afawuifiuafuiahuifhawifawfawfawfa',
            exam_time = time.asctime(time.localtime())
        )
        db.session.add(user)
        db.session.commit()



        user = UserExam(
            id = 4,
            user_id = 1,
            testpaper_id = 2,
            question_id = 2,
            answer = '6',
            correct = True,
            score = 5.0,
            exam_time = time.asctime(time.localtime())
        )
        db.session.add(user)
        db.session.commit()

        user = UserExam(
            id = 5,
            user_id = 1,
            testpaper_id = 2,
            question_id = 3,
            answer = 'Aawdawbdawbdawbdiabwdibawidbiawbdiawawd',
            correct = False,
            score = 9.0,
            exam_time = time.asctime(time.localtime())
        )
        db.session.add(user)
        db.session.commit()



        # user = UserExam(
        #     id = 6,
        #     user_id = 1,
        #     testpaper_id = 1,
        #     question_id = 4,
        #     answer = 'A',
        #     correct = True,
        #     score = 7.0,
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 1,
        #     testpaper_id = 2,
        #     question_id = 4,
        #     answer = 'A',
        #     correct = True,
        #     score = 7.0,
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 1,
        #     testpaper_id = 2,
        #     question_id = 4,
        #     answer = 'A',
        #     correct = True,
        #     score = 7.0,
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 1,
        #     testpaper_id = 2,
        #     question_id = 4,
        #     answer = 'A',
        #     correct = False,
        #     score = 7.0,
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 2,
        #     testpaper_id = 2,
        #     question_id = 4,
        #     answer = 'A',
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 1,
        #     testpaper_id = 2,
        #     question_id = 4,
        #     answer = 'A',
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 1,
        #     testpaper_id = 3,
        #     question_id = 4,
        #     answer = 'A',
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 1,
        #     testpaper_id = 4,
        #     question_id = 4,
        #     answer = 'A',
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        # user = UserExam(
        #     user_id = 2,
        #     testpaper_id = 4,
        #     question_id = 4,
        #     answer = 'A',
        #     exam_time = time.asctime(time.localtime())
        # )
        # db.session.add(user)
        # db.session.commit()

        