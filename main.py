import streamlit as st

st.title("⚙️ 순수 스트림릿 토크 계산기")

st.markdown("""
힘과 회전 반경을 여러 개 입력하여 토크를 계산하고,  
토크 값들을 표와 막대그래프로 확인할 수 있습니다.
""")

# 입력 개수 선택
num_inputs = st.number_input("토크 계산 개수", min_value=1, max_value=10, value=3)

forces = []
distances = []
for i in range(num_inputs):
    st.write(f"### 토크 #{i+1} 입력")
    f = st.number_input(f"힘 (N) #{i+1}", min_value=0.0, value=100.0, step=1.0, key=f"f{i}")
    d = st.number_input(f"회전 반경 (m) #{i+1}", min_value=0.0, value=0.5, step=0.01, key=f"d{i}")
    forces.append(f)
    distances.append(d)

# 토크 계산
torques = [f * d for f, d in zip(forces, distances)]

# 데이터 정리
data = {
    "힘 (N)": forces,
    "회전 반경 (m)": distances,
    "토크 (N·m)": torques,
}

# 결과 테이블 출력
st.subheader("계산 결과 테이블")
st.table(data)

# 토크 합계, 평균
total_torque = sum(torques)
average_torque = total_torque / len(torques) if torques else 0

st.markdown(f"**총 토크 합계:** {total_torque:.2f} N·m")
st.markdown(f"**평균 토크:** {average_torque:.2f} N·m")

# 스트림릿 기본 바 차트로 시각화
st.subheader("토크 막대 그래프")
st.bar_chart(torques)

st.markdown("""
---
### 설명
- 입력한 힘과 회전 반경으로 토크를 계산합니다.
- 여러 토크 값을 한 번에 계산할 수 있습니다.
- 기본 스트림릿 그래프로 토크 분포를 시각화했습니다.
""")

