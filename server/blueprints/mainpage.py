from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
import json
import os
from utils import fit_rater

fit_api = Blueprint('fit_api', __name__)

class FitAPI(MethodView):

    def get(self):
        return 'Testing Get'
    
    def post(self):
        image = request.files['image']
        current_directory = os.getcwd()
        image.save(os.path.join(current_directory,current_app.config['UPLOAD_FOLDER'], image.filename))
        img, msg = fit_rater.rate_my_fit(os.path.join(current_directory,current_app.config['UPLOAD_FOLDER'], image.filename))
        return json.dumps({"message" : "test script \ntest script"})


fit_view = FitAPI.as_view('fit')
fit_api.add_url_rule('/fit', view_func=fit_view, methods=['GET','POST'])