from flask import Flask
from routes.memos import memos_bp

app = Flask(__name__)
app.register_blueprint(memos_bp)


@app.route("/")
def index():
    return {"message": "メモAPIサーバーへようこそ！"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
