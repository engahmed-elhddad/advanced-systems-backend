import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.title("Advanced Systems Stock Manager")

tab1, tab2 = st.tabs(["Add Product", "Bulk Import Excel"])


# =========================
# Add Product
# =========================
with tab1:

    st.subheader("Add Single Product")

    part = st.text_input("Part Number")

    manufacturer = st.text_input("Manufacturer")

    quantity = st.number_input("Quantity", min_value=0)

    condition = st.selectbox(
        "Condition",
        ["New", "Refurbished", "Used"]
    )

    availability = st.selectbox(
        "Availability",
        ["In Stock", "RFQ"]
    )

    price = st.number_input("Price", min_value=0)

    # 🔥 Image Upload
    images = st.file_uploader(
        "Upload Product Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if st.button("Save Product"):

        data = {
            "part_number": part,
            "manufacturer": manufacturer,
            "condition": condition,
            "availability": availability,
            "price": price,
            "quantity": quantity
        }

        res = requests.post(f"{API}/add-product", json=data)

        if res.status_code == 200:

            # Upload images
            if images:

                for img in images:

                    files = {"file": img}

                    requests.post(
                        f"{API}/upload-product-image/{part}",
                        files=files
                    )

            st.success("Product Added Successfully")

        else:

            st.error("Error Adding Product")


# =========================
# Bulk Import
# =========================
with tab2:

    st.subheader("Bulk Import from Excel")

    uploaded_file = st.file_uploader("Upload Excel File")

    if uploaded_file:

        df = pd.read_excel(uploaded_file)

        st.write("Preview:")
        st.dataframe(df)

        if st.button("Import All Products"):

            count = 0

            for _, row in df.iterrows():

                data = {
                    "part_number": row["part_number"],
                    "manufacturer": row.get("manufacturer", ""),
                    "condition": row.get("condition", "Used"),
                    "availability": row.get("availability", "In Stock"),
                    "price": row.get("price", 0),
                    "quantity": row.get("quantity", 0)
                }

                requests.post(f"{API}/add-product", json=data)

                count += 1

            st.success(f"{count} Products Imported Successfully")