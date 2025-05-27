import streamlit as st
import matplotlib
matplotlib.use("Agg")  # headless backend 설정
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm
import numpy as np
import base64

# 한글 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = fontprop.get_name()

st.title("갈톤 보드 실시간 애니메이션 🎬")
num_levels = st.slider("핀의 층 수", 5, 15, 7)
run = st.button("시뮬레이션 시작")

def simulate_ball_path(levels):
    position = 0
    path = [(0, 0)]
    for level in range(1, levels + 1):
        step = np.random.choice([-0.5, 0.5])
        position += step
        path.append((position, level))
    return path

if run:
    path = simulate_ball_path(num_levels)

    if len(path) < 2:
        st.error("공의 경로가 너무 짧습니다.")
    else:
        fig, ax = plt.subplots(figsize=(6, 6))
        max_x = num_levels / 2 + 1
        ax.set_xlim(-max_x, max_x)
        ax.set_ylim(-1, num_levels + 1)
        ax.set_title("갈톤 보드 애니메이션", fontproperties=fontprop)
        ax.axis("off")

        # 핀 고정
        for level in range(num_levels):
            for pin in range(level + 1):
                x = pin - level / 2
                y = level + 0.5
                ax.plot(x, y, "ko", markersize=4)

        ball, = ax.plot([], [], 'ro', markersize=10)

        def init():
            ball.set_data([], [])
            return (ball,)

        def update(frame):
            if frame < len(path):
                x, y = path[frame]
                ball.set_data(x, y)
            return (ball,)

        # ✅ 핵심: save_count 명시 + blit=False
        ani = animation.FuncAnimation(
            fig, update,
            frames=len(path),
            init_func=init,
            blit=False,
            interval=300,
            save_count=len(path)  # ← save_count 설정 중요
        )

        plt.close(fig)  # Streamlit 백엔드 충돌 방지

        # 저장
        ani.save("galton_board.gif", writer="pillow")

        # 표시
        with open("galton_board.gif", "rb") as f:
            gif_bytes = f.read()
            b64 = base64.b64encode(gif_bytes).decode("utf-8")
            data_url = f"data:image/gif;base64,{b64}"
            st.markdown(f"<img src='{data_url}' alt='갈톤 보드 애니메이션'>", unsafe_allow_html=True)
