from flask import Blueprint

question_blueprint = Blueprint('question', __name__, url_prefix='/question')
testpaper_blueprint = Blueprint('testpaper', __name__, url_prefix='/paper')

# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
from app.api import question
from app.api import testpaper