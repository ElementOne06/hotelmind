
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="HotelMind MVP",
    page_icon="🏨",
    layout="wide"
)

st.title("🏨 HotelMind")
st.subheader("Dashboard inteligente para hoteles pequeños y medianos")

st.write(
    "Esta primera versión muestra métricas básicas del hotel: ingresos, gastos, "
    "utilidad, ocupación, ADR y RevPAR."
)

# -----------------------------
# Datos simulados
# -----------------------------

habitaciones = pd.DataFrame({
    "habitacion": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "tipo": ["Doble", "King", "Suite", "Doble", "Sencilla", "King", "Doble", "Suite", "Sencilla", "Doble"],
    "estado": ["Ocupada", "Disponible", "Ocupada", "Limpieza", "Ocupada", "Disponible", "Mantenimiento", "Ocupada", "Disponible", "Ocupada"],
    "precio_base": [1500, 1800, 2800, 1500, 1000, 1800, 1500, 2800, 1000, 1500]
})

reservaciones = pd.DataFrame({
    "cliente": ["Juan Pérez", "Ana López", "Carlos Ruiz", "María García", "Pedro Sánchez"],
    "habitacion": [101, 103, 105, 108, 110],
    "canal": ["Booking", "Directo", "Airbnb", "WhatsApp", "Expedia"],
    "estado": ["En curso", "En curso", "En curso", "En curso", "En curso"],
    "noches": [2, 3, 1, 2, 4],
    "precio_por_noche": [1500, 2800, 1000, 2800, 1500]
})

ingresos = pd.DataFrame({
    "concepto": ["Hospedaje", "Hospedaje", "Hospedaje", "Restaurante", "Tours"],
    "monto": [3000, 8400, 1000, 2500, 1800]
})

gastos = pd.DataFrame({
    "categoria": ["Limpieza", "Mantenimiento", "Luz", "Agua", "Comisiones"],
    "monto": [900, 1500, 2200, 800, 1200]
})

# -----------------------------
# Cálculos principales
# -----------------------------

habitaciones_totales = len(habitaciones)
habitaciones_ocupadas = len(habitaciones[habitaciones["estado"] == "Ocupada"])
habitaciones_disponibles = habitaciones_totales

ingresos_totales = ingresos["monto"].sum()
gastos_totales = gastos["monto"].sum()
utilidad = ingresos_totales - gastos_totales

ingresos_hospedaje = ingresos[ingresos["concepto"] == "Hospedaje"]["monto"].sum()
habitaciones_vendidas = len(reservaciones)

ocupacion = habitaciones_ocupadas / habitaciones_disponibles
adr = ingresos_hospedaje / habitaciones_vendidas
revpar = ingresos_hospedaje / habitaciones_disponibles

# -----------------------------
# Métricas
# -----------------------------

st.markdown("## Métricas principales")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Ingresos totales", f"${ingresos_totales:,.0f}")
col2.metric("Gastos totales", f"${gastos_totales:,.0f}")
col3.metric("Utilidad estimada", f"${utilidad:,.0f}")
col4.metric("Ocupación", f"{ocupacion:.1%}")

col5, col6, col7 = st.columns(3)

col5.metric("ADR", f"${adr:,.0f}")
col6.metric("RevPAR", f"${revpar:,.0f}")
col7.metric("Habitaciones ocupadas", f"{habitaciones_ocupadas}/{habitaciones_totales}")

# -----------------------------
# Gráficas
# -----------------------------

st.markdown("## Gráficas")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.write("Ingresos por concepto")
    ingresos_grafica = ingresos.groupby("concepto")["monto"].sum()
    st.bar_chart(ingresos_grafica)

with col_graf2:
    st.write("Gastos por categoría")
    gastos_grafica = gastos.groupby("categoria")["monto"].sum()
    st.bar_chart(gastos_grafica)

# -----------------------------
# Tablas
# -----------------------------

st.markdown("## Habitaciones")
st.dataframe(habitaciones, use_container_width=True)

st.markdown("## Reservaciones")
st.dataframe(reservaciones, use_container_width=True)

# -----------------------------
# Recomendaciones básicas
# -----------------------------

st.markdown("## Recomendaciones inteligentes")

if ocupacion > 0.80:
    st.success("La ocupación es alta. Podrías considerar subir precios en fechas próximas.")
elif ocupacion < 0.40:
    st.warning("La ocupación es baja. Podrías lanzar una promoción o revisar tus canales de venta.")
else:
    st.info("La ocupación está en un nivel medio. Conviene monitorear ingresos y reservas próximas.")

if gastos_totales > ingresos_totales * 0.60:
    st.warning("Los gastos representan más del 60% de los ingresos. Revisa categorías como mantenimiento, comisiones o servicios.")
else:
    st.success("Los gastos se mantienen en un rango razonable frente a los ingresos.")