from app.model.models import Question, Answer, Testpaper, TestpaperQuestion
from sqlalchemy import exc
from .. import create_app
from .. import db
import time
import datetime

if __name__ == "__main__":

    app = create_app()

    with app.app_context():

        db.session.query(Question).delete()
        db.session.query(Answer).delete()

        question = Question(
            id = 1,
            content = "Question 1: balabalabalabala, choose the answer from A. B. C. D.",
            analysis = "if else then balabala the answer is B",
            type = "singleChoice",
            level = "easy",
            point = 5.0
        )

        db.session.add(question)
        db.session.commit()

        answer = Answer(
            id = 1,
            content = "A. XXXXX",
            correct = 0,
            question_id = 1
        )
        db.session.add(answer)
        answer = Answer(
            id = 2,
            content = "B. XXXXX",
            correct = 1,
            question_id = 1,
        )
        db.session.add(answer)
        answer = Answer(
            id = 3,
            content = "C. XXXXX",
            correct = 0,
            question_id = 1,
        )
        db.session.add(answer)
        answer = Answer(
            id = 4,
            content = "D. XXXXX",
            correct = 0,
            question_id = 1,
        )
        db.session.add(answer)
        db.session.commit()

        question = Question(
            id = 2,
            content = "Question 2: judge whether the following statement is correct",
            analysis = "because ......, the answer is false",
            type = "trueOrFalse",
            level = "medium",
            point = 4.0
        )
        db.session.add(question)
        db.session.commit()

        answer = Answer(
            id = 5,
            content = "True",
            correct = 0,
            question_id = 2
        )
        db.session.add(answer)

        answer = Answer(
            id = 6,
            content = "False",
            correct = 1,
            question_id = 2
        )
        db.session.add(answer)
        db.session.commit()

        question = Question(
            id = 3,
            content = "Question 3: please briefly describe the principle of xxx",
            analysis = "According to zzzzzz, the principle of xxx can be stated as follows: yyyyyyyy",
            type = "shortAnswer",
            level = "hard",
            point = 10.0
        )
        db.session.add(question)
        db.session.commit()

        answer = Answer(
            id = 7,
            content = "The principle of xxx is yyyyyyy",
            correct = 1,
            question_id = 3
        )
        db.session.add(answer)
        db.session.commit()


        # answer = db.session.query(Answer).join(Question, Answer.question_id == Question.id) \
        #     .with_entities(Question.content.label('qcontent'), Question.analysis, Question.point, Answer.content.label('acontent')).first()
        
        # print(answer._mapping)

        
        # testpaper = Testpaper(
        #     name = 'data structure test',
        #     passline = 60.0,
        #     duration = '2:00:00'
        # )

        # db.session.add(testpaper)
        # db.session.commit()

        # papers = db.session.query(Testpaper).all()
        # for paper in papers:
        #     print(paper.name)
        #     print(paper.passline)
        #     print(paper.duration)