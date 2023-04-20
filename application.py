from flask import Flask, render_template, request

app = Flask(__name__)

 
airline_names = ['Air India','Air Asia', 'Spice Jet','Indigo']
sources = ['Banglore','Kolkata','Delhi','Chennai','Mumbai']
destination = ['New Delhi','Banglore','Cochin','Kolkata','Delhi','Hyerbad']
stops = ['non-stop','1 stop','2 stops','3 stops','4 stops']
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html',airways=airline_names,source = sources,destination=destination,stops=stops)

@app.route('/predict',methods=['GET','POST'])
def predict():
    print('predicting...')
    print(request.method)
    if request.method == 'POST':
        a = request.form.get('Airline')
        print(a)
        return render_template('predict.html',h1=a)
    else:
        return render_template('predict.html',h1='error')


if __name__ == '__main__':
    app.run(debug=True)