from app.api import testpaper_blueprint as bp
from app.model.models import Testpaper, TestpaperQuestion, Question, Answer
from app.utils import util
from app import db
from flask import request, jsonify

@bp.route('/', methods = ('GET',))
def getPapers():
    papers = db.session.query(Testpaper).with_entities(
        Testpaper.id,
        Testpaper.duration,
        Testpaper.name,
        Testpaper.passline,
        Testpaper.created
    ).all()

    papers = list(map(lambda paper: dict(paper._mapping), papers))

    return jsonify(papers)

@bp.route('/<int:id>', methods=('GET',))
def getOnePaper(id):
    paper = db.session.query(Testpaper).with_entities(
        Testpaper.id,
        Testpaper.duration,
        Testpaper.name,
        Testpaper.passline,
        Testpaper.created
    ).filter(Testpaper.id == id).first()

    if paper is None:
        return 'Testpaper not found', 404
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
        questions = list(map(util.convertQuestion, questions))

        for question in questions:
            answers = db.session.query(Answer).with_entities(
                Answer.id,
                Answer.content,
                Answer.correct
            ).filter(Answer.question_id == question['id']).all()
            answers = list(map(lambda answer: dict(answer._mapping), answers))
            question['answers'] = answers
        
        paper['questions'] = questions
        return jsonify(paper)





