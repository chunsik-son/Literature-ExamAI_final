from flask import Flask, render_template, request
import json
import os
from generator import generate_question

app = Flask(__name__)

works = {}

# os.walk를 사용하여 data 폴더 및 그 하위 폴더(events, points, questions 등)의 모든 json을 탐색
for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # json 구조에 따라 작품 목록(works)에 등록
                    if isinstance(data, dict) and "title" in data:
                        works[data["title"]] = data
                    elif isinstance(data, dict):
                        works.update(data)
                        
            except Exception as e:
                print(f"{file} 읽기 실패:", e)

print("불러온 작품 수:", len(works))


@app.route("/")
def home():
    return render_template(
        "index.html",
        works=works
    )


@app.route("/generate", methods=["POST"])
def generate():
    title = request.form["title"]
    data = works[title]
    
    result = generate_question(title, data)
    
    return render_template(
        "index.html",
        works=works,
        result=result
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )