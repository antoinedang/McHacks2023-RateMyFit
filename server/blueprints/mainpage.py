from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
import fit_rater

import os


fit_api = Blueprint('fit_api', __name__)

class FitAPI(MethodView):

    def get(self):
        return 'Testing Get'
    
    def post(self):
        image = request.files['image']
        print(type(image))
        current_directory = os.getcwd()
        image.save(os.path.join(current_directory,current_app.config['UPLOAD_FOLDER'], image.filename))

        return "Ratting your fit"


fit_view = FitAPI.as_view('fit')
fit_api.add_url_rule('/fit', view_func=fit_view, methods=['GET','POST'])