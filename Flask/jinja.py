from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/index', methods=['GET', 'POST'])
def index():
    name = None
    if request.method == 'POST':
        name = request.form.get('name')
    return render_template('form.html', name=name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/success/<score>')
def success(score):
    #return 'The person has scored '+str(score)
    res=""
    if int(score)>=50:
        res="Passed"
    else:
        res="Failed"
    return render_template('result.html', result=res)
@app.route('/success_res/<int:scores>')
def success_res(scores):
    #return 'The person has scored '+str(score)
    res=""
    if int(scores)>=50:
        res="Passed"
    else:
        res="Failed"
    exp={"score":scores, "result":res}
    return render_template('result1.html', result=exp)
@app.route('/successif/<int:scores>')
def successif(scores):
    return render_template('result1.html', result=scores)
if __name__ == '__main__':
    app.run(debug=True)