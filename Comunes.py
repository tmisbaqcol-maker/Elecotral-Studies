import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -----------------------------
# Configuración general
# -----------------------------

st.set_page_config(
    page_title="Mapa Comunes Atlántico 2022–2026",
    layout="wide"
)

st.title("🗺️ Mapa Comparativo de Votación")
st.subheader("Partido Comunes – Atlántico (2022 vs Proyección 2026)")

st.markdown("""
🔵 **Azul:** Votación oficial 2022  
🔴 **Rojo:** Proyección 2026 (bases comunitarias)
""")

# -----------------------------
# Datos consolidados
# -----------------------------

data = [
    ["Barranquilla", 10.968540, -74.781320, 867, 414],
    ["Baranoa", 10.794917, -74.916250, 46, 87],
    ["Campo de la Cruz", 10.424444, -74.881389, 24, 0],
    ["Candelaria", 10.459675, -74.880967, 4, 43],
    ["Galapa", 10.896938, -74.886111, 79, 0],
    ["Juan de Acosta", 10.830556, -75.035278, 2, 0],
    ["Luruaco", 10.610414, -75.143242, 8, 405],
    ["Malambo", 10.859722, -74.773611, 60, 0],
    ["Manatí", 10.449239, -74.959369, 3, 65],
    ["Palmar de Varela", 10.740278, -74.754444, 8, 43],
    ["Piojó", 10.754444, -75.107222, 2, 0],
    ["Polonuevo", 10.780294, -74.855747, 5, 45],
    ["Sabanagrande", 10.789769, -74.755200, 0, 46],
    ["Tubará", 10.874714, -74.973850, 0, 80],
]

df = pd.DataFrame(
    data,
    columns=["Municipio", "Lat", "Lon", "Votos_2022", "Votos_2026"]
)

# -----------------------------
# Controles
# -----------------------------

mostrar_2022 = st.checkbox("Mostrar votación 2022", value=True)
mostrar_2026 = st.checkbox("Mostrar proyección 2026", value=True)

# -----------------------------
# Mapa
# -----------------------------

mapa = folium.Map(
    location=[10.8, -74.9],
    zoom_start=9,
    tiles="cartodbpositron"
)

for _, row in df.iterrows():

    if mostrar_2022 and row["Votos_2022"] > 0:
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=max(row["Votos_2022"] / 30, 5),
            color="blue",
            fill=True,
            fill_opacity=0.6,
            popup=f"""
            <b>{row['Municipio']}</b><br>
            🗳️ 2022: {row['Votos_2022']}<br>
            📈 2026: {row['Votos_2026']}
            """
        ).add_to(mapa)

    if mostrar_2026 and row["Votos_2026"] > 0:
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=max(row["Votos_2026"] / 30, 5),
            color="red",
            fill=True,
            fill_opacity=0.7,
            popup=f"""
            <b>{row['Municipio']}</b><br>
            🗳️ 2022: {row['Votos_2022']}<br>
            📈 2026: {row['Votos_2026']}
            """
        ).add_to(mapa)

st_folium(mapa, width=1400, height=700)

# -----------------------------
# Tabla resumen
# -----------------------------

st.subheader("📊 Comparación municipal")

df["Variación"] = df["Votos_2026"] - df["Votos_2022"]
st.dataframe(df[["Municipio", "Votos_2022", "Votos_2026", "Variación"]])