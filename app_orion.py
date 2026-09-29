import datetime
from google.cloud import firestore
import pandas as pd
import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Lee los secretos desde la configuración de Streamlit Cloud
            secret_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(secret_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error al inicializar Firebase con los secretos: {e}")
    return firestore.client()

db = init_firebase()

# Configuración de la página
st.set_page_config(
    page_title="Club de Ciencias: Orión",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS ejecutivos y limpios
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B132B;
        color: #E0FBFC;
    }

    .main {
        background-color: #0B132B;
        padding: 1.5rem 1rem;
    }

    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 600;
        letter-spacing: -0.025em;
    }

    .product-card {
        background-color: #1C2541;
        border: 1px solid #3A506B;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }

    .stButton>button {
        background-color: #48CAE4;
        color: #0B132B;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #00B4D8;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONEXIÓN A FIREBASE FIRESTORE EN TIEMPO REAL
# ---------------------------------------------------------
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # Lee las credenciales desde los secretos seguros de Streamlit Cloud
        # O inicializa con el archivo local si estás probando en tu PC
        try:
            secret_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(secret_dict)
            firebase_admin.initialize_app(cred)
        except:
            # Fallback para pruebas locales si no hay secretos configurados aún
            pass
    return firestore.client()

db = init_firebase()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email_user = ""
    st.session_state.nombre_user = ""
    st.session_state.rol_user = ""

# ==========================================
# 1. PANTALLA DE ACCESO (LOGIN / REGISTRO)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Club de Ciencias: Orión</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8D99AE;'>Plataforma Sincronizada en Tiempo Real</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Registrarse"])
        
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            email_login = st.text_input("Correo Institucional", placeholder="tu_correo@orion.edu", key="log_email")
            pass_login = st.text_input("Contraseña", type="password", key="log_pass")
            
            if st.button("Entrar a la Plataforma", use_container_width=True):
                if email_login and pass_login:
                    # Consultar usuario en Firestore
                    user_ref = db.collection('usuarios').document(email_login).get()
                    if user_ref.exists:
                        user_data = user_ref.to_dict()
                        if user_data["password"] == pass_login:
                            st.session_state.logged_in = True
                            st.session_state.email_user = email_login
                            st.session_state.nombre_user = user_data["nombre"]
                            st.session_state.rol_user = user_data["rol"]
                            st.rerun()
                        else:
                            st.error("Contraseña incorrecta.")
                    else:
                        st.error("El correo no está registrado.")
                else:
                    st.warning("Complete todos los campos.")
        
        with tab_registro:
            st.markdown("<br>", unsafe_allow_html=True)
            nombre_reg = st.text_input("Nombre Completo", placeholder="Ej. Eneas Alvarez", key="reg_name")
            email_reg = st.text_input("Correo Institucional", placeholder="ejemplo@orion.edu", key="reg_email")
            pass_reg = st.text_input("Crear Contraseña", type="password", key="reg_pass")
            
            if st.button("Crear Cuenta", use_container_width=True):
                if nombre_reg and email_reg and pass_reg:
                    user_ref = db.collection('usuarios').document(email_reg).get()
                    if user_ref.exists:
                        st.warning("Este correo ya está registrado.")
                    else:
                        rol_asignado = "Administrador" if ("admin" in email_reg.lower() or "maestro" in email_reg.lower()) else "Alumno"
                        
                        # Guardar nuevo usuario en Firestore en tiempo real
                        db.collection('usuarios').document(email_reg).set({
                            "nombre": nombre_reg,
                            "password": pass_reg,
                            "rol": rol_asignado,
                            "total": 0,
                            "abonado": 0,
                            "seleccion": "Ninguna"
                        })
                        st.success("¡Cuenta creada con éxito! Ya puede iniciar sesión.")
                else:
                    st.warning("Por favor complete todos los campos.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # ==========================================
    # 2. PANEL PRINCIPAL (POST-LOGIN)
    # ==========================================
    st.title("Club de Ciencias: Orión")
    st.markdown(f"<p style='color: #8D99AE; font-size: 0.9rem;'>Usuario: <b>{st.session_state.nombre_user}</b> | Rol: <span style='color: #48CAE4;'>{st.session_state.rol_user}</span></p>", unsafe_allow_html=True)

    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.email_user = ""
        st.session_state.nombre_user = ""
        st.session_state.rol_user = ""
        st.rerun()

    st.markdown("---")

    if st.session_state.rol_user == "Administrador":
        menu = st.radio("Menu Admin", ["Encuestas", "Pedidos", "Historial (Excel en Tiempo Real)"], horizontal=True, label_visibility="collapsed")
    else:
        menu = st.radio("Menu Alumno", ["Encuestas", "Pedidos"], horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    # SECCIÓN: ENCUESTAS
    if menu == "Encuestas":
        st.subheader("Módulo de Encuestas: Requerimiento de Indumentaria")
        productos = {
            "Playera Oficial": {"precio": 250, "tallas": ["XL", "L", "M", "S", "XS"], "descripcion": "Algodón peinado de alta densidad."},
            "Sudadera con Gorro": {"precio": 450, "tallas": ["XL", "L", "M", "S", "XS"], "descripcion": "Tela polar interior reforzada."},
            "Bolsa Ecológica de Tela": {"precio": 120, "tallas": [], "descripcion": "Lona de alta resistencia."}
        }

        seleccionados = []
        total_encuesta = 0

        for nombre, info in productos.items():
            with st.container():
                st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([2.5, 1.5], gap="medium")
                
                with col1:
                    elegido = st.checkbox(f"**{nombre}**", key=f"chk_{nombre}")
                    st.markdown(f"<p style='color: #8D99AE; font-size: 0.8rem; margin-bottom: 0;'>{info['descripcion']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #48CAE4; font-weight: 600; margin-top: 2px; font-size: 0.9rem;'>Precio: ${info['precio']} MXN</p>", unsafe_allow_html=True)
                
                talla_sel = None
                if elegido:
                    if len(info['tallas']) > 0:
                        with col2:
                            talla_sel = st.selectbox("Talla", info['tallas'], key=f"talla_{nombre}", label_visibility="collapsed")
                    else:
                        with col2:
                            st.markdown("<p style='color: #8D99AE; font-size: 0.8rem; font-style: italic; padding-top: 8px;'>Talla única</p>", unsafe_allow_html=True)
                    
                    seleccionados.append(f"{nombre} ({talla_sel if talla_sel else 'N/A'})")
                    total_encuesta += info['precio']
                st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Guardar Selección en la Nube"):
            if seleccionados:
                user_key = st.session_state.email_user
                # Actualizar directamente en Firestore
                db.collection('usuarios').document(user_key).update({
                    "total": total_encuesta,
                    "seleccion": ", ".join(seleccionados)
                })
                st.success("¡Selección guardada y sincronizada en tiempo real con la nube!")
            else:
                st.warning("Seleccione al menos un producto.")

    # SECCIÓN: PEDIDOS
    elif menu == "Pedidos":
        st.subheader("Módulo de Pedidos y Estado de Cuenta")
        
        # Obtener datos actualizados desde Firestore en tiempo real
        user_doc = db.collection('usuarios').document(st.session_state.email_user).get()
        user_data = user_doc.to_dict() if user_doc.exists else {"total": 0, "abonado": 0, "seleccion": ""}
        
        total_apagar = user_data.get("total", 0)
        total_abonado = user_data.get("abonado", 0)
        restante = total_apagar - total_abonado

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric(label="Total a Pagar", value=f"${total_apagar} MXN")
        with col_p2:
            st.metric(label="Total Abonado", value=f"${total_abonado} MXN")
        with col_p3:
            st.metric(label="Restante Pendiente", value=f"${restante} MXN")

        st.markdown("---")
        st.markdown(f"**Artículos seleccionados:** {user_data.get('seleccion', 'Ninguna')}")
        st.success("Sincronizado en tiempo real con la base de datos de la nube.")

    # SECCIÓN: HISTORIAL / EXCEL (Admin)
    elif menu == "Historial (Excel en Tiempo Real)" and st.session_state.rol_user == "Administrador":
        st.subheader("Panel Administrativo Global (Tipo Excel)")
        st.markdown("<p style='color: #8D99AE; font-size: 0.9rem;'>Modifique los abonos o totales; los cambios se guardan y reflejan al instante para los usuarios.</p>", unsafe_allow_html=True)

        # Leer todos los usuarios de Firestore
        usuarios_ref = db.collection('usuarios').stream()
        df_data = []
        
        for doc in usuarios_ref:
            info = doc.to_dict()
            if info.get("rol") == "Alumno":
                df_data.append({
                    "Correo": doc.id,
                    "Nombre": info.get("nombre", ""),
                    "Selección": info.get("seleccion", ""),
                    "Total ($)": info.get("total", 0),
                    "Abonado ($)": info.get("abonado", 0),
                    "Restante ($)": info.get("total", 0) - info.get("abonado", 0)
                })

        df = pd.DataFrame(df_data)

        if not df.empty:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="cloud_excel")

            # Sincronizar cambios editados en la tabla directamente a Firestore
            for index, row in edited_df.iterrows():
                correo = row["Correo"]
                db.collection('usuarios').document(correo).update({
                    "nombre": row["Nombre"],
                    "abonado": row["Abonado ($)"],
                    "total": row["Total ($)"],
                    "seleccion": row["Selección"]
                })

            st.markdown("---")
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            with col_sum1:
                st.metric("Recaudación Total Esperada", f"${edited_df['Total ($)'].sum()} MXN")
            with col_sum2:
                st.metric("Total Ingresado (Abonos)", f"${edited_df['Abonado ($)'].sum()} MXN")
            with col_sum3:
                st.metric("Deuda Global Pendiente", f"${edited_df['Restante ($)'].sum()} MXN")
        else:
            st.warning("No hay alumnos registrados todavía.")
