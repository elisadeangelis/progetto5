from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")
@app.route('/music')
def music():
    return render_template("music.html")

@app.route('/book')
def book():
    return render_template("book.html")

if __name__ == '__main__':
    app.run(debug=True)

