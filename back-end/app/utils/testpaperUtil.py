from app import db
from app.model.models import Question, Answer, Testpaper, TestpaperQuestion, UserExam
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
    

def teacherGetPaperUtil(id,user_id):
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
            user_exams = db.session.query(UserExam).with_entities(
                UserExam.answer,
                UserExam.score
            ).filter(UserExam.testpaper_id==id).filter(UserExam.user_id==user_id)\
                .filter(UserExam.question_id == question['id']).all()
            user_exams = list(map(lambda user_exam: dict(user_exam._mapping), user_exams))
            question['user_exams'] = user_exams
        
        paper['questions'] = questions
        return paper