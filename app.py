import streamlit as st
import pandas as pd
import math

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# ============================================================
# CSS GIAO DIỆN
# ============================================================

st.markdown("""
<style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f7fa;
        text-align: center;
        border: 1px solid #e0e0e0;
    }

    .result-label {
        font-size: 15px;
        color: #666;
        margin-bottom: 8px;
    }

    .result-value {
        font-size: 24px;
        font-weight: 700;
    }

    .formula-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="main-title">💰 MÁY TÍNH LÃI SUẤT TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Tính toán tiền lãi theo lãi đơn hoặc lãi kép</div>',
    unsafe_allow_html=True
)

# ============================================================
# NHẬP THÔNG TIN
# ============================================================

st.header("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=1000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    term_months = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    interest_rate = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.01,
        format="%.2f"
    )

with col2:
    interest_method = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    calculation_type = st.radio(
        "🧮 Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        horizontal=True
    )

# ============================================================
# THÔNG TIN NHẬP
# ============================================================

st.divider()

st.subheader("📌 Thông tin đã chọn")

info1, info2, info3, info4 = st.columns(4)

with info1:
    st.metric("Số tiền gửi", format_money(principal))

with info2:
    st.metric("Kỳ hạn", f"{term_months} tháng")

with info3:
    st.metric("Lãi suất", f"{interest_rate:.2f}%/năm")

with info4:
    st.metric("Phương pháp", calculation_type)

# ============================================================
# TÍNH TOÁN
# ============================================================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    # Lãi suất năm -> lãi suất tháng
    monthly_rate = interest_rate / 100 / 12

    # Số tháng
    n_months = int(term_months)

    # --------------------------------------------------------
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # --------------------------------------------------------

    if interest_method == "Cuối kỳ":
        periods = [n_months]
        period_months = n_months

    elif interest_method == "Hàng tháng":
        periods = list(range(1, n_months + 1))
        period_months = 1

    else:  # Hàng quý
        periods = list(range(3, n_months + 1, 3))

        # Nếu kỳ hạn không chia hết cho 3,
        # thêm kỳ cuối cùng
        if n_months % 3 != 0:
            periods.append(n_months)

        period_months = 3

    # --------------------------------------------------------
    # LÃI ĐƠN
    # --------------------------------------------------------

    if calculation_type == "Lãi đơn":

        # Công thức:
        # I = P * r * t

        total_interest = principal * (interest_rate / 100) * (n_months / 12)

        final_amount = principal + total_interest

        # Tính lãi theo từng kỳ
        schedule = []

        previous_month = 0

        for month in periods:

            current_period = month - previous_month

            interest_period = (
                principal
                * monthly_rate
                * current_period
            )

            cumulative_interest = (
                principal
                * monthly_rate
                * month
            )

            schedule.append({
                "Kỳ": f"Tháng {month}",
                "Số tiền gốc": principal,
                "Tiền lãi kỳ này": interest_period,
                "Tổng lãi lũy kế": cumulative_interest,
                "Tổng tiền": principal + cumulative_interest
            })

            previous_month = month

    # --------------------------------------------------------
    # LÃI KÉP
    # --------------------------------------------------------

    else:

        # Lãi kép:
        # A = P(1+r)^n

        final_amount = principal * (
            (1 + monthly_rate) ** n_months
        )

        total_interest = final_amount - principal

        schedule = []

        previous_month = 0

        for month in periods:

            current_amount = principal * (
                (1 + monthly_rate) ** month
            )

            previous_amount = principal * (
                (1 + monthly_rate) ** previous_month
            )

            interest_period = (
                current_amount - previous_amount
            )

            cumulative_interest = (
                current_amount - principal
            )

            schedule.append({
                "Kỳ": f"Tháng {month}",
                "Số tiền gốc": principal,
                "Tiền lãi kỳ này": interest_period,
                "Tổng lãi lũy kế": cumulative_interest,
                "Tổng tiền": current_amount
            })

            previous_month = month

    # ========================================================
    # KẾT QUẢ
    # ========================================================

    st.divider()

    st.header("📊 KẾT QUẢ TÍNH TOÁN")

    # --------------------------------------------------------
    # TÍNH LÃI ĐỊNH KỲ
    # --------------------------------------------------------

    if interest_method == "Cuối kỳ":
        periodic_interest = total_interest
        periodic_text = "Tiền lãi cuối kỳ"

    elif interest_method == "Hàng tháng":
        periodic_interest = schedule[0]["Tiền lãi kỳ này"]
        periodic_text = "Tiền lãi mỗi tháng"

    else:
        # Nếu có kỳ cuối không đủ 3 tháng thì lấy kỳ đầu tiên
        periodic_interest = schedule[0]["Tiền lãi kỳ này"]
        periodic_text = "Tiền lãi mỗi quý"

    # --------------------------------------------------------
    # HIỂN THỊ 3 KẾT QUẢ CHÍNH
    # --------------------------------------------------------

    result1, result2, result3 = st.columns(3)

    with result1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">{periodic_text}</div>
                <div class="result-value">
                    {format_money(periodic_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Tổng tiền lãi</div>
                <div class="result-value">
                    {format_money(total_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with result3:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Tổng gốc + lãi</div>
                <div class="result-value">
                    {format_money(final_amount)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # CÔNG THỨC
    # ========================================================

    st.divider()

    st.subheader("📐 Công thức áp dụng")

    if calculation_type == "Lãi đơn":

        st.markdown(
            """
            <div class="formula-box">

            <b>Lãi đơn:</b>

            <br><br>

            Tiền lãi = Tiền gốc × Lãi suất năm × Thời gian

            <br><br>

            Tổng tiền = Tiền gốc + Tiền lãi

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="formula-box">

            <b>Lãi kép:</b>

            <br><br>

            Tổng tiền = P × (1 + r)<sup>n</sup>

            <br><br>

            Trong đó:
            <br>
            • P = Tiền gốc
            <br>
            • r = Lãi suất mỗi kỳ
            <br>
            • n = Số kỳ nhập lãi

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # BẢNG CHI TIẾT
    # ========================================================

    st.divider()

    st.subheader("📅 Chi tiết tiền lãi theo từng kỳ")

    df = pd.DataFrame(schedule)

    # Định dạng tiền
    money_columns = [
        "Số tiền gốc",
        "Tiền lãi kỳ này",
        "Tổng lãi lũy kế",
        "Tổng tiền"
    ]

    for column in money_columns:
        df[column] = df[column].apply(format_money)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # TÓM TẮT
    # ========================================================

    st.divider()

    st.subheader("📝 Tóm tắt")

    st.success(
        f"""
        Với số tiền gửi **{format_money(principal)}**, kỳ hạn **{n_months} tháng**,
        lãi suất **{interest_rate:.2f}%/năm**, áp dụng **{calculation_type.lower()}**
        và nhận lãi **{interest_method.lower()}**:

        **Tổng tiền lãi: {format_money(total_interest)}**

        **Tổng số tiền nhận được: {format_money(final_amount)}**
        """
    )

# ============================================================
# CHÂN TRANG
# ============================================================

st.divider()

st.caption(
    "💡 Lưu ý: Đây là công cụ tính toán tham khảo. "
    "Lãi suất thực tế của ngân hàng có thể áp dụng quy định và cách tính khác."
)
