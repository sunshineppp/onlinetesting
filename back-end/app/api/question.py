from app.api import question_blueprint as bp
from flask import request, jsonify
from app import db
from app.model.models import Question, Answer
from app.utils import questionUtil
from sqlalchemy import exc

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
    questions = list(map(questionUtil.convertQuestion, questions))
    
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
        question = questionUtil.convertQuestion(question)
        answers = db.session.query(Answer).with_entities(
            Answer.id,
            Answer.content,
            Answer.correct,
        ).filter(Answer.question_id == id).all()
        answers = list(map(lambda answer: dict(answer._mapping), answers))
        question['answers'] = answers
        return jsonify(question)

@bp.route('/create', methods = ('POST',))
def createQuestion():
    request_data = request.get_json()

    try:
        question, answers = questionUtil.checkQuestion(request_data)
    except Exception as e:
        return e.args

    try:
        db.session.add(question)
    except exc.SQLAlchemyError:
        return 'failed to add questions', 400

    db.session.flush()
    question_id = question.id
   
    for answer in answers:
        answer.question_id = question_id
        try:  
            db.session.add(answer)
        except exc.SQLAlchemyError:
            return 'failed to add questions', 400
    
    db.session.commit()

    return 'Add question success', 200

@bp.route('/delete/<int:id>', methods = ('DELETE',))
def deleteQuestion(id):
    db.session.query(Answer).filter(Answer.question_id == id).delete()
    db.session.query(Question).filter(Question.id == id).delete()
    db.session.commit()
    return 'delete success', 200

@bp.route('/update/<int:id>', methods=('POST',))
def updateQuestion(id):
    request_data = request.get_json()
    try:
        question, answers = questionUtil.checkQuestion(request_data, check_id=True)
    except Exception as e:
        return e.args
    
    try:
        db.session.query(Question).filter(Question.id == id).update({
                Question.content: question.content,
                Question.analysis: question.analysis,
                Question.type: question.type,
                Question.level: question.level,
                Question.point: question.point
            })
    except exc.SQLAlchemyError:
        return 'failed to update questions', 400

    for answer in answers:
        try:  
            db.session.query(Answer).filter(Answer.id == answer.id).update({
                Answer.content: answer.content,
                Answer.correct: answer.correct,
            })
        except exc.SQLAlchemyError:
            return 'failed to add questions', 400
    
    db.session.commit()

    return 'update success', 200