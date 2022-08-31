import joblib
from flask import Flask, render_template, request 

app = Flask(__name__)
model = joblib.load('models/model.h5')
scaler = joblib.load('models/scaler.h5')
@app.route('/', methods=['GET'])

def index():
    return render_template('index.html')

@app.route('/predict', methods = ['GET'])
def get_predict():

    touch_screen = request.args.get("touch_screen") 
    if touch_screen == 'Yes':
        touch_screen = 1
    else :
        touch_screen = 0


    inp_data = [
        request.args.get("battery_power") ,
        request.args.get("int_memory") ,
        request.args.get("mobile_wt") ,
        request.args.get("pc") ,
        request.args.get("px_height") ,
        request.args.get("px_width") ,
        request.args.get("ram") ,
        request.args.get("sc_w") ,   
        touch_screen   
    ]

    inp_data = scaler.transform([inp_data])
    price_range = model.predict(inp_data)[0]

    if price_range == 1:
        price_range = 'Low Cost'
    elif price_range == 2:
        price_range = 'Medium Cost'
    elif price_range == 3:
        price_range = 'High Cost'
    elif price_range == 4:
        price_range = 'Very High Cost'

    print(inp_data)

    return render_template("index.html" , price_range = price_range)

if __name__ == '__main__' :
    app.run(debug = True,host="127.0.0.32")