from app.api import testpaper_blueprint as bp
from app.model.models import Testpaper, TestpaperQuestion, Question, Answer
from app.utils import questionUtil, testpaperUtil
from app import db
from flask import request, jsonify
from time import strptime, strftime, localtime
from sqlalchemy import exc

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

    for paper in papers:
        questions = db.session.query(TestpaperQuestion.question_id).filter(
                TestpaperQuestion.testpaper_id == paper['id']
            ).all()
        questions = list(map(lambda q: q[0], questions))
        paper['questionID'] = list(questions)

    return jsonify(papers)

@bp.route('/<int:id>', methods=('GET',))
def getOnePaper(id):
    try:
        paper = testpaperUtil.getPaperUtil(id)
    except Exception as e:
        return e.args

    return jsonify(paper)

@bp.route('/edit', methods = ('POST',))
def createPaper():

    request_data = request.get_json()

    try:
        name, duration, question_ids = testpaperUtil.checkPaper(request_data)
    except Exception as e:
        return e.args
   
    created = strftime("%a, %d %b %Y %H:%M:%S", localtime())

    total_point = 0.0

    for question_id in question_ids:
        question = db.session.query(Question).filter(Question.id == question_id).first()
        total_point += question.point
    
    passline = total_point * 0.6

    testpaper = Testpaper(
        duration = duration,
        name = name,
        created = created,
        passline = passline
    )

    try:
        db.session.add(testpaper)
    except exc.SQLAlchemyError:
        return 'failed to add test paper', 400
    
    db.session.flush()
    testpaper_id = testpaper.id

    for question_id in question_ids:
        testpaperQuestion = TestpaperQuestion(
            question_id = question_id,
            testpaper_id = testpaper_id
        )
        try:
            db.session.add(testpaperQuestion)
        except exc.SQLAlchemyError:
            return 'failed to add test paper', 400
    
    db.session.commit()

    try:
        paper = testpaperUtil.getPaperUtil(testpaper_id)
    except Exception as e:
        return e.args
    
    return jsonify(paper)

@bp.route('/edit/<int:id>', methods=('POST',)) 
def modifyPaper(id):
    request_data = request.get_json()
    try: 
        name, duration, question_ids = testpaperUtil.checkPaper(request_data)
    except Exception as e:
        return e.args

    total_point = 0.0

    for question_id in question_ids:
        question = db.session.query(Question).filter(Question.id == question_id).first()
        total_point += question.point
    
    passline = total_point * 0.6

    try:
        db.session.query(Testpaper).filter(Testpaper.id == id).update({
            Testpaper.name: name,
            Testpaper.duration: duration,
            Testpaper.passline: passline
        })
        db.session.query(TestpaperQuestion).filter(TestpaperQuestion.testpaper_id == id).delete()
    except exc.SQLAlchemyError:
        return 'failed to update test paper', 400
    
    for question_id in question_ids:
        testpaperQuestion = TestpaperQuestion(
            question_id = question_id,
            testpaper_id = id
        )
        try:
            db.session.add(testpaperQuestion)
        except exc.SQLAlchemyError:
            return 'failed to update test paper', 400

    db.session.commit() 

    return '', 200


@bp.route('/delete/<int:id>', methods=('DELETE',))
def deletePaper(id):
    db.session.query(TestpaperQuestion).filter(TestpaperQuestion.testpaper_id == id).delete()
    db.session.query(Testpaper).filter(Testpaper.id == id).delete()
    db.session.commit()
    return 'delete success', 200