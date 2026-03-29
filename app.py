from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData,PredictPipeline


application = Flask(__name__)

app = application

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return render_template('page.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        return render_template('page.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=request.form.get('reading_score'),
            writing_score=request.form.get('writing_score')
        )

        pred_data = data.get_data_as_dataframe()
        predict_pipline = PredictPipeline()

        result = predict_pipline.predict(pred_data)

        return render_template('result.html', result=result[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)