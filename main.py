import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="기계 요소 응력 해석 시뮬레이터", layout="wide")
st.title("⚙️ 기계 요소 응력 해석 시뮬레이터")

# 입력 변수 사이드바
st.sidebar.header("입력 변수")

diameter = st.sidebar.number_input("축 직경 (mm)", min_value=1.0, max_value=500.0, value=50.0, step=0.1)
axial_force = st.sidebar.number_input("축력 (축 방향 힘, N)", value=1000.0, step=10.0)
bending_moment = st.sidebar.number_input("굽힘 모멘트 (N·mm)", value=5000.0, step=100.0)

materials = {
    "탄소강 (Carbon Steel)": 250,
    "알루미늄 (Aluminum)": 150,
    "스테인리스강 (Stainless Steel)": 300,
    "구리 (Copper)": 70,
}
material = st.sidebar.selectbox("재료 선택", list(materials.keys()))
allowable_stress = materials[material]

# 단면적 계산
radius = diameter / 2 / 1000  # m
area = math.pi * radius**2  # m^2

# 응력 계산
axial_stress = axial_force / (area * 1e6)  # MPa
d_m = diameter / 1000
I = math.pi * d_m**4 / 64
c = d_m / 2
bending_stress = bending_moment * c / I / 1e6  # MPa
max_stress = axial_stress + bending_stress
safety_factor = allowable_stress / max_stress if max_stress != 0 else float('inf')

# 컬러 정하기
if safety_factor > 1.5:
    color = 'green'
elif safety_factor >= 1:
    color = 'orange'
else:
    color = 'red'

# 레이아웃
col1, col2 = st.columns([2,3])

with col1:
    st.subheader("📊 응력 값")
    st.metric("축 응력 (Axial Stress, MPa)", f"{axial_stress:.2f}")
    st.metric("굽힘 응력 (Bending Stress, MPa)", f"{bending_stress:.2f}")
    st.metric("최대 응력 (Max Stress, MPa)", f"{max_stress:.2f}")
    st.metric("허용 응력 (Allowable Stress, MPa)", f"{allowable_stress}")
    st.metric("안전율 (Safety Factor)", f"{safety_factor:.2f}", delta=None)

    if safety_factor > 1.5:
        st.success("안전합니다! 😊")
    elif 1 <= safety_factor <= 1.5:
        st.warning("주의 필요: 안전율이 낮습니다.")
    else:
        st.error("위험: 안전율 미달! 설계 재검토 필요!")

with col2:
    st.subheader("🛠️ 응력 분포 시각화")

    stresses = [axial_stress, bending_stress, max_stress]
    labels = ['축 응력', '굽힘 응력', '최대 응력']
    colors = ['blue', 'orange', color]

    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(labels, stresses, color=colors)
    ax.set_ylabel('응력 (MPa)')
    ax.set_ylim(0, max(max_stress*1.2, allowable_stress*1.2))
    ax.set_title("응력 분포")

    for bar, stress in zip(bars, stresses):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height*1.02, f'{stress:.2f}', ha='center', va='bottom')

    # 허용 응력 라인 추가
    ax.axhline(y=allowable_stress, color='red', linestyle='--', label='허용 응력')
    ax.legend()

    st.pyplot(fig)

st.markdown("---")
st.subheader("재료별 허용 응력 표 (MPa)")

import pandas as pd
df_materials = pd.DataFrame(list(materials.items()), columns=["재료", "허용 응력 (MPa)"])
st.dataframe(df_materials.style.highlight_max(axis=0, color='lightgreen'))

st.markdown("### 설명")
st.write("""
- 입력한 축 직경과 힘, 모멘트를 바탕으로 응력을 계산합니다.
- 최대 응력과 선택한 재료의 허용 응력을 비교해 안전율을 구합니다.
- 안전율이 1 이상이면 기본적으로 안전하지만, 1.5 이상을 권장합니다.
- 그래프와 색상으로 한눈에 상태를 확인할 수 있습니다.
""")

