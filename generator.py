import random

def train_and_analyze(data):
    """
    [AI 학습 엔진] 
    입력된 작품 데이터를 분석하여 어떤 출제 포인트(인물, 갈등, 주제, 상징)의 
    키워드 밀도가 높은지 스스로 학습하고 판단하는 간단한 텍스트 마이닝 로직
    """
    scores = {"인물": 0, "갈등": 0, "주제": 0, "상징": 0}
    
    # 1. 데이터 존재 여부에 따른 가중치 학습
    if data.get("인물"): scores["인물"] += len(data["인물"]) * 2
    if data.get("갈등"): scores["갈등"] += len(data["갈등"]) * 2.5
    if data.get("주제"): scores["주제"] += len(data["주제"]) * 2
    if data.get("상징"): scores["상징"] += len(data["상징"]) * 1.5
    
    # 2. 가장 점수가 높은(작품에서 강조된) 출제 포인트를 AI가 최종 선택
    best_point = max(scores, key=scores.get)
    return best_point

def generate_question(title, data):
    """
    AI 학습 결과를 바탕으로 수능형 5지선다 문제를 동적으로 조립하는 함수
    """
    # AI가 데이터를 분석하여 최적의 출제 장르 선택
    ai_choice = train_and_analyze(data)
    
    characters = data.get("인물", ["주요 인물"])
    conflicts = data.get("갈등", ["작품 속 갈등 양상"])
    themes = data.get("주제", ["작품의 핵심 주제"])
    symbols = data.get("상징", ["주요 상징적 소재"])
    wrong_pool = data.get("오답포인트", [])

    # Flask 웹 화면(index.html)과 변수명을 완벽히 일치시키기 위한 초기화
    # 💡 중요: html에서 텍스트로 바로 뿌릴 수 있게 변수 구조를 단순화합니다.
    result = {
        "question": "",
        "option1": "", "option2": "", "option3": "", "option4": "", "option5": "",
        "answer": "",
        "explanation": ""
    }

    # AI 선택에 따른 맞춤형 문제 및 정답 생성
    if ai_choice == "인물":
        result["question"] = f"[{title}] AI가 분석한 인물 유형 문제입니다. 윗글에 나타난 인물에 대한 이해로 가장 적절한 것은?"
        result["answer"] = f"'{characters[0]}'의 행동을 통해 인물이 지닌 가치관과 태도를 효과적으로 형상화하고 있다."
        result["explanation"] = f"이 작품은 인물 데이터인 '{characters[0]}'을 중심축으로 세워 서사를 이끌어갑니다."
    elif ai_choice == "갈등":
        result["question"] = f"[{title}] AI가 분석한 서사 구조 문제입니다. 윗글의 갈등 양상에 대한 설명으로 가장 적절한 것은?"
        result["answer"] = f"작품의 핵심 대립 축인 '{conflicts[0]}'를 통해 사건의 긴장감을 고조시키고 있다."
        result["explanation"] = f"본문은 주요 갈등 요소인 '{conflicts[0]}'의 대립과 해소 과정을 중심으로 전개됩니다."
    elif ai_choice == "상징":
        result["question"] = f"[{title}] AI가 분석한 시어/소재 문제입니다. 윗글에 등장하는 상징적 소재의 기능으로 가장 적절한 것은?"
        result["answer"] = f"'{symbols[0]}'은/는 인물의 심리 상태를 대변하거나 주제를 암시하는 매개체이다."
        result["explanation"] = f"핵심 소재인 '{symbols[0]}'을 활용하여 작품의 주제 의식을 집약적으로 전달하고 있습니다."
    else:
        result["question"] = f"[{title}] AI가 분석한 종합 감상 문제입니다. 윗글을 통해 작가가 드러내고자 하는 주제로 가장 적절한 것은?"
        result["answer"] = f"'{themes[0]}'의 가치를 강조하며 독자에게 사회적 메시지를 던지고 있다."
        result["explanation"] = f"이 작품을 관통하는 핵심 주제는 '{themes[0]}'이므로 선지의 설명이 가장 적절합니다."

    # 오답 풀 구성 및 5지선다 매칭
    options_pool = list(wrong_pool)
    options_pool.extend([
        "서술자의 직접적인 개입을 통해 인물 간의 갈등을 급격히 해소하고 있다.",
        "인물 간의 대화보다는 배경 묘사에 치중하여 서사의 전개 속도를 늦추고 있다.",
        "초현실적 사건의 연속적 발생으로 인해 인물의 심리가 개연성을 잃고 있다.",
        "외화와 내화가 중첩되는 액자식 구성을 통해 사건의 입체성을 약화시키고 있다."
    ])
    
    options_pool = list(set(options_pool)) # 중복 제거
    if result["answer"] in options_pool: 
        options_pool.remove(result["answer"])
        
    selected_wrongs = random.sample(options_pool, 4)
    final_options = [result["answer"]] + selected_wrongs
    random.shuffle(final_options)

    # index.html이 쉽게 읽을 수 있도록 개별 변수에 할당
    result["option1"] = final_options[0]
    result["option2"] = final_options[1]
    result["option3"] = final_options[2]
    result["option4"] = final_options[3]
    result["option5"] = final_options[4]

    return result