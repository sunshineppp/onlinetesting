import enum

class QuestionType(enum.Enum):
    singleChoice = 0
    multipleChoice = 1
    trueOrFalse = 2
    shortAnswer = 3

class QuestionLevel(enum.Enum):
    easy = 0
    medium = 1
    hard = 2
