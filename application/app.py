from flask import Flask, request, abort, redirect, render_template, send_file, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import joblib
import os
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from model.prepare_dataset import prepare_data


app = Flask(__name__, static_folder='static')

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app.config.update({'SECRET_KEY': WTF_CSRF_SECRET_KEY,
                   'WTF_CSRF_SECRET_KEY': SECRET_KEY})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = joblib.load('./model/model.pkl')


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route('/submit/<params>')
def submit_manually(params):
    cols = ['ID', 'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5',
            'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1',
            'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
    try:
        params = [float(p) for p in params.split(',')]
        df = pd.DataFrame(dict(zip(cols, params)), index=[0])
        y_pred = model.predict(prepare_data(df))
    except ValueError:
        return bad_request()
    return render_template('prediction.html', prediction_result=f'Default next month: {bool(y_pred[0])}')


@app.route('/badrequest400')
def bad_request():
    return abort(400)


class SubmissionForm(FlaskForm):
    file = FileField()


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SubmissionForm()
    dt = datetime.today().strftime('%Y_%m-%d_%H%M%S')
    if form.validate_on_submit():
        f = form.file.data
        df = pd.read_csv(f)
        df = prepare_data(df)
        result = pd.DataFrame(model.predict(df))

        filename = 'result_' + dt + '.csv'
        filepath = os.path.join('./predictions/', filename)
        result.to_csv(filepath)
        return send_file(
            filepath,
            mimetype='text/csv',
            download_name=filename,
            as_attachment=True
        )
    return render_template('submit.html', form=form)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
    return render_template('upload.html')
