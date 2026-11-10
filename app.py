# =================================================================
# 🍕 [Google Gemini API 연동] 나만의 AI 웹 서비스 스타터 코드
# =================================================================
import streamlit as st
from google import genai
from google.genai import types  # ⚡ 속도 최적화 설정을 위해 추가

# -----------------------------------------------------------------
# 1️⃣ [Secrets 보안] Google Gemini API 클라이언트 생성
# -----------------------------------------------------------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------------------------------------------------
# 2️⃣ [Header Zone] 메인 제목 및 설명
# -----------------------------------------------------------------
st.title("🍕[test2] 시험 기간 맞춤 큐레이터 '야식요정'")
st.caption("※ Google Gemini AI가 당신의 기분과 고민에 맞춰 딱 맞는 야식을 추천합니다.")

# -----------------------------------------------------------------
# 3️⃣ [Left Sidebar] 좌측 사이드바: 내 정보 및 기분 선택
# -----------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 내 정보 설정")
    user_name = st.text_input("사용자 별명:", placeholder="예: 김인공")
    mood = st.selectbox(
        "오늘의 기분 상태를 선택하세요:",
        ["😊 행복함", "😭 우울함", "🤯 스트레스 받음", "🥱 피곤함"]
    )

# -----------------------------------------------------------------
# 4️⃣ [Main Input Zone] 메인 화면: 고민 작성
# -----------------------------------------------------------------
st.subheader("📝 현재 고민이나 상황을 들려주세요")
user_story = st.text_area(
    "어떤 상황인가요? 자유롭게 적어주세요:",
    placeholder="예: 내일 수학 시험인데 잠 깨는 매콤한 게 당겨!"
)

# -----------------------------------------------------------------
# 5️⃣ [Action & Output Zone] Gemini API 호출 및 2단 결과 출력
# -----------------------------------------------------------------
if st.button("✨ AI 맞춤 추천받기"):
    if user_story:
        with st.spinner(f"Gemini AI가 {user_name if user_name else '사용자'}님의 고민을 분석하고 있습니다... 🤖"):
            
            prompt_content = f"""
            역할: 고등학교 2학년 학생 대상 친절한 '야식요정 AI'
            사용자 이름: {user_name if user_name else '학생'} 
            오늘의 기분: {mood}
            current_situation: {user_story}

            위 정보를 바탕으로 다음 사항을 친근한 말투로 간결하게 작성해 주세요:
            1. 맞춤 추천 야식 메뉴 1개와 그 이유
            2. 칼로리 조절 또는 건강을 위한 섭취 꿀팁 1가지
            """

            try:
                fast_config = types.GenerateContentConfig(
                    max_output_tokens=400,
                    temperature=0.7
                )

                response_stream = client.models.generate_content_stream(
                    model="gemini-1.5-flash",  # 혹은 사용하시는 gemini-3.8-flash
                    contents=prompt_content,
                    config=fast_config
                )

                col1, col2 = st.columns(2)
                
                with col1:
                    st.success("🎉 Gemini AI 추천 야식")
                    st.write_stream(chunk.text for chunk in response_stream)
                    
                with col2:
                    st.info("💡 섭취 꿀팁 & 응원 메시지")
                    st.write("👉 야식을 먹은 후 바로 눕지 말고 30분 동안 암기 과목을 복습해 보세요!")
            
            except Exception as e:
                st.error(f"❌ API 호출 중 오류가 발생했습니다: {e}")
                
    else:  # 👈 바로 이 else: 의 들여쓰기가 'if user_story:'와 수직으로 똑같이 맞아야 합니다!
        st.warning("⚠️ 고민 내용을 먼저 작성해 주세요!")
