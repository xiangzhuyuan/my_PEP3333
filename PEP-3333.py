from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def hello_world_test():
    return 'Hello World TEST!'

if __name__ == '__main__':
    app.run()
