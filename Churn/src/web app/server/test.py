from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import prediction

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)


class Test(Resource):
    def get(self):
        return 'Your First API'

    def post(self):
        try:
            value = request.get_json()
            if value:
                return {'Post Values': value}, 201
            return {"error": "Invalid format."}, 400
        except Exception as error:
            return {'error': str(error)}, 500


class GetPredictionOutput(Resource):
    def post(self):
        try:
            data = request.form
            if not data:
                return {"error": "No form data provided."}, 400

            customer = {
                'gender': data.get("gender"),
                'seniorcitizen': data.get("seniorcitizen"),
                'partner': data.get("partner"),
                'dependents': data.get("dependents"),
                'phoneservice': data.get("phoneservice"),
                'multiplelines': data.get("multiplelines"),
                'internetservice': data.get("internetservice"),
                'onlinesecurity': data.get("onlinesecurity"),
                'onlinebackup': data.get("onlinebackup"),
                'deviceprotection': data.get("deviceprotection"),
                'techsupport': data.get("techsupport"),
                'streamingtv': data.get("streamingtv"),
                'streamingmovies': data.get("streamingmovies"),
                'contract': data.get("contract"),
                'paperlessbilling': data.get("paperlessbilling"),
                'paymentmethod': data.get("paymentmethod"),
                'tenure': data.get("tenure"),
                'monthlycharges': data.get("monthlycharge"),
                'totalcharges': data.get("totalcharges")
            }

            prediction_result = prediction.load_model(customer)
            return {'Model Report': prediction_result}, 200
        except Exception as error:
            return {'error': str(error)}, 500


api.add_resource(Test, '/')
api.add_resource(GetPredictionOutput, '/getPredictionOutput')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
