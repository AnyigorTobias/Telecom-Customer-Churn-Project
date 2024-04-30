from flask import Flask, render_template, request, jsonify
import prediction

app = Flask(__name__)

# Allow CORS for all origins on all routes
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Route to render the form HTML template
@app.route('/predict_form')
def predict_form():
    return render_template('form.html')

# Route to handle churn prediction
@app.route('/getPredictionOutput', methods=['GET', 'POST'])
def predict_churn():
    if request.method == 'POST':
        try:
            customer = {
                'gender': request.form["gender"],
                'seniorcitizen': request.form["seniorcitizen"],
                'partner': request.form["partner"],
                'dependents': request.form["dependents"],
                'phoneservice': request.form["phoneservice"],
                'multiplelines': request.form["multiplelines"],
                'internetservice': request.form["internetservice"],
                'onlinesecurity': request.form["onlinesecurity"],
                'onlinebackup': request.form["onlinebackup"],
                'deviceprotection': request.form["deviceprotection"],
                'techsupport': request.form["techsupport"],
                'streamingtv': request.form["streamingtv"],
                'streamingmovies': request.form["streamingmovies"],
                'contract': request.form["contract"],
                'paperlessbilling': request.form["paperlessbilling"],
                'paymentmethod': request.form["paymentmethod"],
                'tenure': request.form["tenure"],
                'monthlycharges': request.form["monthlycharges"],
                'totalcharges': request.form["totalcharges"]
            }

            predicted_churn = prediction.load_model(customer)
            return jsonify({"Predicted Churn": predicted_churn})

        except Exception as error:
            return jsonify({'error': str(error)}), 500

    # Return a message if a GET request is made to this endpoint
    return jsonify({'message': 'Use POST method to get churn prediction'}), 405

