from app import db
from app.model.models import Question, Answer, Testpaper, TestpaperQuestion
from app.utils import questionUtil

def getPaperUtil(id):
    paper = db.session.query(Testpaper).with_entities(
        Testpaper.id,
        Testpaper.duration,
        Testpaper.name,
        Testpaper.passline,
        Testpaper.created
    ).filter(Testpaper.id == id).first()

    if paper is None:
        raise Exception('Testpaper not found', 404)
    else:
        paper = dict(paper._mapping)
        questions = db.session.query(TestpaperQuestion).join(
            Question,
            TestpaperQuestion.question_id == Question.id).filter(
                TestpaperQuestion.testpaper_id == id
            ).with_entities(
                Question.id,
                Question.content,
                Question.analysis,
                Question.type, 
                Question.level,
                Question.point
            ).all()
        questions = list(map(questionUtil.convertQuestion, questions))

        for question in questions:
            answers = db.session.query(Answer).with_entities(
                Answer.id,
                Answer.content,
                Answer.correct
            ).filter(Answer.question_id == question['id']).all()
            answers = list(map(lambda answer: dict(answer._mapping), answers))
            question['answers'] = answers
        
        paper['questions'] = questions
        return paper