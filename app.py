from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form["text"]

    # 여기 나중에 AI 문제 생성 코드 연결
    result = "문제 생성 결과"

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    