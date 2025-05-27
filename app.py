import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import time

# 한글 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)

st.title("갈톤 보드 시뮬레이터 🎯")

# 사용자 입력
num_balls = st.slider("공의 수", min_value=10, max_value=200, value=30, step=10)
num_levels = st.slider("핀의 층 수", min_value=5, max_value=15, value=7, step=1)
speed = st.slider("애니메이션 속도 (초 단위)", min_value=0.0, max_value=1.0, value=0.1, step=0.05)

# 공 낙하 함수 (한 개 공 기준)
def drop_ball(levels):
    position = 0
    path = [0]
    for _ in range(levels):
        step = np.random.choice([0, 1])
        position += step
        path.append(position)
    return path

# 애니메이션 플롯 그리기 함수
def draw_board(ball_paths, current_ball_idx=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.clear()
    ax.set_xlim(-1, num_levels + 1)
    ax.set_ylim(-1, num_levels + 1)

    # 핀 표시
    for level in range(num_levels):
        for pin in range(level + 1):
            ax.plot(pin + 0.5 * (level % 2), num_levels - level - 1, 'ko', markersize=4)

    # 공 경로 표시
    for i, path in enumerate(ball_paths):
        if current_ball_idx is not None and i > current_ball_idx:
            continue
        for l, p in enumerate(path):
            if l > 0:
                ax.plot(p - 0.5 * (num_levels - l) % 2, num_levels - l, 'bo', alpha=0.6)

    ax.set_title("공 낙하 애니메이션", fontproperties=fontprop)
    ax.axis('off')
    st.pyplot(fig)

# 공 낙하 시뮬레이션 실행
dropped_paths = []
if st.button("공 떨어뜨리기"):
    for i in range(num_balls):
        dropped_paths.append(drop_ball(num_levels))
        draw_board(dropped_paths, current_ball_idx=i)
        time.sleep(speed)

# 결과 히스토그램
if dropped_paths:
    final_positions = [path[-1] for path in dropped_paths]
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.hist(final_positions, bins=range(num_levels+2), edgecolor='black', align='left')
    ax.set_title("최종 도착 위치 분포", fontproperties=fontprop)
    ax.set_xlabel("도착 위치", fontproperties=fontprop)
    ax.set_ylabel("공의 수", fontproperties=fontprop)
    st.pyplot(fig)

st.markdown("""
**설명**:
- 갈톤 보드는 공이 여러 층의 핀을 통과하면서 좌우로 랜덤 이동하는 실험 장치입니다.
- 많은 공이 떨어지면 정규분포 모양의 결과를 보여줍니다.
""")