import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Streamlit UI
st.title("Interaktives Plotly-Spiel")

# Farben für die Sektoren
outer_colors = ["#F98B1F", "#FFD400", "#C27EA3", "#00A8A0", "#009DDC", "#009E73"]
middle_ring_color = "#f2f2f2"
inner_ring_color = "#D9D9D9"
center_color = "#f2f2f2"

# Radien
r_act = 0.5
r_prepare = 2 * r_act
r_watch = 3 * r_act
r_outer = 3.33 * r_act

# Erstellen der Spuren für die Ringe
fig = go.Figure()

# Äußerer Ring (farbige Sektoren)
angles = np.linspace(90, -270, 7)
for i in range(6):
    theta = np.linspace(angles[i], angles[i+1], 50)
    x_outer = np.cos(np.radians(theta)) * r_outer
    y_outer = np.sin(np.radians(theta)) * r_outer
    x_inner = np.cos(np.radians(theta)) * r_watch
    y_inner = np.sin(np.radians(theta)) * r_watch
    
    fig.add_trace(go.Scatter(x=np.append(x_outer, x_inner[::-1]),
                             y=np.append(y_outer, y_inner[::-1]),
                             fill="toself",
                             line=dict(color='white'),
                             fillcolor=outer_colors[i],
                             mode='lines'))

# "WATCH"-Ring
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=0)))
fig.add_shape(type="circle", xref="x", yref="y",
              x0=-r_watch, y0=-r_watch, x1=r_watch, y1=r_watch,
              line=dict(color=middle_ring_color, width=2))

# "PREPARE"-Ring
fig.add_shape(type="circle", xref="x", yref="y",
              x0=-r_prepare, y0=-r_prepare, x1=r_prepare, y1=r_prepare,
              line=dict(color=inner_ring_color, width=2))

# "ACT"-Kreis in der Mitte
fig.add_shape(type="circle", xref="x", yref="y",
              x0=-r_act, y0=-r_act, x1=r_act, y1=r_act,
              fillcolor=center_color, line=dict(color="white"))

# Linien bis zum Zentrum
for angle in angles:
    x = np.cos(np.radians(angle)) * r_outer
    y = np.sin(np.radians(angle)) * r_outer
    fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode='lines', line=dict(color='white', width=1.5)))

# Äußere Labels
outer_labels = [
    "Passenger Experience", "Enabling Technologies", "Artificial Intelligence",
    "Seamless Mobility", "News Ecology & Sustainability", "Safety & Security"
]
radius_text = 1.56
start_angle = 85

for i, label in enumerate(outer_labels):
    angle_sector = start_angle - i * 60
    angle_rad = np.radians(angle_sector)
    x_text = np.cos(angle_rad) * radius_text
    y_text = np.sin(angle_rad) * radius_text
    fig.add_trace(go.Scatter(x=[x_text], y=[y_text], text=[label], mode='text',
                             textposition='middle center', textfont=dict(color='white', size=12)))

# Interaktive Punkte
point_positions = np.array([
    [0.5 * r_watch, 0.3 * r_watch],  
    [-0.6 * r_watch, 0.3 * r_watch], 
    [0.2 * r_watch, -0.7 * r_watch]  
])

# Streamlit Slider für interaktive Positionierung
for i in range(len(point_positions)):
    point_positions[i][0] = st.slider(f'X-Koordinate Punkt {i+1}', -r_watch, r_watch, point_positions[i][0])
    point_positions[i][1] = st.slider(f'Y-Koordinate Punkt {i+1}', -r_watch, r_watch, point_positions[i][1])

# Punkte hinzufügen
fig.add_trace(go.Scatter(x=point_positions[:, 0], y=point_positions[:, 1], mode='markers',
                         marker=dict(size=10, color="#ffd732")))

# Layout anpassen
fig.update_layout(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    showlegend=False,
    plot_bgcolor="black",
    width=600, height=600
)

# Plotly-Figur in Streamlit anzeigen
st.plotly_chart(fig)


