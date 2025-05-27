import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

font_path = 'NanumGothic.ttf'  # 업로드한 ttf 파일 경로
fontprop = fm.FontProperties(fname=font_path)

# 사용자 입력
num_balls = st.slider("공의 수", min_value=10, max_value=1000, value=300, step=10)
num_levels = st.slider("핀의 층 수", min_value=5, max_value=20, value=10, step=1)

# 공이 지나간 경로를 저장할 리스트
final_positions = []

# 공 하나당 시뮬레이션
for _ in range(num_balls):
    position = 0
    for _ in range(num_levels):
        step = np.random.choice([0, 1])  # 0: 왼쪽, 1: 오른쪽
        position += step
    final_positions.append(position)

# 히스토그램 그리기
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(final_positions, bins=range(num_levels+2), edgecolor='black', align='left')
plt.title("갈톤 보드 시뮬레이터", fontproperties=fontprop)
plt.xlabel("도착 위치", fontproperties=fontprop)
plt.ylabel("공의 수", fontproperties=fontprop)

st.pyplot(fig)

st.markdown("""
**설명**:
- 갈톤 보드는 확률과 통계에서 정규분포가 자연스럽게 나타나는 원리를 보여주는 장치입니다.
- 공은 각 핀을 만날 때마다 좌우로 이동할 확률이 같으며, 많은 공이 떨어지면 종 모양의 분포를 형성합니다.
""")
