import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="LeanCan", page_icon="🥫", layout="wide")

st.title("🥫 LeanCan Scheduler")
st.markdown("---")

# Conexión a Supabase
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Menú principal
menu = st.sidebar.radio(
    "📋 MENÚ PRINCIPAL",
    [
        "🏭 Líneas de Fabricación",
        "⚙️ Máquinas",
        "👥 Clientes",
        "📦 Referencias",
        "📝 Pedidos"
    ]
)

# ============================================
# 1. LÍNEAS DE FABRICACIÓN
# ============================================
if menu == "🏭 Líneas de Fabricación":
    st.header("🏭 Líneas de Fabricación")
    
    maquinas = supabase.table("maquinas").select("*").execute()
    
    if maquinas.data:
        for row in maquinas.data:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.subheader(f"**{row['nombre']}**")
                st.caption(f"Formato: {row['formato']}")
            with col2:
                st.metric("⚡ Velocidad", f"{row['velocidad']} latas/min")
                st.caption(f"Capacidad diaria: {row['capacidad']:,} latas")
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
        maquinas = supabase.table("maquinas").select("*").order("id").execute()
        if maquinas.data:
            for row in maquinas.data:
                with st.expander(f"🖥️ {row['nombre']}"):
                    col1, col2, col3, col4 = st.columns([2,2,2,1])
                    col1.metric("Velocidad", f"{row['velocidad']} latas/min")
                    col2.metric("Capacidad", f"{row['capacidad']:,} latas/día")
                    col3.metric("Formato", row['formato'])
                    if col4.button("🗑️", key=f"del_maq_{row['id']}"):
                        supabase.table("maquinas").delete().eq("id", row['id']).execute()
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
                supabase.table("maquinas").insert({
                    "nombre": nombre, "velocidad": velocidad,
                    "capacidad": capacidad, "formato": formato
                }).execute()
                st.rerun()

# ============================================
# 3. CLIENTES (CRUD)
# ============================================
elif menu == "👥 Clientes":
    st.header("👥 Gestión de Clientes")
    
    tab1, tab2 = st.tabs(["📋 Listado", "➕ Añadir"])
    
    with tab1:
        clientes = supabase.table("clientes").select("*").order("id").execute()
        if clientes.data:
            for row in clientes.data:
                with st.expander(f"🏢 {row['nombre']}"):
                    col1, col2, col3 = st.columns([2,2,1])
                    col1.metric("Prioridad", f"{row['prioridad']}/10")
                    col2.metric("Penalización", f"{row['penalizacion']} €/día")
                    if col3.button("🗑️", key=f"del_cli_{row['id']}"):
                        supabase.table("clientes").delete().eq("id", row['id']).execute()
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
                supabase.table("clientes").insert({
                    "nombre": nombre, "prioridad": prioridad, "penalizacion": penalizacion
                }).execute()
                st.rerun()

# ============================================
# 4. REFERENCIAS (PRODUCTOS)
# ============================================
elif menu == "📦 Referencias":
    st.header("📦 Gestión de Referencias")
    
    tab1, tab2 = st.tabs(["📋 Listado", "➕ Añadir"])
    
    with tab1:
        productos = supabase.table("productos").select("*").order("sku").execute()
        if productos.data:
            for row in productos.data:
                with st.expander(f"📦 {row['sku']} - {row['nombre']}"):
                    col1, col2, col3, col4 = st.columns([1,1,1,1])
                    col1.metric("SKU", row['sku'])
                    col2.metric("Formato", row['formato'])
                    col3.metric("Familia", row.get('familia', '-'))
                    if col4.button("🗑️", key=f"del_prod_{row['sku']}"):
                        supabase.table("productos").delete().eq("sku", row['sku']).execute()
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
                supabase.table("productos").insert({
                    "sku": sku, "nombre": nombre, "formato": formato, "familia": familia
                }).execute()
                st.rerun()

# ============================================
# 5. PEDIDOS
# ============================================
elif menu == "📝 Pedidos":
    st.header("📝 Gestión de Pedidos")
    
    clientes = supabase.table("clientes").select("*").execute()
    productos = supabase.table("productos").select("*").execute()
    
    if not clientes.data or not productos.data:
        st.warning("Primero crea clientes y productos")
    else:
        tab1, tab2 = st.tabs(["📋 Listado", "➕ Nuevo Pedido"])
        
        with tab1:
            pedidos = supabase.table("pedidos").select("*").order("id", desc=True).execute()
            if pedidos.data:
                for row in pedidos.data:
                    with st.expander(f"📄 Pedido {row['numero']}"):
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Fecha entrega", row['fecha_entrega'])
                        col2.metric("Cantidad", f"{row['cantidad']:,} latas")
                        col3.metric("Producto", row['producto_sku'])
                        col4.metric("RT", "✅" if row['lleva_rt'] else "❌")
                        if st.button("🗑️", key=f"del_ped_{row['id']}"):
                            supabase.table("pedidos").delete().eq("id", row['id']).execute()
                            st.rerun()
            else:
                st.info("No hay pedidos")
        
        with tab2:
            with st.form("form_pedido"):
                col1, col2 = st.columns(2)
                with col1:
                    numero = st.text_input("Número de pedido")
                    cliente_opciones = {c['nombre']: c['id'] for c in clientes.data}
                    cliente_nombre = st.selectbox("Cliente", list(cliente_opciones.keys()))
                with col2:
                    fecha_entrega = st.date_input("Fecha entrega", datetime.now())
                    producto_opciones = {p['sku']: p['nombre'] for p in productos.data}
                    producto_sku = st.selectbox("Producto", list(producto_opciones.keys()))
                    cantidad = st.number_input("Cantidad (latas)", min_value=1, value=10000)
                    lleva_rt = st.checkbox("Lleva RT")
                
                if st.form_submit_button("Guardar"):
                    supabase.table("pedidos").insert({
                        "numero": numero,
                        "cliente_id": cliente_opciones[cliente_nombre],
                        "fecha_entrega": str(fecha_entrega),
                        "cantidad": cantidad,
                        "producto_sku": producto_sku,
                        "lleva_rt": 1 if lleva_rt else 0
                    }).execute()
                    st.rerun()
