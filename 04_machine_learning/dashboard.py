import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scoring Crediticio - Asesor", layout="wide")

st.title("Sistema Inteligente de Evaluación Crediticia MYPE")
st.markdown("Herramienta prescriptiva para asesores de negocio y comités de riesgo.")

# Barra lateral para ingreso de cliente
st.sidebar.header("Datos del Solicitante")
cliente_id = st.sidebar.number_input("ID Cliente", value=1024, step=1)
linea = st.sidebar.slider("Línea de Crédito Solicitada (S/)", 1000, 500000, 25000, step=5000)
edad = st.sidebar.slider("Edad", 18, 75, 34)
pay_0 = st.sidebar.selectbox("Estado de Pago Reciente (pay_0)", 
                             options=[-1, 0, 1, 2, 3],
                             format_func=lambda x: {
                                 -1: "Al día (Sin deuda vencida)",
                                 0: "Pago puntual",
                                 1: "Atraso 1 mes",
                                 2: "Atraso 2 meses",
                                 3: "Atraso 3+ meses"
                             }[x])
max_atraso = st.sidebar.slider("Máximo Atraso Histórico (Meses)", 0, 6, 0)
rec_delay = st.sidebar.slider("Meses con Atraso Reciente", 0, 6, 0)

# Motor de cálculo
score = 0.12
if pay_0 > 0: score += (pay_0 * 0.18)
if rec_delay > 0: score += (rec_delay * 0.12)
if max_atraso >= 2: score += 0.15

pd_calc = round(min(max(score, 0.02), 0.96), 4)

col1, col2, col3 = st.columns(3)
col1.metric("Probabilidad de Mora (PD)", f"{pd_calc*100:.1f}%")
col2.metric("Decisión Threshold (0.38)", "RECHAZO / ALERTA" if pd_calc >= 0.38 else "APROBADO")

if pd_calc < 0.20:
    col3.success("RIESGO BAJO")
    st.info(f"Acción Prescriptiva: Cliente Apto. Ofertar incremento hasta S/ {linea*1.30:,.0f}.")
elif pd_calc < 0.40:
    col3.warning("RIESGO MEDIO")
    st.info("Acción Prescriptiva: Monitoreo preventivo. Mantener línea sin cambios.")
elif pd_calc < 0.70:
    col3.error("RIESGO ALTO")
    st.info(f"Acción Prescriptiva: Restricción preventiva de sobregiro. Reducir línea a S/ {linea*0.70:,.0f}.")
else:
    col3.error("RIESGO CRÍTICO")
    st.info("Acción Prescriptiva: Bloqueo inmediato de tarjeta y pase a cobranza prejudicial.")