import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Streamlit UI
st.title("Interaktives Matplotlib-Spiel mit Klick-Events")

# Farben für die Sektoren
outer_colors = ["#F98B1F", "#FFD400", "#C27EA3", "#00A8A0", "#009DDC", "#009E73"]
middle_ring_color = "#f2f2f2"
inner_ring_color = "#D9D9D9"
center_color = "#f2f2f2"
r_act = 0.5
r_prepare = 2 * r_act
r_watch = 3 * r_act
r_outer = 3.33 * r_act  # Äußerer Ring skaliert

# Punktepositionen definieren
point_positions = np.array([
    [0.5 * r_watch, 0.3 * r_watch],  
    [-0.6 * r_watch, 0.3 * r_watch], 
    [0.2 * r_watch, -0.7 * r_watch]  
])

# Zustand der Klicks speichern
if "clicked_points" not in st.session_state:
    st.session_state.clicked_points = {i: False for i in range(len(point_positions))}

# Plotly-Figur erstellen
fig = go.Figure()

# Äußerer Ring
fig.add_trace(go.Pie(
    labels=["Passenger Experience", "Enabling Technologies", "Artificial Intelligence", "Seamless Mobility", "News Ecology & Sustainability", "Safety & Security"],
    values=[1]*6,
    marker=dict(colors=outer_colors),
    hole=0.6,
    sort=False,
    direction='clockwise',
    hoverinfo='label',
    textinfo='none'
))

# Innerer Ringe als Kreise
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode='markers',
    marker=dict(size=200, color=center_color),
    hoverinfo='none'
))
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode='markers',
    marker=dict(size=300, color=inner_ring_color),
    hoverinfo='none'
))
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode='markers',
    marker=dict(size=400, color=middle_ring_color),
    hoverinfo='none'
))

# Linien bis zum Zentrum
angles = np.linspace(90, -270, 7)
for angle in angles:
    x_start = np.cos(np.radians(angle)) * r_outer
    y_start = np.sin(np.radians(angle)) * r_outer
    fig.add_trace(go.Scatter(x=[x_start, 0], y=[y_start, 0], mode='lines', line=dict(color='white'), hoverinfo='none'))

# Labels für die inneren Ringe
fig.add_trace(go.Scatter(x=[0.2], y=[-0.3], text=["ACT"], mode="text", textfont=dict(size=12, color="gray"), hoverinfo='none'))
fig.add_trace(go.Scatter(x=[0.5], y=[-0.6], text=["PREPARE"], mode="text", textfont=dict(size=12, color="gray"), hoverinfo='none'))
fig.add_trace(go.Scatter(x=[0.8], y=[-0.9], text=["WATCH"], mode="text", textfont=dict(size=12, color="gray"), hoverinfo='none'))

# Punkte hinzufügen
for i, (x, y) in enumerate(point_positions):
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text' if st.session_state.clicked_points[i] else 'markers',
        marker=dict(size=15, color="yellow"),
        text="Hallo" if st.session_state.clicked_points[i] else "",
        textposition="top center",
        name=f"Punkt {i+1}",
        customdata=[i],
        hoverinfo="text"
    ))

# Zeige das interaktive Diagramm
click = st.plotly_chart(fig, use_container_width=True)

# Funktion zur Aktualisierung des Klick-Status
def toggle_click(event_data):
    if event_data is not None:
        point_index = event_data["points"][0]["customdata"]
        st.session_state.clicked_points[point_index] = not st.session_state.clicked_points[point_index]

# Streamlit Callback für Klick-Events
event = st.experimental_get_query_params()
toggle_click(event)

