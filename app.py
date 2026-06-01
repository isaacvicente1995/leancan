import streamlit as st

st.set_page_config(page_title="LeanCan", page_icon="🥫", layout="wide")

st.title("LeanCan Scheduler")
st.write("Bienvenido al sistema de planificación de producción")

st.subheader("Máquinas")
st.dataframe({
    "Máquina": ["E1", "E2", "E3", "E5", "E8"],
    "Formato": ["RR-120", "RR-120/RR-90", "RR-120", "RT", "RO-85"],
    "Capacidad (latas/día)": [54000, 32400, 54000, 33750, 48600]
})

st.subheader("Próximos pasos")
st.info("Pronto: gestión de pedidos y planificación automática")
