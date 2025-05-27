import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.font_manager as fm

# 한글 폰트 설정 (NanumGothic.ttf는 fonts 폴더 안에 있어야 함)
font_path = "fonts/NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)

# 제목
st.title("정규분포 확률 계산기")

# 입력값 받기
mean = st.number_input("평균 (μ)", value=0.0)
std_dev = st.number_input("표준편차 (σ)", value=1.0, min_value=0.01)
a = st.number_input("구간 a", value=-1.0)
b = st.number_input("구간 b", value=1.0)

# x축 범위 및 정규분포 계산
x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 500)
y = norm.pdf(x, mean, std_dev)

# 확률 계산
p = norm.cdf(b, mean, std_dev) - norm.cdf(a, mean, std_dev)

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(x, y, label='정규분포 곡선')
ax.fill_between(x, y, where=(x >= a) & (x <= b), color='skyblue', alpha=0.5, label=f"P({a} ≤ X ≤ {b})")

# 그래프 텍스트 설정
ax.set_title("정규분포와 누적 확률 영역", fontproperties=font_prop)
ax.set_xlabel("x", fontproperties=font_prop)
ax.set_ylabel("확률 밀도", fontproperties=font_prop)
ax.legend(prop=font_prop)

# 출력
st.pyplot(fig)
st.write(f"✅ P({a} ≤ X ≤ {b}) = **{p:.4f}**")
