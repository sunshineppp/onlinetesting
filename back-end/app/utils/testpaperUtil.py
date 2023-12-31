from app import db
from app.model.models import Question, Answer, Testpaper, TestpaperQuestion, UserExam
from app.utils import questionUtil
from time import strptime


def checkPaper(request_data):
    try:
        duration = request_data['duration']
        name = request_data['name']
        question_ids = request_data['questionID']
    except KeyError:
        raise Exception('Test paper info missing', 400)

    if None not in (duration, name):
        pass
    else:
        raise Exception('Test paper info missing', 400)

    try:
        strptime(duration, "%H:%M:%S")
    except ValueError:
        raise Exception('Test duration format is wrong', 400)

    if len(question_ids) == 0:
        raise Exception('There is no question in the test paper', 400)

    return name, duration, question_ids
 

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
            if question['type'] != 'shortAnswer':
                for user_exam in user_exams:
                    if user_exam['answer']:
                        answer_content =  db.session.query(Answer.content).filter(Answer.id == int(user_exam['answer'],10)).first()
                        user_exam['answer_content'] = answer_content[0]
                    else:
                        user_exam['answer_content'] = ''
            print(user_exams)
            question['user_exams'] = user_exams
        
        paper['questions'] = questions
        return paper