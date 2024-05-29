from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired
import os
import soundfile as sf
import librosa
import numpy as np
import pickle
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.config['SECRET_KEY'] = '23223'  # Replace with a secret key for form security

# Load the model and label encoder
model_path = r'C:\Users\AVINASH RAJ\Desktop\Project_111\model\rnn_new.h5'
model = tf.keras.models.load_model(model_path)

label_encoder_path = r'C:\Users\AVINASH RAJ\Desktop\Project_111\model\rnn_new.pkl'
with open(label_encoder_path, 'rb') as file:
    label_encoder = pickle.load(file)

# Define a form for file upload
class FileUploadForm(FlaskForm):
    audio_file = FileField('Upload MP3 File', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Define functions for processing audio
def extract_mfcc(audio_data, sample_rate):
    mfccs = np.mean(librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40).T, axis=0)
    return mfccs

def predict_language(audio_data, sample_rate):
    test_point = extract_mfcc(audio_data, sample_rate)
    test_point = np.reshape(test_point, newshape=(1, 40, 1))
    prediction = model.predict(test_point)
    predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]
    predicted_probabilities = {label: prob for label, prob in zip(label_encoder.classes_, prediction[0])}
    return predicted_label, predicted_probabilities

# Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    form = FileUploadForm()
    if form.validate_on_submit():
        audio_file = form.audio_file.data
        filename = "uploaded_audio.mp3"
        audio_file.save(filename)
        predicted_language, predicted_probabilities = process_recorded_audio(filename)
        os.remove(filename)
        if predicted_language == 0:
            lan = "Hindi"
        elif predicted_language == 1:
            lan = "Marathi"
        elif predicted_language == 2:
            lan = "English"
        return render_template('result.html', predicted_language= lan, predicted_probabilities=predicted_probabilities)
    return render_template('index.html', form=form)

def process_recorded_audio(filename):
    audio, sample_rate = librosa.load(filename, sr=None)
    predicted_language, predicted_probabilities = predict_language(audio, sample_rate)
    return predicted_language, predicted_probabilities

if __name__ == "__main__":
    app.run(debug=True)
