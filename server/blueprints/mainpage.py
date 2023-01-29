from flask import Blueprint, request, jsonify, current_app
from flask.views import MethodView
import json
import os
from cv2 import imencode
from utils import fit_rater
import base64

fit_api = Blueprint('fit_api', __name__)

class FitAPI(MethodView):

    def get(self):
        return 'Testing Get'
    
    def post(self):
        image = request.files['image']
        city = request.form['message']
        current_directory = os.getcwd()
        image.save(os.path.join(current_directory,current_app.config['UPLOAD_FOLDER'], image.filename))
        img, msg = fit_rater.rate_my_fit(os.path.join(current_directory,current_app.config['UPLOAD_FOLDER'], image.filename), city)
        print(msg)
        string = base64.b64encode(imencode('.jpg', img)[1]).decode()
        # Create the response
        response = jsonify({'image': string, 'message': msg})
        return response


fit_view = FitAPI.as_view('fit')
fit_api.add_url_rule('/fit', view_func=fit_view, methods=['GET','POST'])


#fix UI
#make string from outfit detection
#do fake detection on outfits
#host on mimi