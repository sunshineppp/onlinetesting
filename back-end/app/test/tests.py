from app.model.enums import QuestionLevel, AnswerCorrect
from datetime import timedelta
from time import localtime, strftime, strptime
from app import db
from app.model.models import Question, TestpaperQuestion, UserExam
from sqlalchemy.sql import func, null
from sqlalchemy import case
from .. import create_app

if __name__ == "__main__":
    # created = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    # duration = str(timedelta(hours=2, minutes=30))
    # print(created)
    # print(duration)

    # duration = "20:00:00"

    # try:
    #     success = strptime(duration, "%H:%M:%S")
    # except ValueError:
    #     print('fuck')
    app = create_app()
    with app.app_context():
        q = db.session.query(UserExam.user_id, func.sum(UserExam.score)).group_by(UserExam.user_id).having(
            func.count(UserExam.score) == func.count(UserExam.id)
        ).filter(UserExam.testpaper_id == 2)
        print(q.all())
