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

    return jsonify(papers)

@bp.route('/<int:id>', methods=('GET',))
def getOnePaper(id):
    try:
        paper = testpaperUtil.getPaperUtil(id)
    except Exception as e:
        return e.args

    return jsonify(paper)

@bp.route('/generate', methods = ('POST',))
def createPaper():

    request_data = request.get_json()
    
    try:
        duration = request_data['duration'] 
        name = request_data['name']
    except KeyError:
        return 'Test paper info missing', 400

    if None not in (duration, name):
        pass
    else:
        return 'Test paper info missing', 400

    try:
        strptime(duration, "%H:%M:%S")
    except ValueError:
        return 'Test duration format is wrong', 400
    
    created = strftime("%a, %d %b %Y %H:%M:%S", localtime())

    # question_ids = generate_questions()

    question_ids = [1, 2, 3]   

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
