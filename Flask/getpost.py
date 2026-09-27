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

if __name__ == '__main__':
    app.run(debug=True)