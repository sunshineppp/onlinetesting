from app.api import wqb
from flask import request, jsonify, url_for, g
from sqlalchemy import func
from app import db
from app.api.errors import bad_request,bad_response
from app.model.models import UserExam,Testpaper,Question,TestpaperQuestion,Answer,User
from app.model.enums import QuestionType
from app.api.auth import token_auth,permission_require
import re
from app.api.auth import permission_require_student,permission_require_teacher
from app.api.errors import bad_request
import time
from app.utils import questionUtil, testpaperUtil

def get_exam_total(qs):
        exam_score = db.session.query(func.sum(Question.point)).filter(Question.id.in_(qs)).all()
        exam_score = exam_score[0][0]
        return exam_score




@token_auth.verify_token
@wqb.route('/myExamScore', methods=['GET'])#学生成绩界面
@permission_require_student
def wrong():
    # data = request.get_json()
    # question_id = data.get('question_list')
    # question_id = question_id.split(",")
    # userexam = db.session.query(UserExam.testpaper_id,func.sum(UserExam.score)).filter(UserExam.user_id==1)\
    # .filter(UserExam.testpaper_id==1).filter(UserExam.correct == 1).all()
    userexams = db.session.query(UserExam.testpaper_id).filter(UserExam.user_id==g.user_id)\
        .group_by(UserExam.testpaper_id).all() #.filter(UserExam.correct == 1)
    if userexams is None:
        return 'no exam',208
    # print(userexams)
    all_exam=[]
    for userexam in userexams:
        exam_time = db.session.query(UserExam.exam_time).filter(UserExam.user_id==g.user_id)\
            .filter(UserExam.testpaper_id== userexam[0]).first()
        # print(exam_time)
        questions = db.session.query(TestpaperQuestion.question_id)\
            .filter(TestpaperQuestion.testpaper_id==userexam[0]).all()
        qs=[]#试卷题集合
        for question in questions:
            qs.append(question[0])
        exam = db.session.query(Testpaper.name,Testpaper.passline).filter(Testpaper.id == userexam[0]).first()
        # print(exam) #试卷名，试卷及格分
        # exam_score = db.session.query(func.sum(Question.point)).filter(Question.id.in_(qs)).all()
        # exam_score = exam_score[0][0]
        exam_score = get_exam_total(qs)
        # print(exam_score)#试卷总分

        #是否完成批改
        user_exam = db.session.query(UserExam).filter(UserExam.user_id == g.user_id)\
            .filter(UserExam.testpaper_id == userexam[0]).filter(UserExam.correct == None).first()
        if user_exam is None:
            get_score = db.session.query(func.sum(UserExam.score)).filter(UserExam.user_id==g.user_id)\
                .filter(UserExam.testpaper_id == userexam[0]).all()
            # print(get_score)
            score = get_score[0][0]
        else:
            score = -1
        
        if score > exam[1]:
            pass_or_not = '合格'
        elif score < 0:
            pass_or_not = '已交卷'
        else:
            pass_or_not = '不合格'
        
        data = {
            'exam_id': userexam[0],
            'exam_name': exam[0],
            'exam_total_score':exam_score,
            'exam_pass_score':exam[1],
            'score':score,
            'pass_or_not':pass_or_not,
            'exam_time':exam_time[0]
        }
        print(data)
        all_exam.append(data)

    return jsonify(all_exam)




@token_auth.verify_token
@wqb.route('/myExam', methods=['POST'])#学生提交试卷
@permission_require_student
def create_exam():
    data = request.get_json()

    message={}
    # if 'user_id' not in data or not data.get('user_id', None):
    #     message['user_id'] = 'Please provide user_id.'
    if 'exam_id' not in data or not data.get('exam_id', None):
        message['exam_id'] = 'Please provide exam_id.'
    if 'questions' not in data or not data.get('questions', None):
         message['questions'] = 'Please provide questions.'
    if message:
        return bad_response(message)
    
    if db.session.query(UserExam).filter(UserExam.user_id == g.user_id)\
        .filter(UserExam.testpaper_id == data.get('exam_id')).first():
        return bad_request('请勿重复提交试卷')
    
    questions = data.get('questions')

    for question in questions:
        if 'question_id' not in question or not question.get('question_id', None):
            message['question_id'] = 'Please provide question_id.'
        if 'answer' not in question:
            message['answer'] = 'Please provide answer.'
        if 'type' not in question:
            message['type'] = 'Please provide type.'

        if message:
            return bad_request(message)
        
        try:
            userexam = UserExam()
            userexam.exam_time = time.asctime(time. localtime())
            # time_tuple = time.localtime(time.time())
            # create_time = "{}年{}月{}日{}点{}分".format(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3],time_tuple[4])
            # userexam.exam_time = create_time
            userexam.testpaper_id = data.get('exam_id')
            userexam.from_dict(question)
            userexam.user_id = g.user_id
            type = question.get('type')

            if type == QuestionType.singleChoice.name or type == QuestionType.trueOrFalse.name:
                answer = question.get('answer')
                if answer:
                    question_id = question.get('question_id')
                    correct = db.session.query(Answer.correct).filter(Answer.id == int(answer,10))\
                    .filter(Answer.question_id == question_id).first()
                    correct = correct[0]
                    if correct == 1:
                        userexam.correct = True
                        score = db.session.query(Question.point).filter(Question.id == question_id).first()
                        userexam.score = score[0]
                else:
                    userexam.correct = False
                    userexam.score =  0
            # print(userexam.to_dict())
            db.session.add(userexam)
        except Exception as e:
            print(e)
            return bad_response('System maintenance')
        
    db.session.commit()
    
    return 'Submit the test paper successfully'



