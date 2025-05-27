import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm
import numpy as np
import base64
import os

# 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()

st.title("갈톤 보드 실시간 애니메이션 🎬")

# 사용자 입력
num_balls = st.slider("공의 수", 10, 100, 30, step=10)
num_levels = st.slider("핀의 층 수", 5, 15, 7)
run = st.button("시뮬레이션 시작")

# 공 경로 생성 함수
def simulate_ball_path(levels):
    position = 0
    path = [(position, 0)]
    for level in range(1, levels + 1):
        step = np.random.choice([-0.5, 0.5])
        position += step
        path.append((position, level))
    return path

# 시뮬레이션 실행
if run:
    ball_paths = [simulate_ball_path(num_levels) for _ in range(num_balls)]
    max_width = num_levels / 2 + 1

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-max_width, max_width)
    ax.set_ylim(-1, num_levels + 1)
    ax.set_title("갈톤 보드 애니메이션", fontproperties=fontprop)
    ax.axis('off')

    # 핀 위치 그리기
    for level in range(num_levels):
        for pin in range(level + 1):
            x = pin - level / 2
            y = level + 0.5
            ax.plot(x, y, 'ko', markersize=4)

    ball = ax.plot([], [], 'ro', markersize=8)[0]
    current_path = []

    def init():
        ball.set_data([], [])
        return ball,

    def update(frame):
        if frame >= len(current_path):
            return ball,
        x, y = current_path[frame]
        ball.set_data(x, y)
        return ball,

    # 하나의 공만 애니메이션
    current_path = ball_paths[0]
    ani = animation.FuncAnimation(fig, update, frames=len(current_path), init_func=init, blit=True, interval=300)

    ani.save("galton_board.gif", writer="pillow")

    with open("galton_board.gif", "rb") as f:
        gif_bytes = f.read()
        b64 = base64.b64encode(gif_bytes).decode("utf-8")
        data_url = f"data:image/gif;base64,{b64}"
        st.markdown(f"<img src='{data_url}' alt='갈톤 보드 애니메이션'>", unsafe_allow_html=True)

    st.markdown("""
    - 핀은 고정되어 있으며, 공이 좌우로 랜덤하게 이동하며 떨어지는 모습을 시뮬레이션합니다.
    - 현재는 첫 번째 공만 애니메이션으로 표현됩니다.
    """)