from app.model.models import Question, Answer, Testpaper, TestpaperQuestion
from sqlalchemy import exc
from .. import create_app
from .. import db
from datetime import timedelta
from time import localtime, strftime

if __name__ == "__main__":

    app = create_app()

    with app.app_context():

        db.session.query(Question).delete()
        db.session.query(Answer).delete()
        db.session.query(Testpaper).delete()
        db.session.query(TestpaperQuestion).delete()

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

        paper = Testpaper(
            id = 1,
            duration = str(timedelta(hours=2, minutes=30)),
            name = 'Test 1',
            passline = 5.4,
            created = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        )

        db.session.add(paper)
        db.session.commit()

        paperQuestion = TestpaperQuestion(
            id = 1,
            question_id = 1,
            testpaper_id = 1,
        )
        db.session.add(paperQuestion)
        
        paperQuestion = TestpaperQuestion(
            id = 2,
            question_id = 2,
            testpaper_id = 1
        )
        db.session.add(paperQuestion)
        db.session.commit()

        paper = Testpaper(
            id = 2,
            duration = str(timedelta(hours=2)),
            name = 'Test 2',
            passline = 8.4,
            created = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        )
        
        db.session.add(paper)
        db.session.commit()

        paperQuestion = TestpaperQuestion(
            id = 3,
            question_id = 2,
            testpaper_id = 2,
        )
        db.session.add(paperQuestion)
        
        paperQuestion = TestpaperQuestion(
            id = 4,
            question_id = 3,
            testpaper_id = 2
        )
        db.session.add(paperQuestion)
        db.session.commit()

