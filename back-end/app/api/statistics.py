from app.api import st_bp as bp
from app import db
from app.model.models import UserExam, TestpaperQuestion, Question, Testpaper
from sqlalchemy.sql import func
from flask import jsonify

# @bp.route('/user/<int:id>', methods=('GET',))
# def getUserStatistics():
    # 每场考试得分，总分，通过线，是否通过，答对题目数量/题目总数
    # pass


@bp.route('/exam/<int:id>', methods=('GET',))
def getExamStatistics():
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

    paper['totalPoints'] = total_points

    total_number = db.session.query(
        func.count(UserExam.user_id)
    ).filter(UserExam.testpaper_id == id).first()

    paper['totalNumber'] = total_number

    if total_number == 0:
        paper['passNumber'] = 0
        paper['avgPoint'] = 0
        paper['notProcessed'] = 0
    else:
        query = db.session.query(UserExam).group_by(UserExam.user_id).filter(UserExam.score == -1)
        processed_list = db.session.query(
            UserExam.user_id.label('id'), func.sum(UserExam.score).label('score')
        ).group_by(UserExam.user_id).where(
            query.exists()
        ).all()
        not_processed = total_number - len(processed_list)
        avg_point = 0
        pass_number = 0

        for processed in processed_list:
            avg_point += processed['score']
            if processed['score'] >= paper['passline']:
                pass_number+=1
        avg_point = avg_point / len(processed_list)

        paper['passNumber'] = pass_number
        paper['avgPoint'] = avg_point
        paper['notProcessed'] = not_processed

    return jsonify(paper)
