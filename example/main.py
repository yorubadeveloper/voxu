from flask import Flask
from voxu import Voxu

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/voxu'
app.config['VOXU_LOG_TABLE'] = 'http_request_logs'
app.config['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

voxu = Voxu(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/test-page')
def logs():
    return "An error occured", 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
