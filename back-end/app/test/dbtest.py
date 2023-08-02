from ..models import Question, Answer, Testpaper, TestpaperQuestion
from sqlalchemy import exc
from .. import create_app
from .. import db
import time
import datetime

if __name__ == "__main__":

    app = create_app()

    with app.app_context():

        # question = Question(
        #     content = "Question 1",
        #     analysis = "if else then answer is balabala",
        #     type = "choice",
        #     level = "easy",
        #     point = 5.0
        # )

        # db.session.add(question)
        # db.session.commit()

        # answer = Answer(
        #     content = "A. XXXXX",
        #     correct = 0,
        #     question_id = 1
        # )
        # db.session.add(answer)
        # db.session.commit()

        # answer = db.session.query(Answer).join(Question, Answer.question_id == Question.id) \
        #     .with_entities(Question.content.label('qcontent'), Question.analysis, Question.point, Answer.content.label('acontent')).first()
        
        # print(answer._mapping)

        
        testpaper = Testpaper(
            name = 'data structure test',
            passline = 60.0,
            duration = '2:00:00'
        )

        db.session.add(testpaper)
        db.session.commit()

        papers = db.session.query(Testpaper).all()
        for paper in papers:
            print(paper.name)
            print(paper.passline)
            print(paper.duration)