import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import base64
from PIL import Image
import io

# 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = fontprop.get_name()

st.title("갈톤 보드 수동 애니메이션 🎬")

num_levels = st.slider("핀의 층 수", 5, 15, 7)
run = st.button("애니메이션 만들기")

def simulate_ball_path(levels):
    position = 0
    path = [(0, 0)]
    for level in range(1, levels + 1):
        step = np.random.choice([-0.5, 0.5])
        position += step
        path.append((position, level))
    return path

def draw_frame(path, current_index, num_levels):
    fig, ax = plt.subplots(figsize=(5, 5))
    max_x = num_levels / 2 + 1
    ax.set_xlim(-max_x, max_x)
    ax.set_ylim(-1, num_levels + 1)
    ax.axis('off')

    # 핀 그리기
    for level in range(num_levels):
        for pin in range(level + 1):
            x = pin - level / 2
            y = level + 0.5
            ax.plot(x, y, 'ko', markersize=4)

    # 공 위치
    x, y = path[current_index]
    ax.plot(x, y, 'ro', markersize=10)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    return Image.open(buf)

if run:
    path = simulate_ball_path(num_levels)

    frames = []
    for i in range(len(path)):
        img = draw_frame(path, i, num_levels)
        frames.append(img)

    # GIF 저장
    gif_path = "galton_board.gif"
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=300, loop=0)

    with open(gif_path, "rb") as f:
        gif_bytes = f.read()
        b64 = base64.b64encode(gif_bytes).decode("utf-8")
        data_url = f"data:image/gif;base64,{b64}"
        st.markdown(f"<img src='{data_url}' alt='갈톤 보드 애니메이션'>", unsafe_allow_html=True)
