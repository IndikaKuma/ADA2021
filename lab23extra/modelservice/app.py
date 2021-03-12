from flask import Flask, request

from diabetes_predictor import DiabetesPredictor

app = Flask(__name__)
app.config["DEBUG"] = True

model = None


@app.route('/diabetes_predictor', methods=['PUT'])
def refresh_model():
    return dp.update(request)


@app.route('/diabetes_predictor', methods=['GET'])
def predict():
    return dp.predict(request)


dp = DiabetesPredictor()
app.run(host='0.0.0.0', port=5000)
