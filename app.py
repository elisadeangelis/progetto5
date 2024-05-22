from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")
@app.route('/artisti')
def artisti():
    return render_template("artisti.html")

@app.route('/opere')
def opere():
    return render_template("opere.html")

if __name__ == '__main__':
    app.run(debug=True)

