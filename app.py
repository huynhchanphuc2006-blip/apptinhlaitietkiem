import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(
    page_title="Tính Lãi Đơn & Lãi Kép",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Lãi Đơn & Lãi Kép")
st.write("Nhập các thông số đầu vào bên dưới để tính toán và so sánh số tiền nhận được.")

st.divider()

# Khu vực nhập dữ liệu
col1, col2 = st.columns(2)

with col1:
    c = st.number_input(
        "Số tiền gốc ban đầu (đồng)",
        min_value=0,
        value=100_000_000,
        step=1_000_000,
        format="%d"
    )
    n = st.number_input(
        "Số kỳ hạn (n)",
        min_value=1,
        value=3,
        step=1
    )

with col2:
    # Nhập lãi suất theo % cho trực quan với người dùng, sau đó chia 100
    rate_percent = st.number_input(
        "Lãi suất mỗi kỳ (%)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f"
    )
    i = rate_percent / 100

st.divider()

# Tính toán theo công thức gốc
An = c * (1 + i * n)
Bn = c * ((1 + i) ** n)

lai_don = An - c
lai_kep = Bn - c
chenh_lech = Bn - An

# Hiển thị kết quả nổi bật bằng Metric
st.subheader("📊 Kết quả tính toán")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(
        label="Tổng nhận theo Lãi Đơn",
        value=f"{An:,.0f} đ",
        delta=f"Tiền lãi: {lai_don:,.0f} đ"
    )

with res_col2:
    st.metric(
        label="Tổng nhận theo Lãi Kép",
        value=f"{Bn:,.0f} đ",
        delta=f"Tiền lãi: {lai_kep:,.0f} đ (Hơn lãi đơn {chenh_lech:,.0f} đ)"
    )

# Hiển thị câu thông báo tương tự code gốc
st.success(f"**Số tiền KH nhận được theo lãi đơn:** {An:,.0f} đồng")
st.info(f"**Số tiền KH nhận được theo lãi kép:** {Bn:,.0f} đồng")

# Bảng theo dõi biến động qua từng kỳ hạn
st.subheader("📈 Chi tiết tăng trưởng qua từng kỳ")
data = []
for ky in range(1, int(n) + 1):
    tien_don = c * (1 + i * ky)
    tien_kep = c * ((1 + i) ** ky)
    data.append({
        "Kỳ hạn": f"Kỳ {ky}",
        "Lãi đơn (đồng)": f"{tien_don:,.0f}",
        "Lãi kép (đồng)": f"{tien_kep:,.0f}",
        "Chênh lệch (đồng)": f"{(tien_kep - tien_don):,.0f}"
    })

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)
