from flask import Flask, render_template, redirect, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import re
import string


# Load data
crops = pd.read_csv('Crop_recommendation.csv')

# Preprocessing functions
def convert_to_lower(text):
    return text.lower()

def remove_numbers(text):
    number_pattern = r'\d+'
    without_number = re.sub(pattern=number_pattern, repl=" ", string=text)
    return without_number

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_extra_white_spaces(text):
    single_char_pattern = r'\s+[a-zA-Z]\s+'
    without_sc = re.sub(pattern=single_char_pattern, repl=" ", string=text)
    return without_sc

# Model training
features = crops[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
target = crops['label']
knn = KNeighborsClassifier()
knn.fit(features, target)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Route for prediction
@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        crop_x = request.form['crop']
        crop_x = convert_to_lower(remove_numbers(remove_punctuation(remove_extra_white_spaces(crop_x))))
        print(crop_x)
        x_data = request.form.to_dict()
        x_data.pop('crop')
        print(x_data)
        x_values = np.array([[float(x_data[key]) for key in x_data if x_data]])
        print(x_values.shape)
        ans = knn.predict(x_values)
        return render_template('result.html', crop=ans[0])
    return render_template('prediction.html')

@app.route('/training_results.html')
def training_results():
   return render_template('training_results.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 