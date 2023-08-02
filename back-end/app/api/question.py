from app.api import question_blueprint as bp
from flask import request, jsonify
from app import db
from app.model.models import Question, Answer
from app.utils import util

@bp.route('/', methods = ('GET',))
def getQuestions():
    questions = db.session.query(Question).with_entities(
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
            Answer.correct,
        ).filter(Answer.question_id == question['id']).all()
        answers = list(map(lambda answer: dict(answer._mapping), answers))
        question['answers'] = answers

    return jsonify(questions)

@bp.route('/<int:id>', methods = ('GET',))
def getOneQuestion(id):
    question = db.session.query(Question).with_entities(
        Question.id,
        Question.content,
        Question.analysis,
        Question.type,
        Question.level,
        Question.point
    ).filter(Question.id == id).first()

    if question is None:
        return 'Question not found', 404
    else:
        question = util.convertQuestion(question)
        answers = db.session.query(Answer).with_entities(
            Answer.id,
            Answer.content,
            Answer.correct,
        ).filter(Answer.question_id == id).all()
        answers = list(map(lambda answer: dict(answer._mapping), answers))
        question['answers'] = answers
        return jsonify(question)
