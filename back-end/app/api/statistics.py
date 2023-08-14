from app.api import statistics_blueprint as bp
from app import db
from app.model.models import UserExam, TestpaperQuestion, Question, Testpaper
from sqlalchemy.sql import func
from sqlalchemy import distinct
from flask import jsonify

# @bp.route('/user/<int:id>', methods=('GET',))
# def getUserStatistics():
    # 每场考试得分，总分，通过线，是否通过，答对题目数量/题目总数
    # pass


@bp.route('/exam/<int:id>', methods=('GET',))
def getExamStatistics(id):
    # 该考试基本信息，总分，通过线，参考人数，通过人数，未批改人数，平均分
    total_points = db.session.query(
            func.sum(Question.point)
        ).join(
            TestpaperQuestion, Question.id == TestpaperQuestion.question_id
        ).filter(TestpaperQuestion.testpaper_id == id).first()
    if total_points is None:
        return 'Testpaper not found', 404
    
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

    paper['fullPoints'] = total_points[0]

    total_number = db.session.query(
        func.count(distinct(UserExam.user_id))
    ).filter(UserExam.testpaper_id == id).first()[0]

    paper['totalNumber'] = total_number

    if total_number == 0:
        paper['passNumber'] = 0
        paper['avgPoints'] = 0
        paper['notProcessed'] = 0
    else:
        processed_list = db.session.query(UserExam.user_id, func.sum(UserExam.score)).group_by(UserExam.user_id).having(
            func.count(UserExam.score) == func.count(UserExam.id)
        ).filter(UserExam.testpaper_id == id).all()

        not_processed = total_number - len(processed_list)
        paper['notProcessed'] = not_processed

        avg_point = 0
        pass_number = 0

        if len(processed_list) == 0:
            pass
        else:
            for processed in processed_list:
                avg_point += processed[1]
                if processed[1] >= paper['passline']:
                    pass_number+=1
            avg_point = avg_point / len(processed_list)

        paper['passNumber'] = pass_number
        paper['avgPoint'] = avg_point

    return jsonify(paper)
