import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("Advanced Systems Stock Manager")

part = st.text_input("Part Number")

manufacturer = st.text_input("Manufacturer")

quantity = st.number_input("Quantity", min_value=0)

condition = st.selectbox(
    "Condition",
    ["New","Refurbished","Used"]
)

availability = st.selectbox(
    "Availability",
    ["In Stock","RFQ"]
)

price = st.number_input("Price",0)

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

    st.success("Product Added")