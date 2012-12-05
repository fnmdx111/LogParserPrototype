from flask import render_template
from web import app

@app.route('/home')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


