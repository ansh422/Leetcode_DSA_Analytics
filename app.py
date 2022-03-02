from flask import Flask, render_template,request
from leetcode import main_func
app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        user = request.form['uname']
        #result = main_func(user)
        return render_template('home.html', result=main_func(user))
    else:   
        return render_template('home.html')

if __name__ == "__main__":
    app.run()