@token_auth.verify_token
@wqb.route('/teacherCorrect', methods=['GET'])#老师批改界面
@permission_require_teacher
def get_paper():
    papers = {}
    paper=[]

    testpapers = db.session.query(UserExam.testpaper_id,UserExam.user_id,UserExam.exam_time)\
        .filter(UserExam.correct == None).group_by(UserExam.testpaper_id,UserExam.user_id).all()
    print(testpapers)

    if testpapers is None:
        return '没有可批改的试卷',208
    try:
        for testpaper in testpapers:
            questions = db.session.query(TestpaperQuestion.question_id)\
                .filter(TestpaperQuestion.testpaper_id==testpaper[0]).all()
            qs=[]#试卷题集合
            for question in questions:
                qs.append(question[0])

            #试卷名，试卷及格分
            exam = db.session.query(Testpaper.name,Testpaper.passline).filter(Testpaper.id == testpaper[0]).first()
            print(exam)
            #试卷总分
            exam_score = get_exam_total(qs)
            #答题人
            username = db.session.query(User.account).filter(User.id == testpaper[1]).first()
            data = {
                'username' : username[0],
                'exam_name': exam[0],
                'exam_total_score':exam_score,
                'exam_pass_score':exam[1],
                'exam_time': testpaper[2],
                'testpaper_id_': testpaper[0],
                'user_id': testpaper[1]
            }
            paper.append(data)
        papers['paper'] = paper
    except Exception as e:
        print(e)
        return bad_response('正在维护')
    
    return jsonify(papers)

@token_auth.verify_token
@wqb.route('/correctPaper/<int:student_id>/<int:exam_id>', methods=['GET'])#考官批改试卷
@permission_require_teacher
def correctPaper(student_id,exam_id):
    try:
        paper = testpaperUtil.teacherGetPaperUtil(exam_id,student_id)
    except Exception as e:
        print(e)
        return bad_response('正在维护')

    return jsonify(paper)




@token_auth.verify_token
@wqb.route('/correctPaper/<int:student_id>/<int:exam_id>', methods=['POST'])#考官批改试卷上传
@permission_require_teacher
def commitCorrectPaper(student_id,exam_id):
    data = request.get_json()
    message={}
    if 'questions' not in data or not data.get('questions', None):
        message['questions'] = 'Please provide questions'
    
    questions = data['questions']
    for question in questions:
        if 'question_id' not in question or not question.get('question_id', None):
            message['question_id'] = 'Please provide questions_id'

        # if 'question_score' not in question or not question.get('question_score', None):
        if 'question_score' not in question:
            message['question_score'] = 'Please provide question_score'

        question_id = question['question_id']
        type  = db.session.query(Question.type).filter(Question.id == question_id).first()
        # print(type[0].name)
        # print(QuestionType.shortAnswer.name)
        if type[0].name != QuestionType.shortAnswer.name:
            message["question_type"] = 'Question can not  correct'

        user_exam = db.session.query(UserExam).filter(UserExam.user_id == student_id)\
            .filter(UserExam.testpaper_id == exam_id).filter(UserExam.question_id == question_id).first()
        if user_exam is None:
            message['user_exam'] = 'No exam question'

        if message:
            return bad_response(message)
        
        try:
            score = question['question_score']
            question_score = db.session.query(Question.point).filter(Question.id == question_id).first()
            if score >= (0.8*question_score[0]):
                user_exam.correct = True
            else:
                user_exam.correct = False
            
            user_exam.score = question['question_score']
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return bad_response('正在维护')

    return 'Correct testpaper success'


    
    
@token_auth.verify_token
@wqb.route('/myExamDetil/<int:exam_id>', methods=['GET'])#学生试卷细节
@permission_require_student
def myExamDetil(exam_id):
    try:
        paper = testpaperUtil.teacherGetPaperUtil(exam_id,g.user_id)
    except Exception as e:
        return bad_response('正在维护')

    return jsonify(paper)




@token_auth.verify_token
@wqb.route('/myExams', methods=['GET'])#学生试卷
@permission_require_student
def myExams():
    papers={}
    paper=[]
    try:
        # a=1/0
        testpapers = db.session.query(Testpaper.id,Testpaper.name,Testpaper.passline,Testpaper.duration).all()
        print(testpapers)
        for testpaper in testpapers:
            # print(testpaper[0])
            user_exam = db.session.query(UserExam).filter(UserExam.user_id == g.user_id)\
                .filter(UserExam.testpaper_id == testpaper[0]).first()
            print(user_exam)
            if user_exam:
                continue

            questions = db.session.query(TestpaperQuestion.question_id)\
                .filter(TestpaperQuestion.testpaper_id==testpaper[0]).all()
            qs=[]#试卷题集合
            for question in questions:
                qs.append(question[0])
            exam_score = get_exam_total(qs)
            data = {
                'testpaper_id':testpaper[0],
                'testpaper_name':testpaper[1],
                'testpaper_score':exam_score,
                'testpaper_passline':testpaper[2],
                'testpaper_duration':testpaper[3],
            }
            paper.append(data)

    except Exception as e:
        return bad_response('正在维护')

    if paper == []:
        return 'No testpaper you should take',208
    
    papers['testpaper'] = paper

    return jsonify(papers)












    



    