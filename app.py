# app.py

import streamlit as st

import pandas as pd

from datetime import datetime

from io import BytesIO

# =========================

# CẤU HÌNH TRANG

# =========================

st.set_page_config(

    page_title="Quản lý hóa đơn trà sữa",

    page_icon="🧋",

    layout="wide"

)

st.title("🧋 Ứng dụng tính tiền quán trà sữa")

st.markdown("---")

# =========================

# DỮ LIỆU MENU

# =========================

MENU = {

    "Trà sữa truyền thống": 30000,

    "Trà sữa matcha": 35000,

    "Trà sữa socola": 35000,

    "Trà sữa khoai môn": 38000,

    "Trà đào": 32000,

    "Hồng trà sữa": 34000,

    "Trà sữa ô long": 36000

}

SIZE_PRICE = {

    "M": 0,

    "L": 8000,

    "XL": 15000

}

TOPPING_PRICE = {

    "Không": 0,

    "Trân châu đen": 5000,

    "Trân châu trắng": 5000,

    "Thạch phô mai": 7000,

    "Pudding": 7000,

    "Kem cheese": 10000,

    "Nha đam": 5000

}

SUGAR_LEVEL = ["0%", "30%", "50%", "70%", "100%"]

ICE_LEVEL = ["Không đá", "Ít đá", "Bình thường"]

# =========================

# SESSION STATE

# =========================

if "cart" not in st.session_state:

    st.session_state.cart = []

# =========================

# THÔNG TIN KHÁCH HÀNG

# =========================

st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input("Tên khách hàng")

st.markdown("---")

# =========================

# CHỌN MÓN

# =========================

st.subheader("🥤 Thêm món")

col1, col2 = st.columns(2)

with col1:

    drink = st.selectbox(

        "Loại nước",

        list(MENU.keys())

    )

    size = st.selectbox(

        "Size",

        list(SIZE_PRICE.keys())

    )

    sugar = st.selectbox(

        "Mức đường",

        SUGAR_LEVEL

    )

with col2:

    topping = st.selectbox(

        "Topping",

        list(TOPPING_PRICE.keys())

    )

    ice = st.selectbox(

        "Mức đá",

        ICE_LEVEL

    )

    quantity = st.number_input(

        "Số lượng",

        min_value=1,

        value=1

    )

# =========================

# TÍNH GIÁ

# =========================

base_price = MENU[drink]

size_price = SIZE_PRICE[size]

topping_price = TOPPING_PRICE[topping]

unit_price = base_price + size_price + topping_price

total_item = unit_price * quantity

st.info(f"💰 Giá món hiện tại: {total_item:,} VNĐ")

# =========================

# THÊM GIỎ HÀNG

# =========================

if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):

    item = {

        "Tên nước": drink,

        "Size": size,

        "Topping": topping,

        "Đường": sugar,

        "Đá": ice,

        "SL": quantity,

        "Đơn giá": unit_price,

        "Thành tiền": total_item

    }

    st.session_state.cart.append(item)

    st.success("Đã thêm món!")

# =========================

# HIỂN THỊ GIỎ HÀNG

# =========================

st.markdown("---")

st.subheader("🛒 Hóa đơn tạm tính")

if len(st.session_state.cart) > 0:

    df = pd.DataFrame(st.session_state.cart)

    st.dataframe(

        df,

        use_container_width=True

    )

    grand_total = df["Thành tiền"].sum()

    st.markdown(

        f"""

        ## Tổng tiền: **{grand_total:,} VNĐ**

        """

    )

    # Xóa hóa đơn

    if st.button("🗑️ Xóa toàn bộ hóa đơn"):

        st.session_state.cart = []

        st.rerun()

else:

    st.warning("Chưa có món nào.")

# =========================

# THANH TOÁN

# =========================

st.markdown("---")

if st.button("💳 Thanh toán", use_container_width=True):

    if len(st.session_state.cart) == 0:

        st.error("Chưa có món trong hóa đơn.")

    else:

        st.subheader("🧾 HÓA ĐƠN")

        invoice_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        st.write(f"**Khách hàng:** {customer_name}")

        st.write(f"**Thời gian:** {invoice_time}")

        invoice_df = pd.DataFrame(st.session_state.cart)

        st.table(invoice_df)

        final_total = invoice_df["Thành tiền"].sum()

        st.success(f"TỔNG THANH TOÁN: {final_total:,} VNĐ")

        # =========================

        # TẠO FILE HÓA ĐƠN TXT

        # =========================

        invoice_text = ""

        invoice_text += "===== HOA DON TRA SUA =====\n"

        invoice_text += f"Khach hang: {customer_name}\n"

        invoice_text += f"Thoi gian: {invoice_time}\n"

        invoice_text += "\n"

        for i, row in invoice_df.iterrows():

            invoice_text += (

                f"{i+1}. {row['Tên nước']} | "

                f"Size {row['Size']} | "

                f"{row['Topping']} | "

                f"SL: {row['SL']} | "

                f"{row['Thành tiền']:,} VND\n"

            )

        invoice_text += "\n"

        invoice_text += f"TONG CONG: {final_total:,} VND"

        st.download_button(

            label="📥 Xuất hóa đơn TXT",

            data=invoice_text,

            file_name=f"hoadon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",

            mime="text/plain"

        )

# =========================

# FOOTER

# =========================

st.markdown("---")

st.caption("Ứng dụng quản lý hóa đơn trà sữa bằng Streamlit")
