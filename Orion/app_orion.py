import datetime
import pandas as pd
import streamlit as st

# Configuración de la página (Compatible con móviles y escritorio)
st.set_page_config(
    page_title="Club de Ciencias: Orión",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS ejecutivos, limpios y profesionales
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
# SISTEMA DE MEMORIA Y BASE DE DATOS LOCAL EN VIVO
# ---------------------------------------------------------
if "usuarios_nube" not in st.session_state:
    st.session_state.usuarios_nube = {
        "alvarezgro36@gmail.com": {
            "nombre": "Administrador General",
            "password": "insanoff1",
            "rol": "Administrador",
            "total": 0,
            "abonado": 0,
            "seleccion": "N/A"
        },
        "alumno@orion.edu": {
            "nombre": "Eneas Alvarez",
            "password": "123",
            "rol": "Alumno",
            "total": 700,
            "abonado": 200,
            "seleccion": "Playera Oficial (M), Sudadera (L)"
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email_user = ""
    st.session_state.nombre_user = ""
    st.session_state.rol_user = ""

# ==========================================
# 1. PANTALLA DE ACCESO (LOGIN / REGISTRO CON MEMORIA)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Club de Ciencias: Orión</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8D99AE;'>Plataforma Institucional de Control y Encuestas</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        # Pestañas para elegir entre Iniciar Sesión o Registrarse
        tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Registrarse"])
        
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            email_login = st.text_input("Correo Institucional", placeholder="tu_correo@orion.edu", key="log_email")
            pass_login = st.text_input("Contraseña", type="password", key="log_pass")
            
            if st.button("Entrar a la Plataforma", use_container_width=True):
                if email_login in st.session_state.usuarios_nube:
                    if st.session_state.usuarios_nube[email_login]["password"] == pass_login:
                        # MEMORIA DE SESIÓN ACTIVADA
                        st.session_state.logged_in = True
                        st.session_state.email_user = email_login
                        st.session_state.nombre_user = st.session_state.usuarios_nube[email_login]["nombre"]
                        st.session_state.rol_user = st.session_state.usuarios_nube[email_login]["rol"]
                        st.rerun()
                    else:
                        st.error("Contraseña incorrecta.")
                else:
                    st.error("El correo no está registrado. Regístrese en la pestaña contigua.")
        
        with tab_registro:
            st.markdown("<br>", unsafe_allow_html=True)
            nombre_reg = st.text_input("Nombre Completo", placeholder="Ej. Carlos Mendoza", key="reg_name")
            email_reg = st.text_input("Correo Institucional", placeholder="ejemplo@orion.edu", key="reg_email")
            pass_reg = st.text_input("Crear Contraseña", type="password", key="reg_pass")
            
            if st.button("Crear Cuenta", use_container_width=True):
                if nombre_reg and email_reg and pass_reg:
                    if email_reg in st.session_state.usuarios_nube:
                        st.warning("Este correo ya está registrado.")
                    else:
                        # Asignación automática de rol según el correo
                        rol_asignado = "Administrador" if ("admin" in email_reg.lower() or "maestro" in email_reg.lower()) else "Alumno"
                        
                        st.session_state.usuarios_nube[email_reg] = {
                            "nombre": nombre_reg,
                            "password": pass_reg,
                            "rol": rol_asignado,
                            "total": 0,
                            "abonado": 0,
                            "seleccion": "Ninguna"
                        }
                        st.success("¡Cuenta creada con éxito! Ya puede iniciar sesión.")
                else:
                    st.warning("Por favor complete todos los campos.")
                    
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # ==========================================
    # 2. PANEL PRINCIPAL (POST-LOGIN)
    # ==========================================
    st.title("Club de Ciencias: Orión")
    st.markdown(f"<p style='color: #8D99AE; font-size: 0.9rem;'>Usuario: <b>{st.session_state.nombre_user}</b> ({st.session_state.email_user}) | Rol: <span style='color: #48CAE4;'>{st.session_state.rol_user}</span></p>", unsafe_allow_html=True)

    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.email_user = ""
        st.session_state.nombre_user = ""
        st.session_state.rol_user = ""
        st.rerun()

    st.markdown("---")

    # Menú adaptativo según el rol
    if st.session_state.rol_user == "Administrador":
        menu = st.radio("Menu Admin", ["Encuestas", "Pedidos", "Historial (Excel en Tiempo Real)"], horizontal=True, label_visibility="collapsed")
    else:
        menu = st.radio("Menu Alumno", ["Encuestas", "Pedidos"], horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    # SECCIÓN: ENCUESTAS
    if menu == "Encuestas":
        st.subheader("Módulo de Encuestas: Requerimiento de Indumentaria")
        st.markdown("<p style='color: #8D99AE; font-size: 0.9rem;'>Seleccione los artículos requeridos.</p>", unsafe_allow_html=True)

        productos = {
            "Playera Oficial": {
                "precio": 250, 
                "tallas": ["XL", "L", "M", "S", "XS"],
                "descripcion": "Algodón peinado de alta densidad."
            },
            "Sudadera con Gorro": {
                "precio": 450, 
                "tallas": ["XL", "L", "M", "S", "XS"],
                "descripcion": "Tela polar interior reforzada."
            },
            "Bolsa Ecológica de Tela": {
                "precio": 120, 
                "tallas": [],
                "descripcion": "Lona de alta resistencia."
            }
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

        if st.button("Guardar Selección en Pedidos"):
            if seleccionados:
                user_key = st.session_state.email_user
                st.session_state.usuarios_nube[user_key]["total"] = total_encuesta
                st.session_state.usuarios_nube[user_key]["seleccion"] = ", ".join(seleccionados)
                st.success("¡Selección guardada con éxito en su estado de cuenta!")
            else:
                st.warning("Seleccione al menos un producto.")

    # SECCIÓN: PEDIDOS (Vista Alumno)
    elif menu == "Pedidos":
        st.subheader("Módulo de Pedidos y Estado de Cuenta")
        user_data = st.session_state.usuarios_nube.get(st.session_state.email_user, {"total": 0, "abonado": 0, "seleccion": ""})
        
        total_apagar = user_data["total"]
        total_abonado = user_data["abonado"]
        restante = total_apagar - total_abonado

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric(label="Total a Pagar", value=f"${total_apagar} MXN")
        with col_p2:
            st.metric(label="Total Abonado", value=f"${total_abonado} MXN")
        with col_p3:
            st.metric(label="Restante Pendiente", value=f"${restante} MXN")

        st.markdown("---")
        st.markdown(f"**Artículos seleccionados:** {user_data['seleccion'] if user_data['seleccion'] else 'Ninguno'}")
        st.info("Sus montos y abonos se actualizan automáticamente en tiempo real conforme el administrador los modifica.")

    # SECCIÓN: HISTORIAL / EXCEL (Vista Administrador)
    elif menu == "Historial (Excel en Tiempo Real)" and st.session_state.rol_user == "Administrador":
        st.subheader("Panel Administrativo Global (Tipo Excel)")
        st.markdown("<p style='color: #8D99AE; font-size: 0.9rem;'>Gestione los nombres, abonos y totales de los usuarios directamente en la tabla.</p>", unsafe_allow_html=True)

        df_data = []
        for correo, info in st.session_state.usuarios_nube.items():
            if info["rol"] == "Alumno":
                df_data.append({
                    "Correo": correo,
                    "Nombre": info["nombre"],
                    "Selección": info["seleccion"],
                    "Total ($)": info["total"],
                    "Abonado ($)": info["abonado"],
                    "Restante ($)": info["total"] - info["abonado"]
                })

        df = pd.DataFrame(df_data)

        if not df.empty:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="cloud_excel")

            for index, row in edited_df.iterrows():
                correo = row["Correo"]
                if correo in st.session_state.usuarios_nube:
                    st.session_state.usuarios_nube[correo]["nombre"] = row["Nombre"]
                    st.session_state.usuarios_nube[correo]["abonado"] = row["Abonado ($)"]
                    st.session_state.usuarios_nube[correo]["total"] = row["Total ($)"]
                    st.session_state.usuarios_nube[correo]["seleccion"] = row["Selección"]

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