from flask import Blueprint, request, jsonify
from flask.views import MethodView


fit_api = Blueprint('fit_api', __name__)

class FitAPI(MethodView):

    def get(self):
        return 'Hello, World'


fit_view = FitAPI.as_view('fit')
fit_api.add_url_rule('/fit', view_func=fit_view, methods=['GET','POST'])