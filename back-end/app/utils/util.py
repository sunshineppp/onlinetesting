from app.model.models import Question
from app.model.enums import QuestionLevel, QuestionType

def convertQuestion(question):
    question = dict(question._mapping)
    question['type'] = question['type'].name
    question['level'] = question['level'].name
    return question