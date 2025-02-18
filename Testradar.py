import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math

st.title("Interaktives Plotly-Spiel (Punkte auf WATCH-Ring)")

# --------------------------------
# Parameter (entsprechen grob deinem Matplotlib-Setup)
# --------------------------------
outer_colors = ["#F98B1F", "#FFD400", "#C27EA3", "#00A8A0", "#009DDC", "#009E73"]
middle_ring_color = "#f2f2f2"  # WATCH
inner_ring_color = "#D9D9D9"   # PREPARE
center_color = "#f2f2f2"       # ACT

r_act = 0.5
r_prepare = 2 * r_act
r_watch = 3 * r_act
r_outer = 3.33 * r_act  # Äußerer Ring skaliert

# --------------------------------
# Hilfsfunktion: Pfad für kreisförmige Sektoren (Wedges)
# --------------------------------
def wedge_path(r_inner, r_outer, start_deg, end_deg):
    """
    Erzeugt ein SVG-Pfad-String für Plotly-Shapes,
    um einen kreisförmigen Sektor (Wedge) zu zeichnen.
    """
    start_rad = np.radians(start_deg)
    end_rad = np.radians(end_deg)
    
    # Innere Bogen-Start/Endpunkte
    x0i = r_inner * math.cos(start_rad)
    y0i = r_inner * math.sin(start_rad)
    x1i = r_inner * math.cos(end_rad)
    y1i = r_inner * math.sin(end_rad)
    
    # Äußere Bogen-Start/Endpunkte
    x0o = r_outer * math.cos(start_rad)
    y0o = r_outer * math.sin(start_rad)
    x1o = r_outer * math.cos(end_rad)
    y1o = r_outer * math.sin(end_rad)
    
    # Falls der Sektor > 180° ist, large_arc_flag = 1
    large_arc_inner = 1 if (end_deg - start_deg) > 180 else 0
    large_arc_outer = 1 if (end_deg - start_deg) > 180 else 0
    
    # SVG-Pfad: Bogen im inneren Radius -> Linie zum äußeren Radius -> Bogen zurück
    path = (
        f"M {x0i},{y0i} "
        f"A {r_inner},{r_inner} 0 {large_arc_inner},1 {x1i},{y1i} "
        f"L {x1o},{y1o} "
        f"A {r_outer},{r_outer} 0 {large_arc_outer},0 {x0o},{y0o} Z"
    )
    return path

# --------------------------------
# Plotly-Figur erstellen
# --------------------------------
fig = go.Figure()
fig.update_layout(
    width=600,
    height=600,
    xaxis=dict(range=[-3.5, 3.5], showgrid=False, zeroline=False),
    yaxis=dict(range=[-3.5, 3.5], showgrid=False, zeroline=False, scaleanchor='x', scaleratio=1),
    plot_bgcolor="white",
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False,
    # Klick-Events erlauben (blaue Markierung)
    clickmode='event+select'
)

# --------------------------------
# Äußerer Ring (6 farbige Sektoren)
# --------------------------------
start_angle = 90
for i in range(6):
    sector_start = start_angle - i * 60
    sector_end = sector_start - 60
    color = outer_colors[i]
    shape = dict(
        type='path',
        path=wedge_path(r_watch, r_outer, sector_start, sector_end),
        fillcolor=color,
        line=dict(color='white', width=1),
        layer='below'  
    )
    fig.add_shape(shape)

# --------------------------------
# WATCH-Ring (ein großer, grauer Ring)
# --------------------------------
shape_watch = dict(
    type='path',
    path=wedge_path(r_prepare, r_watch, 90, -270),
    fillcolor=middle_ring_color,
    line=dict(color='white', width=1),
    layer='below'
)
fig.add_shape(shape_watch)

# --------------------------------
# PREPARE-Ring
# --------------------------------
shape_prepare = dict(
    type='path',
    path=wedge_path(r_act, r_prepare, 90, -270),
    fillcolor=inner_ring_color,
    line=dict(color='white', width=1),
    layer='below'
)
fig.add_shape(shape_prepare)

# --------------------------------
# ACT-Kreis in der Mitte
# --------------------------------
shape_center = dict(
    type='circle',
    xref='x', yref='y',
    x0=-r_act, x1=r_act, y0=-r_act, y1=r_act,
    fillcolor=center_color,
    line_color=center_color,
    layer='below'
)
fig.add_shape(shape_center)

# --------------------------------
# Linien vom Zentrum nach außen
# --------------------------------
angles = np.linspace(90, -270, 7)
for angle in angles:
    rad = np.radians(angle)
    x_end = r_outer * math.cos(rad)
    y_end = r_outer * math.sin(rad)
    shape_line = dict(
        type='line',
        x0=0, y0=0,
        x1=x_end, y1=y_end,
        line=dict(color='white', width=1.5),
        layer='above'
    )
    fig.add_shape(shape_line)

# --------------------------------
# Labels für die inneren Ringe (ACT, PREPARE, WATCH)
# --------------------------------
fig.add_annotation(
    x=0.2, y=-0.3,
    text="ACT",
    showarrow=False,
    font=dict(size=10, color="gray")
)
fig.add_annotation(
    x=0.5, y=-0.6,
    text="PREPARE",
    showarrow=False,
    font=dict(size=10, color="gray")
)
fig.add_annotation(
    x=0.8, y=-0.9,
    text="WATCH",
    showarrow=False,
    font=dict(size=10, color="gray")
)

# --------------------------------
# Äußere Labels (um den Ring herum)
# --------------------------------
outer_labels = [
    "Passenger Experience",
    "Enabling Technologies",
    "Artificial Intelligence",
    "Seamless Mobility",
    "News Ecology & Sustainability",
    "Safety & Security"
]
radius_text = 1.56
start_angle = 85

for i, label in enumerate(outer_labels):
    angle_sector = start_angle - i * 60
    letter_spacing = 50 / len(label)
    for j, char in enumerate(label):
        angle_char = np.radians(angle_sector - j * letter_spacing)
        x_char = radius_text * np.cos(angle_char)
        y_char = radius_text * np.sin(angle_char)
        
        fig.add_annotation(
            x=x_char, y=y_char,
            text=char,
            showarrow=False,
            font=dict(size=9, color='white'),
            textangle=np.degrees(angle_char) - 90
        )

# --------------------------------
# Punkte auf dem WATCH-Ring
# --------------------------------
# 3 Punkte bei 0°, 120°, 240° (auf Radius r_watch)
angles_deg = [0, 120, 240]
xs = [r_watch * np.cos(np.radians(a)) for a in angles_deg]
ys = [r_watch * np.sin(np.radians(a)) for a in angles_deg]
hover_texts = [f"Hello {i+1}" for i in range(len(xs))]

# Punkte-Trace mit Hover- und Klick-Unterstützung
fig.add_trace(go.Scatter(
    x=xs,
    y=ys,
    mode="markers",
    marker=dict(size=12, color="#ffd732"),
    text=hover_texts,
    hoverinfo="text",  # zeigt nur den Text an
    name="WATCH-Points"
))

# --------------------------------
# Plotly-Grafik in Streamlit anzeigen
# --------------------------------
st.plotly_chart(fig, use_container_width=True)



