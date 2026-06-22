from flask import Flask, render_template, request
import json
import os
from generator import generate_question

app = Flask(__name__)

works = {}

# os.walk를 사용하여 data 폴더 및 하위 폴더 탐색
for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # 💡 파일 이름에서 진짜 작품명 추출 (예: 노힐부득과달달박박_points.json -> 노힐부득과달달박박)
                    file_pure_name = file.split('_')[0].split('.')[0]
                    
                    # 딕셔너리 구조라면 작품 데이터를 맵핑
                    if isinstance(data, dict):
                        if file_pure_name not in works:
                            works[file_pure_name] = {}
                        # 기존 데이터에 새로운 key-value(인물, 갈등 등)들을 누적해서 병합
                        works[file_pure_name].update(data)
                        
            except Exception as e:
                print(f"{file} 읽기 실패:", e)

# 데이터 보완: 각 작품 내부의 'title' 키가 없으면 채워줌
for w_title in list(works.keys()):
    # 알맹이가 없는 껍데기 key 데이터는 삭제
    if w_title in ["인물", "갈등", "주제", "상징", "장면", "출제포인트", "오답포인트"]:
        works.pop(w_title, None)
    else:
        works[w_title]["title"] = w_title

print("정제 완료된 실제 작품 목록:", list(works.keys()))


@app.route("/")
def home():
    return render_template("index.html", works=works, selected_title=None, result=None)


@app.route("/generate", methods=["POST"])
def generate():
    title = request.form.get("title")
    if not title or title not in works:
        return render_template("index.html", works=works, selected_title=None, result=None)
        
    data = works[title]
    result = generate_question(title, data)
    
    # 💡 문제를 계속 돌릴 수 있도록 '선택했던 작품명'과 '결과'를 함께 템플릿으로 전달
    return render_template(
        "index.html",
        works=works,
        selected_title=title,
        result=result
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)