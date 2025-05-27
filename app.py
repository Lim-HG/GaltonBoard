import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import base64
from PIL import Image
import io

# 한글 폰트 설정
font_path = "NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()

st.title("갈톤 보드 - 여러 공 애니메이션")

num_levels = st.slider("핀의 층 수", 5, 15, 7)
num_balls = st.slider("공의 수", 1, 20, 5)
run = st.button("애니메이션 만들기")


def simulate_ball_path(levels):
    position = 0
    path = [(0, levels)]
    for level in range(1, levels + 1):
        step = np.random.choice([-0.5, 0.5])
        position += step
        path.append((position, levels - level))
    return path


def draw_frame(all_paths, current_ball, current_step, box_counts, num_levels):
    fig, ax = plt.subplots(figsize=(6, 6))
    max_x = num_levels / 2 + 1
    ax.set_xlim(-max_x - 0.5, max_x + 0.5)
    ax.set_ylim(-1, num_levels + 2)
    ax.axis('off')

    # 핀 고정
    for level in range(num_levels):
        for pin in range(level + 1):
            x = pin - level / 2
            y = num_levels - level - 0.5
            ax.plot(x, y, 'ko', markersize=4)

    # 바닥 상자
    unique_bins = sorted(set(np.round(np.linspace(-num_levels/2, num_levels/2, num_levels+1), 1).tolist() + [num_levels/2]))

    for pos in unique_bins:
        ax.add_patch(plt.Rectangle((pos - 0.25, -1), 0.5, 0.8, edgecolor='black', facecolor='lightgray'))
        count = box_counts.get(pos, 0)
        ax.text(pos, -0.6, str(count), fontsize=12, ha='center')

    # 공 표시
    for b in range(current_ball + 1):
        path = all_paths[b]
        if b < current_ball:
            x, y = path[-1]
        else:
            x, y = path[current_step] if current_step < len(path) else path[-1]
        ax.plot(x, y, 'ro', markersize=8)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    return Image.open(buf)


if run:
    all_paths = [simulate_ball_path(num_levels) for _ in range(num_balls)]
    frames = []

    # box_counts 초기화: 가능한 위치 모두 0으로 설정
    box_counts = {round(pos, 1): 0 for pos in np.round(np.linspace(-num_levels/2, num_levels/2, num_levels+1), 1)}

    for i in range(num_balls):
        path = all_paths[i]
        for step in range(len(path)):
            frames.append(draw_frame(all_paths, i, step, box_counts, num_levels))
        final_x = round(path[-1][0], 1)
        box_counts[final_x] = box_counts.get(final_x, 0) + 1
        frames.append(draw_frame(all_paths, i, len(path), box_counts, num_levels))

    # GIF 저장 (한 번만 보이도록)
    gif_path = "galton_board.gif"
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=300, loop=0)

    with open(gif_path, "rb") as f:
        gif_bytes = f.read()
        b64 = base64.b64encode(gif_bytes).decode("utf-8")
        data_url = f"data:image/gif;base64,{b64}"
        st.markdown(f"<img src='{data_url}' alt='갈톤 보드 애니메이션'>", unsafe_allow_html=True)

    # 결과 막대 그래프 출력
    st.subheader("공 도착 위치 분포")
    fig, ax = plt.subplots()
    sorted_keys = sorted(box_counts.keys())
    # counts = [box_counts[k] for k in sorted_keys]
    counts = box_counts
    labels = range(1, num_levels+1)
    ax.bar(labels, counts, color='skyblue', edgecolor='black')
    ax.set_xlabel("도착 위치", fontproperties=fontprop)
    ax.set_ylabel("공의 수", fontproperties=fontprop)
    ax.set_title("갈톤 보드 결과 분포", fontproperties=fontprop)
    st.pyplot(fig)
