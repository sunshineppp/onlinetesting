from app.model.models import Question, Answer
from app.model.enums import QuestionLevel, QuestionType, AnswerCorrect

def convertQuestion(question):
    question = dict(question._mapping)
    question['type'] = question['type'].name
    question['level'] = question['level'].name
    return question

def checkQuestion(request_data, check_id = False):
    try: 
        content = request_data['content']
        analysis = request_data['analysis']
        type = request_data['type']
        level = request_data['level']
        point = request_data['point']
        if check_id == True:
            question_id = request_data['id']
    except KeyError:
        raise Exception('Question not complete', 400)

    if None not in (content, analysis, type, level, point):
        pass
    else:
        raise Exception('Question not complete', 400)

    if check_id == True:
        if question_id is not None:
            pass
        else:
            raise Exception('Question not complete', 400)

    try:
        type = QuestionType[type] 
    except KeyError:
        raise Exception('Question type is wrong', 400)
    
    try: 
        level = QuestionLevel[level]
    except KeyError:
        raise Exception('Question level is wrong', 400)

    question = Question(
        content = content,
        analysis = analysis,
        type = type,
        level = level,
        point = point
    )
    if check_id == True:
        question.id = question_id

    request_answers = request_data['answers']

    if len(request_answers) == 0:
        raise Exception('answers can not be empty', 400)

    correct_values = [member.value for member in AnswerCorrect]
    for answer in request_answers:
        try:
            answer_content = answer['content'] 
            answer_correct = answer['correct']
            if check_id == True:
                answer_id = answer['id']
        except KeyError:
            raise Exception('incomplete answers', 400)
        
        if None not in (answer_content, answer_correct):
            pass
        else:
            raise Exception('incomplete answers', 400)
        
        if answer_id is not None:
            pass
        else: 
            raise Exception('incomplete answers', 400)
        
        if answer_correct in correct_values:
            pass
        else: 
            raise Exception('correct field can only be 0 or 1', 400)
    
    answers = []
    for answer in request_answers:
        if check_id == True:
            answers.append(Answer(
                content = answer['content'],
                correct = answer['correct'],
                id = answer['id']
            ))
        else:
            answers.append(Answer(
                content = answer['content'],
                correct = answer['correct']
            ))
    
    return question, answers
     