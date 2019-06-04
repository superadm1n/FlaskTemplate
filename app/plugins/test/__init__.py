from flask import Blueprint

blueprint = Blueprint(
    'test_blueprint',
    __name__,
    url_prefix='/test',
    template_folder='templates',
    static_folder='static'
)