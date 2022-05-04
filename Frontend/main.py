from flask import Flask, render_template


# https://2hjlk03e01.execute-api.us-east-1.amazonaws.com/v1/get_stream?q=movie
# https://2hjlk03e01.execute-api.us-east-1.amazonaws.com/v1/get_stream?q=spoiler

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/movie')
def movie():
    return render_template('movie.html')

@app.route('/spoiler')
def spoiler():
    return render_template('spoiler.html')


if __name__ == '__main__':
    app.run(debug=False,port=5000,host='0.0.0.0')
