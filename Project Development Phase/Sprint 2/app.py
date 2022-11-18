import numpy as np
import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
import base64
import time
import tensorflow
import os
import requests
from PIL import Image
st.set_page_config(
page_title=" DEEP WIND ",
page_icon="🚩"
)
old_models =tensorflow.keras.models.load_model('model.h5')
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
c.execute('CREATE TABLE IF NOT EXISTS comments_table(username TEXT,comments TEXT)')
def add_userdata(username,comments):
c.execute('INSERT INTO comments_table(username,comments) VALUES(?,?)',(username,comments))
conn.commit()
def login_user(username,comments):
c.execute('SELECT * FROM comments_table WHERE username =? AND comments = ?',(username,comments))
data = c.fetchall()
return data
def get_binary_file_downloader_html(bin_file):
with open(bin_file, 'rb') as f:
data = f.read()
bin_str = base64.b64encode(data).decode()
href = f'<a href="data:application/octet-stream;base64,{bin_str}"download="{os.path.basename(bin_file)}">You can download the sample dataset here 👩🏻‍💻!</a>'
return href
def select_all():
c.execute('SELECT * FROM comments_table')
data1 = c.fetchall()
return data1
def create_likestable():
c.execute('CREATE TABLE IF NOT EXISTS likes_table(counts TEXT)')
def add_likesdata(counts):
c.execute('INSERT INTO likes_table(counts) VALUES (?)',(counts))
conn.commit()
def count_likes():
c.execute('SELECT count(*) FROM likes_table')
data1 = c.fetchall()
return data1
# set background, use base64 to read local file
def get_base64_of_bin_file(bin_file):
"""
function to read png file
----------
bin_file: png -> the background image in local folder
"""
with open(bin_file, 'rb') as f:
data = f.read()
return base64.b64encode(data).decode()
def set_png_as_page_bg(png_file):
"""
function to display png as bg
----------
png_file: png -> the background image in local folder
"""
bin_str = get_base64_of_bin_file(png_file)
page_bg_img = '''
<style>
body {
background-image: url("data:image/png;base64,%s");
background-size: cover;
}
</style>
''' % bin_str
st.markdown(page_bg_img, unsafe_allow_html=True)
return
set_png_as_page_bg('gr.gif')
def home():
return "welcome"
#@app.route('/predict', methods=['POST'])
def predict(temperature,pressure,wind_speed,wind_direction,dew_point,relative_humidity):
values=np.array([[temperature,pressure,wind_speed,wind_direction,dew_point,relative_humidity]])
prediction=old_models.predict(values.reshape(-1,1,6), batch_size=1)
print(prediction)
return prediction
def weather_data(query):
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# City Name
print(query)
CITY = query
# Your API key
API_KEY = 'b272d7a039c01bd5e161926d44ecf9d8'
# updating the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY+"&units=metric"
print(URL)
res=requests.get(URL);
return res.json();
def print_weather(result,city):
print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
print(result['main']['temp'])
print("Wind speed: {} m/s".format(result['wind']['speed']))
print("Direction: {}".format(result['wind']['deg']))
print("Pressure: {}".format(result['main']['pressure']))
print("Relative Humidity: {}".format(result['main']['humidity']))
print("hi")
speed=result['wind']['speed']
deg=result['wind']['deg']
temp=result['main']['temp']
pres=result['main']['pressure']
rh=result['main']['humidity']
o=predict(temp,pres,speed,deg,0.0,rh)
col1, col2,col3,col4,col5 = st.beta_columns(5)
with col1:
original = Image.open("windspeed.png")
st.info("Wind Speed: {}".format(speed))
st.image(original, use_column_width=30)
with col2:
original = Image.open("winddirection.png")
st.info("Wind Direction: {}".format(deg))
st.image(original, use_column_width=True)
with col3:
original = Image.open("temp.jpg")
st.info("Air Temperature: {}".format(temp))
st.image(original, use_column_width=True)
with col4:
original = Image.open("pressure.jpg")
st.info("Air Pressure: {}".format(pres))
st.image(original, use_column_width=True)
with col5:
original = Image.open("humidity.png")
st.info("Relative Humidity: {}".format(rh))
st.image(original, use_column_width=True)
st.success('Predicted Power is {} kW'.format(o))
st.balloons()
def main():
st.sidebar.markdown("<h1 style='text-align: center; color: black;'>🧭Navigation Bar 🧭</h1>", unsafe_allow_html=True)
nav = st.sidebar.radio("",["Home 🏡","User defined Prediction📟","Forecasting 📊","Dashboard 📌"])
if nav == "Home 🏡":
st.markdown("<h1 style ='color:black; text_align:center;font-family:times new roman;font-size:20pt;font-weight: bold;'>DEEP WINDS ⚒️</h1>", unsafe_allow_html=True)
st.markdown("<h1 style=' color:brown; text_align:center;font-weight:bold;font-size:19pt;'>Made by Quad Techies with ❤️</h1>",unsafe_allow_html=True)
st.markdown("<h1 style ='color:green; text_align:center;font-weight:bold;font-size:18pt;'>🌎 Wind Power Prediction DL Web-App 🌎</h1>",unsafe_allow_html=True)with st.beta_expander("Write a review 📝"):
col1,col2 = st.beta_columns(2)
with col1:
username = st.text_input("Name")
with col2:
comments= st.text_input("Comments")
if st.button("Post ✔️"):
if((username=='' and comments=='') or username=='' or comments=='' ):
st.markdown("<h1 style='text-align: center;font-weight:bold;color:red;background-color:white;font-size:12pt;border-style:solid;border-color:red;border-radius:4px'>❌ Empty field ❌</h1>".format(username),unsafe_allow_html=True)
else:
create_usertable()
add_userdata(username,comments)
result = login_user(username,comments)
if result:
st.markdown("<h1 style='text-align: center; font-weight:
normal;color:DeepPink;background-color:white;font-size:12pt;border-style:
solid;border-color:Deeppink;border-radius:6px'> Thankyou for your
comment {} 🎉 - with regards Team DeepWind❤️
</h1>".format(username),unsafe_allow_html=True)
with st.beta_expander("View reviews 📝"):
result=select_all()
data=pd.DataFrame(result,columns=['UserName','Comments'])
st.table(data)
with st.beta_expander("Like this page💰🏆!!"):
if st.button("❤️"):
st.markdown("<h1 style='text-align: center; font-weight:
normal;color:DeepPink;background-color:white;font-size:12pt;border-style:
solid;border-color:Deeppink;border-radius:6px'> Thanks for your
like😀!</h1>", unsafe_allow_html=True)
create_likestable()
add_likesdata('1')
like=count_likes()
like=pd.DataFrame(like,columns=['Total Likes 🎖️ : '])
like=like.to_string(index=False)
st.markdown("<h1 style='text-align: left; color:
black;font-size:12pt'>{}</h1>".format(like), unsafe_allow_html=True)
if nav == "User defined Prediction📟":
set_png_as_page_bg('gra (1).jpg')
st.markdown("<h1 style='text-align: center; color: green;'>User Input
Parameters 💻️</h1>", unsafe_allow_html=True)
with st.beta_expander("Preferences"):
st.markdown("<h1 style='text-align: left;
font-weight:bold;color:black;background-color:white;font-size:11pt;'>
Temperature ⛅🌞🌧️ (°C) </h1>",unsafe_allow_html=True)
col1,col2 = st.beta_columns(2)
with col1:
min_temp=st.number_input('🌡️ Minimum Temperature
(°C)',min_value=-89,max_value=55,value=-15,step=1)
with col2:
max_temp=st.number_input('🌡️ Maximum Temperature
(°C)',min_value=-88,max_value=56,value=50,step=1)
st.markdown("<h1 style='text-align: left;
font-weight:bold;color:black;background-color:white;font-size:11pt;'>
Wind Speed 🌬️ (m/s) </h1>",unsafe_allow_html=True)
col1,col2 = st.beta_columns(2)
with col1:
min_speed=st.number_input('🚀 Minimum Wind Speed
(m/s)',min_value=0,max_value=99,value=1,step=1)
with col2:
max_speed=st.number_input('🚀 Maximum Wind Speed
(m/s)',min_value=2,max_value=100,value=27,step=1)
st.write("")
temperature = st.slider('Temperature ⛅🌞🌧️ [°C]', min_value=min_temp,
step=1, max_value=max_temp,value=max_temp)
pressure = st.slider('Pressure ⚡ [atm]️',min_value=800,step=1,
max_value=1050,value=1050)
wind_speed = st.slider('Wind Speed 🌬️ [m/s]', min_value=min_speed,
step=1, max_value=max_speed,value=max_speed)
wind_direction = st.slider('Wind Direction 🚩🌀 [deg]', 0, 1, 360)
dew_point = st.slider('Dew Point 💦 [deg]', float(-360), float(1), float(360))
relative_humidity = st.slider('Relative Humidity ☔ [%]', 0, 1, 100)
result = ""
profit=0
if st.button("Predict"):
result = predict(temperature,pressure,wind_speed,wind_direction,dew_point,relative_humidity)
profit=result*0.017*24*365*0.39
profit= int(74.19*profit)
st.balloons()
st.success('Predicted Power is {} kW'.format(result))
st.warning('Annual Profit is {} Rupees'.format(round(profit,2)))
if nav == "Forecasting 📊":
set_png_as_page_bg('04.gif')
st.markdown("<h1 style='text-align: center; color:black
;'>⚡FORECASTING⚡</h1>", unsafe_allow_html=True)
with st.beta_expander("📁 Sample Dataset 📁"):
st.markdown(get_binary_file_downloader_html('SampleData.csv'),
unsafe_allow_html=True)
# Setup file upload
st.markdown("<h1 style='text-align:center;
color:white;background-color:black;font-size:14pt'>📂 Upload your CSV
or Excel file. (200MB max) 📂</h1>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(label="",type=['csv', 'xlsx'])
global df
if uploaded_file is not None:
print(uploaded_file)
st.markdown("<h1 style='text-align:center;
color:black;background-color:lightgreen;font-size:14pt'>📂 File upload
successful 📂</h1>", unsafe_allow_html=True)
print("hello")
try:
df = pd.read_csv(uploaded_file)
st.write(df)
except Exception as e:
df = pd.read_excel(uploaded_file)
st.write(df)
st.markdown("<h1 style='text-align: center; color:black
;background-color:powderblue;font-size:14pt'>📈 INPUT DATA IN TERMS OF
DATE 📈</h1>", unsafe_allow_html=True)
trace = go.Scatter(
x = df['DateTime'],
y = df['Power generated by system | (kW)'],
mode = 'lines',
name = 'Data'
)
layout = go.Layout(
title = "",
xaxis = {'title' : "Date"},
yaxis = {'title' : "Power generated by system | (kW)"}
)
fig = go.Figure(data=[trace], layout=layout)
#fig.show()
st.write(fig)
df1=df.reset_index()['Power generated by system | (kW)']
import matplotlib.pyplot as plt
st.write("\n")
st.markdown("<h1 style='text-align: center; color:black
;background-color:powderblue;font-size:14pt'>📈 INPUT DATA IN TERMS OF
NO. OF HOURS 📈 </h1>", unsafe_allow_html=True)
trace = go.Scatter(
x = df1.index,
y = df['Power generated by system | (kW)'],
mode = 'lines',
name = 'Data'
)
layout = go.Layout(
title = "",
xaxis = {'title' : "No. of hours"},
yaxis = {'title' : "Power generated by system (kW)"}
)
fig = go.Figure(data=[trace], layout=layout)
#fig.show()
st.write(fig)
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
##splitting dataset into train and test split
training_size=int(len(df1)*0.65)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
import numpy
# convert an array of values into a dataset matrix
# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
dataX, dataY = [], []
for i in range(len(dataset)-time_step-1):
a = dataset[i:(i+time_step), 0] ###i=0, 0,1,2,3-----99 100
dataX.append(a)
dataY.append(dataset[i + time_step, 0])
return numpy.array(dataX), numpy.array(dataY)
# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 30
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)
# reshape input to be [samples, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)
### Create the BILSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
model = Sequential()
model.add(Bidirectional(LSTM(300, input_shape=(1, 30))))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=10,batch_size=64,verbose=1)
import tensorflow as tf
### Lets Do the prediction and check performance metrics
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)
##Transformback to original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)
### Calculate RMSE performance metrics
import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train,train_predict))
### Test Data RMSEmath.sqrt(mean_squared_error(ytest,test_predict))
### Plotting
# shift train predictions for plotting
look_back=30
trainPredictPlot = numpy.empty_like(df1)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
# shift test predictions for plotting
testPredictPlot = numpy.empty_like(df1)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :] = test_predict
# plot baseline and predictions
st.markdown("<h1 style='text-align: center; color:black
;background-color:powderblue;font-size:14pt'>📈 TRAIN AND TEST DATA 📈
</h1>", unsafe_allow_html=True)
#plt.plot(scaler.inverse_transform(df1))
plt.plot(scaler.inverse_transform(df1), color="blue", linewidth=1,
linestyle="-")
plt.xlabel('No. of hours')
# Set the y axis label of the current axis.
plt.ylabel('Power generated by system | (kW)')
plt.plot(trainPredictPlot,label='Train
Data',color="black",linewidth=2, linestyle="--")
plt.plot(testPredictPlot,label='Test Data',color="orange",linewidth=2,
linestyle="--")
plt.legend(loc="upper left")
#plt.show()
st.pyplot(plt)
x_input=test_data[len(test_data)-30:].reshape(1,-1)
temp_input=list(x_input)
temp_input=temp_input[0].tolist()
# demonstrate prediction for next 24 hours
from numpy import array
lst_output=[]
n_steps=30
i=0
while(i<24):
if(len(temp_input)>30):
#print(temp_input)
x_input=np.array(temp_input[1:])
x_input=x_input.reshape(1,-1)
x_input = x_input.reshape((1, n_steps, 1))
yhat = model.predict(x_input, verbose=0)
temp_input.extend(yhat[0].tolist())
temp_input=temp_input[1:]
lst_output.extend(yhat.tolist())
i=i+1
else:
x_input = x_input.reshape((1, n_steps,1))
yhat = model.predict(x_input, verbose=0)
print(yhat[0])
temp_input.extend(yhat[0].tolist())
print(len(temp_input))
lst_output.extend(yhat.tolist())
i=i+1
print(lst_output)
day_new=np.arange(1,31)
day_pred=np.arange(len(df1),len(df1)+24)
import matplotlib.pyplot as plt
print(len(df1))
progress=st.progress(0)
for i in range(100):
time.sleep(0.1)
progress.progress(i+1)
st.balloons()
st.markdown("<h1 style='text-align: center; color:black
;background-color:powderblue;font-size:14pt'>📈 PREDICTED RESULTS FOR
NEXT 24 HOURS 📈</h1>", unsafe_allow_html=True)
plt.plot(day_pred,scaler.inverse_transform(lst_output),color="green",linewidth=1.5,
linestyle="--",marker='*',markerfacecolor='yellow', markersize=7)
plt.legend('GTtP',loc="upper left")
plt.xlabel('No. of hours')
# Set the y axis label of the current axis.
plt.ylabel('Power generated by system | (kW)')
st.pyplot(plt)
st.markdown("<h1 style='text-align: center; color:black
;background-color:yellow;font-size:14pt'>🏷️ G-Given Data,
\n🏷️T-Train Data, \n🏷️t-Test Data, \n🏷️P-Predicted Results</h1>",
unsafe_allow_html=True)
power=pd.DataFrame(scaler.inverse_transform(lst_output),columns=['Predicted
Power(kW)'])
st.write(power)
avg_power=power.sum()
avg_power = int(avg_power/24)
profit1=avg_power*0.017*24*0.39
profit1= 74.19*profit1
st.balloons()
value=f"<h1 style='text-align: center; color:black
;background-color:powderblue;font-size:14pt'> Day Profit is
{profit1:.2f} Rupees</h1>"
st.markdown(value,unsafe_allow_html=True)
if nav == "Dashboard 📌":
set_png_as_page_bg('white.jpg')
city=st.text_input('Enter the city:')
print()
try:
query=city;
w_data=weather_data(query);
print_weather(w_data, city)
except:
pass
st.warning('City name not found...')
if __name__ == "__main__":
main()
