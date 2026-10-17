import pickle
from flask import Flask,request,render_template,jsonify 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.preprocessing import StandardScaler



application = Flask(__name__)
app=application

#import ridge regressor and standard scalar
ridge_model=pickle.load(open('model/ridge.pkl','rb'))
standard_scaler=pickle.load(open('model/scaler.pkl','rb'))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predictdata',methods=['POST','GET'])
def predict_datapoint():
    if request.method=='POST':
        Temperature=float(request.form.get('Temperature'))
        RH=float(request.form.get('RH'))
        Ws=float(request.form.get('Ws'))
        Rain=float(request.form.get('Rain'))
        FFMC=float(request.form.get('FFMC'))
        DMC=float(request.form.get('DMC'))
        ISI=float(request.form.get('ISI'))
        Classes=int(request.form.get('Classes'))
        Region=int(request.form.get('Region'))
        data_df=pd.DataFrame({
            'Temperature': [Temperature],
            'RH': [RH],
            'Ws': [Ws],
            'Rain': [Rain],
            'FFMC': [FFMC],
            'DMC': [DMC],
            'ISI': [ISI],
            'Classes': [Classes],
            'Region': [Region]
        })
        data_scaled=standard_scaler.transform(data_df)
        prediction=ridge_model.predict(data_scaled)
        return render_template('home.html',prediction_text='The predicted value is {}'.format(prediction[0]))
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
