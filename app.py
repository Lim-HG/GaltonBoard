import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm
import numpy as np
import os

# 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()

# 사용자 입력
st.title("갈톤 보드 실시간 애니메이션 🎬")
num_balls = st.slider("공의 수", 10, 100, 30, step=10)
num_levels = st.slider("핀의 층 수", 5, 15, 7)
run = st.button("시뮬레이션 시작")

# 공 경로 생성
def simulate_ball_path(levels):
    position = 0
    path = [position]
    for _ in range(levels):
        step = np.random.choice([0, 1])
        position += step
        path.append(position)
    return path

# 시뮬레이션 실행
if run:
    ball_paths = [simulate_ball_path(num_levels) for _ in range(num_balls)]
    max_pos = num_levels

    fig, ax = plt.subplots(figsize=(8, 5))
    scat = ax.scatter([], [], c='blue')
    ax.set_xlim(-1, max_pos + 1)
    ax.set_ylim(-1, num_levels + 1)
    ax.set_title("갈톤 보드 애니메이션", fontproperties=fontprop)
    ax.axis('off')

    frames = []

    # 각 프레임별 공 위치 누적
    positions_per_frame = [[] for _ in range(num_levels + 1)]
    for path in ball_paths:
        for level, pos in enumerate(path):
            positions_per_frame[level].append((pos, num_levels - level))

    def animate(i):
        coords = []
        for level in range(i + 1):
            coords.extend(positions_per_frame[level])
        x, y = zip(*coords) if coords else ([], [])
        scat.set_offsets(np.c_[x, y])
        return scat,

    ani = animation.FuncAnimation(fig, animate, frames=num_levels + 1, interval=500, blit=True)

    ani.save("galton_board.gif", writer='pillow')

    with open("galton_board.gif", "rb") as f:
        st.image(f.read(), format="gif")

