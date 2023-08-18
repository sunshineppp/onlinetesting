from app.api import testpaper_blueprint as bp
from app.model.models import Testpaper, TestpaperQuestion, Question, Answer
from app.utils import questionUtil, testpaperUtil
from app import db
from flask import request, jsonify
from time import strptime, strftime, localtime
from sqlalchemy import exc
from app.api.auth import token_auth, permission_require_teacher, permission_require_student

@token_auth.verify_token
@bp.route('/', methods = ('GET',))
@permission_require_student
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

@token_auth.verify_token
@bp.route('/info/<int:id>', methods=('GET',))
@permission_require_student
def getOnePaperInfo(id):
    paper = db.session.query(Testpaper).with_entities(
        Testpaper.id,
        Testpaper.duration,
        Testpaper.name,
        Testpaper.passline,
        Testpaper.created       
    ).filter(Testpaper.id == id).first()

    if paper is None: 
        return 'Testpaper not found', 404

    paper = dict(paper._mapping)

    questions = db.session.query(TestpaperQuestion.question_id).filter(
            TestpaperQuestion.testpaper_id == paper['id']
        ).all()
    questions = list(map(lambda q: q[0], questions))
    paper['questionID'] = list(questions)

    return jsonify(paper)
 
@token_auth.verify_token
@bp.route('/<int:id>', methods=('GET',))
@permission_require_student
def getOnePaper(id):
    try:
        paper = testpaperUtil.getPaperUtil(id)
    except Exception as e:
        return e.args

    return jsonify(paper)

@token_auth.verify_token
@bp.route('/edit', methods = ('POST',))
@permission_require_teacher
def createPaper():

    request_data = request.get_json()

    try:
        name, duration, question_ids = testpaperUtil.checkPaper(request_data)
    except Exception as e:
        return e.args
   
    created = strftime("%a, %d %b %Y %H:%M:%S", localtime())

    # total_point = 0.0

    # for question_id in question_ids:
    #     question = db.session.query(Question).filter(Question.id == question_id).first()
    #     total_point += question.point
    
    # passline = round(total_point * 0.6, 2)

    testpaper = Testpaper(
        duration = duration,
        name = name,
        created = created,
        # passline = passline
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

@token_auth.verify_token
@bp.route('/edit/<int:id>', methods=('POST',)) 
@permission_require_teacher
def modifyPaper(id):
    request_data = request.get_json()
    try: 
        name, duration, question_ids = testpaperUtil.checkPaper(request_data)
    except Exception as e:
        return e.args

    # total_point = 0.0

    # for question_id in question_ids:
    #     question = db.session.query(Question).filter(Question.id == question_id).first()
    #     total_point += question.point
    
    # passline = round(total_point * 0.6, 2)

    try:
        db.session.query(Testpaper).filter(Testpaper.id == id).update({
            Testpaper.name: name,
            Testpaper.duration: duration,
            # Testpaper.passline: passline
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

@token_auth.verify_token
@bp.route('/delete/<int:id>', methods=('DELETE',))
@permission_require_teacher
def deletePaper(id):
    # db.session.query(TestpaperQuestion).filter(TestpaperQuestion.testpaper_id == id).delete()
    db.session.query(Testpaper).filter(Testpaper.id == id).delete()
    db.session.commit()
    return 'delete success', 200