
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import streamlit as st
# Streamlit UI
st.title("Interaktives Matplotlib-Spiel")
# Farben für die Sektoren
outer_colors = ["#F98B1F", "#FFD400", "#C27EA3", "#00A8A0", "#009DDC", "#009E73"]
middle_ring_color = "#f2f2f2"
inner_ring_color = "#D9D9D9"
center_color = "#f2f2f2"
r_act = 0.5
r_prepare = 2 * r_act
r_watch = 3 * r_act
r_outer = 3.33 * r_act  # Äußerer Ring skaliert
# Matplotlib-Figur erstellen
fig, ax = plt.subplots(figsize=(6,6), subplot_kw={"aspect": "equal"})
# Äußerer Ring (farbige Sektoren)
ax.pie(
    [1]*6,
    radius=r_outer,
    colors=outer_colors,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=r_outer - r_watch, edgecolor="white")
)
# "WATCH"-Ring (mittlerer Ring)
ax.pie(
    [1]*6,
    radius=r_watch,
    colors=[middle_ring_color]*6,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=r_watch - r_prepare, edgecolor="white")
)
# "PREPARE"-Ring (innerer Ring)
ax.pie(
    [1]*6,
    radius=r_prepare,
    colors=[inner_ring_color]*6,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=r_prepare - r_act, edgecolor="white")
)
# "ACT"-Kreis in der Mitte
center_circle = plt.Circle((0, 0), r_act, color=center_color, zorder=0)
ax.add_artist(center_circle)
# Linien bis zum Zentrum
angles = np.linspace(90, -270, 7)
for angle in angles:
    x_start = np.cos(np.radians(angle)) * r_outer
    y_start = np.sin(np.radians(angle)) * r_outer
    ax.plot([x_start, 0], [y_start, 0], color="white", lw=1.5)
    # Platzierung der Texte für die inneren Ringe
ax.text(0.2, -0.3, "ACT", ha="center", va="center", fontsize=9, color="gray")
ax.text(0.5, -0.6, "PREPARE", ha="center", va="center", fontsize=9, color="gray")
ax.text(0.8, -0.9, "WATCH", ha="center", va="center", fontsize=9, color="gray")
# Äußere Labels
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
path_effect = [path_effects.withStroke(linewidth=2, foreground="black")]
for i, label in enumerate(outer_labels):
    angle_sector = start_angle - i * 60  
    letter_spacing = 50 / len(label)  
    for j, char in enumerate(label):
        angle_char = np.radians(angle_sector - j * letter_spacing)  
        x_char = np.cos(angle_char) * radius_text
        y_char = np.sin(angle_char) * radius_text
        ax.text(x_char, y_char, char, ha="center", va="center", fontsize=9, color="white",
                rotation=np.degrees(angle_char) - 90, path_effects=path_effect)
# **Interaktive Punkte (Drag & Drop durch Streamlit-Slider)**
point_positions = np.array([
    [0.5 * r_watch, 0.3 * r_watch],  
    [-0.6 * r_watch, 0.3 * r_watch], 
    [0.2 * r_watch, -0.7 * r_watch]  
])
# Streamlit Slider für interaktives Verschieben der Punkte
for i in range(len(point_positions)):
    point_positions[i][0] = st.slider(f'X-Koordinate Punkt {i+1}', -r_watch, r_watch, point_positions[i][0])
    point_positions[i][1] = st.slider(f'Y-Koordinate Punkt {i+1}', -r_watch, r_watch, point_positions[i][1])
# Punkte auf die neue Position setzen
scatter = ax.scatter(point_positions[:, 0], point_positions[:, 1], color="#ffd732", s=100, zorder=5)
st.pyplot(fig)  # Matplotlib-Plot in Streamlit rendern
