import os
from dotenv import load_dotenv
from flask import Flask, render_template
from routes.memos import memos_bp

load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY が設定されていません。.env を確認してください")
app.config["SECRET_KEY"] = SECRET_KEY
app.register_blueprint(memos_bp)

APP_NAME = os.environ.get("APP_NAME", "メモアプリ")


@app.route("/")
def index():
    return render_template("index.html", app_name=APP_NAME)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(debug=debug, port=port)
