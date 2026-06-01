import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LeanCan", page_icon="🥫", layout="wide")

st.title("🥫 LeanCan Scheduler")

# Configuración de Supabase
SUPABASE_URL = "https://nubxhtlertuwmevxzuyd.supabase.co/rest/v1"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51YnhodGxlcnR1d21ldnh6dXlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAzMTI4ODYsImV4cCI6MjA5NTg4ODg4Nn0.sxXfypXZHyqFnXL1xeXdvXw925C6v-dg9Kg--7KNLWs"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def supabase_get(table):
    """Función para obtener datos de Supabase"""
    response = requests.get(f"{SUPABASE_URL}/{table}", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener {table}: {response.status_code}")
        return []

def supabase_post(table, data):
    """Función para insertar datos en Supabase"""
    response = requests.post(f"{SUPABASE_URL}/{table}", headers=HEADERS, json=data)
    return response

def supabase_delete(table, id_field, id_value):
    """Función para eliminar datos de Supabase"""
    response = requests.delete(f"{SUPABASE_URL}/{table}?{id_field}=eq.{id_value}", headers=HEADERS)
    return response

# Menú principal
menu = st.sidebar.radio(
    "📋 MENÚ PRINCIPAL",
    ["🏭 Líneas de Fabricación", "⚙️ Máquinas", "👥 Clientes", "📦 Referencias", "📝 Pedidos"]
)

# ============================================
# 1. LÍNEAS DE FABRICACIÓN
# ============================================
if menu == "🏭 Líneas de Fabricación":
    st.header("🏭 Líneas de Fabricación")
    
    maquinas = supabase_get("maquinas")
    
    if maquinas:
        for row in maquinas:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.subheader(f"**{row.get('nombre', 'Sin nombre')}**")
                st.caption(f"Formato: {row.get('formato', 'N/A')}")
            with col2:
                st.metric("⚡ Velocidad", f"{row.get('velocidad', 0)} latas/min")
                st.caption(f"Capacidad diaria: {row.get('capacidad', 0):,} latas")
            with col3:
                st.metric("📊 Carga", "0%")
            st.markdown("---")
    else:
        st.warning("No hay máquinas registradas")

# ============================================
# 2. MÁQUINAS (CRUD)
# ============================================
elif menu == "⚙️ Máquinas":
    st.header("⚙️ Gestión de Máquinas")
    
    tab1, tab2 = st.tabs(["📋 Listado", "➕ Añadir"])
    
    with tab1:
        maquinas = supabase_get("maquinas")
        if maquinas:
            for row in maquinas:
                with st.expander(f"🖥️ {row.get('nombre', 'Sin nombre')}"):
                    col1, col2, col3, col4 = st.columns([2,2,2,1])
                    col1.metric("Velocidad", f"{row.get('velocidad', 0)} latas/min")
                    col2.metric("Capacidad", f"{row.get('capacidad', 0):,} latas/día")
                    col3.metric("Formato", row.get('formato', 'N/A'))
                    if col4.button("🗑️", key=f"del_maq_{row.get('id')}"):
                        supabase_delete("maquinas", "id", row.get('id'))
                        st.rerun()
        else:
            st.info("No hay máquinas")
    
    with tab2:
        with st.form("form_maquina"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre")
                velocidad = st.number_input("Velocidad (latas/min)", min_value=1, value=100)
            with col2:
                formato = st.text_input("Formato")
                capacidad = st.number_input("Capacidad diaria", min_value=1, value=30000)
            if st.form_submit_button("Guardar"):
                supabase_post("maquinas", {
                    "nombre": nombre,
                    "velocidad": velocidad,
                    "capacidad": capacidad,
                    "formato": formato
                })
                st.rerun()

# ============================================
# 3. CLIENTES (CRUD)
# ============================================
elif menu == "👥 Clientes":
    st.header("👥 Gestión de Clientes")
    
    tab1, tab2 = st.tabs(["📋 Listado", "➕ Añadir"])
    
    with tab1:
        clientes = supabase_get("clientes")
        if clientes:
            for row in clientes:
                with st.expander(f"🏢 {row.get('nombre', 'Sin nombre')}"):
                    col1, col2, col3 = st.columns([2,2,1])
                    col1.metric("Prioridad", f"{row.get('prioridad', 5)}/10")
                    col2.metric("Penalización", f"{row.get('penalizacion', 0)} €/día")
                    if col3.button("🗑️", key=f"del_cli_{row.get('id')}"):
                        supabase_delete("clientes", "id", row.get('id'))
                        st.rerun()
        else:
            st.info("No hay clientes")
    
    with tab2:
        with st.form("form_cliente"):
            nombre = st.text_input("Nombre")
            col1, col2 = st.columns(2)
            with col1:
                prioridad = st.slider("Prioridad (1-10)", 1, 10, 5)
            with col2:
                penalizacion = st.number_input("Penalización (€/día)", min_value=0, value=0)
            if st.form_submit_button("Guardar"):
                supabase_post("clientes", {
                    "nombre": nombre,
                    "prioridad": prioridad,
                    "penalizacion": penalizacion
                })
                st.rerun()

# ============================================
# 4. REFERENCIAS (PRODUCTOS)
# ============================================
elif menu == "📦 Referencias":
    st.header("📦 Gestión de Referencias")
    
    tab1, tab2 = st.tabs(["📋 Listado", "➕ Añadir"])
    
    with tab1:
        productos = supabase_get("productos")
        if productos:
            for row in productos:
                with st.expander(f"📦 {row.get('sku', 'Sin SKU')} - {row.get('nombre', 'Sin nombre')}"):
                    col1, col2, col3, col4 = st.columns([1,1,1,1])
                    col1.metric("SKU", row.get('sku', 'N/A'))
                    col2.metric("Formato", row.get('formato', 'N/A'))
                    col3.metric("Familia", row.get('familia', '-'))
                    if col4.button("🗑️", key=f"del_prod_{row.get('sku')}"):
                        supabase_delete("productos", "sku", row.get('sku'))
                        st.rerun()
        else:
            st.info("No hay productos")
    
    with tab2:
        with st.form("form_producto"):
            col1, col2 = st.columns(2)
            with col1:
                sku = st.text_input("SKU")
                nombre = st.text_input("Nombre")
            with col2:
                formato = st.selectbox("Formato", ["RR-120", "RR-90", "RO-85", "RT"])
                familia = st.text_input("Familia")
            if st.form_submit_button("Guardar"):
                supabase_post("productos", {
                    "sku": sku,
                    "nombre": nombre,
                    "formato": formato,
                    "familia": familia
                })
                st.rerun()

# ============================================
# 5. PEDIDOS
# ============================================
elif menu == "📝 Pedidos":
    st.header("📝 Gestión de Pedidos")
    
    clientes = supabase_get("clientes")
    productos = supabase_get("productos")
    
    if not clientes or not productos:
        st.warning("Primero crea clientes y productos")
    else:
        tab1, tab2 = st.tabs(["📋 Listado", "➕ Nuevo Pedido"])
        
        with tab1:
            pedidos = supabase_get("pedidos")
            if pedidos:
                # Crear diccionario de clientes por ID
                clientes_dict = {c.get('id'): c.get('nombre') for c in clientes}
                
                for row in pedidos:
                    cliente_nombre = clientes_dict.get(row.get('cliente_id'), "Desconocido")
                    with st.expander(f"📄 Pedido {row.get('numero', 'Sin número')} - {cliente_nombre}"):
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Fecha entrega", row.get('fecha_entrega', 'N/A'))
                        col2.metric("Cantidad", f"{row.get('cantidad', 0):,} latas")
                        col3.metric("Producto", row.get('producto_sku', 'N/A'))
                        col4.metric("RT", "✅" if row.get('lleva_rt') else "❌")
                        if st.button("🗑️", key=f"del_ped_{row.get('id')}"):
                            supabase_delete("pedidos", "id", row.get('id'))
                            st.rerun()
            else:
                st.info("No hay pedidos")
        
        with tab2:
            with st.form("form_pedido"):
                col1, col2 = st.columns(2)
                with col1:
                    numero = st.text_input("Número de pedido")
                    cliente_opciones = {c.get('nombre'): c.get('id') for c in clientes}
                    cliente_nombre = st.selectbox("Cliente", list(cliente_opciones.keys()))
                with col2:
                    fecha_entrega = st.date_input("Fecha entrega", datetime.now())
                    producto_opciones = {p.get('sku'): p.get('nombre') for p in productos}
                    producto_sku = st.selectbox("Producto", list(producto_opciones.keys()))
                    cantidad = st.number_input("Cantidad (latas)", min_value=1, value=10000)
                    lleva_rt = st.checkbox("Lleva RT")
                
                if st.form_submit_button("Guardar"):
                    supabase_post("pedidos", {
                        "numero": numero,
                        "cliente_id": cliente_opciones[cliente_nombre],
                        "fecha_entrega": str(fecha_entrega),
                        "cantidad": cantidad,
                        "producto_sku": producto_sku,
                        "lleva_rt": 1 if lleva_rt else 0
                    })
                    st.rerun()
