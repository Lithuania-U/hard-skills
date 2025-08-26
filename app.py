import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math
import random

st.set_page_config(page_title="Hard Skills Diagrama", layout="wide")

# --- DUOMENYS ---
def get_skills_data():
    """Grąžina visų įgūdžių duomenis kaip (pavadinimas, kampas, maksimalus_lygis) tuple'ų sąrašą"""
    return [
        ("PSICHOLOGIJA", 310, 8),
        ("MĄSTYMAS, FILOSOFIJA", 320, 9),
        ("BIOLOGIJA, NEUROMOKSLAI", 330, 9),
        ("MEDICINOS MOKSLAI", 340, 9),
        ("CHEMIJA, BIOTECHNOLOGIJOS", 350, 10),
        ("MATEMATIKA, KVANTINĖ FIZIKA", 0, 10),
        ("DIRBTINIS INTELEKTAS, MAŠINŲ MOKYMAS", 10, 10),
        ("FIZIKA, ELEKTRONIKA, KOMPIUTERIJA", 20, 10),
        ("INŽINERIJA", 30, 10),
        ("ELEKTROTECHNIKA", 40, 9),
        ("MECHANIKA", 50, 9),
        ("ARCHITEKTŪRA, MODELIAVIMAS", 60, 9),
        ("STATISTIKA, DUOMENYS", 70, 8),
        ("FINANSAI, EKONOMIKA", 80, 8),
        ("ĮSTATYMAI, TEISĖ", 90, 7),
        ("POLITIKA", 100, 7),
        ("VALDŽIA, VALSTYBĖ", 110, 7),
        ("RAŠTAS, SKAIČIAI", 120, 6),
        ("AMATAI, PREKYBA", 130, 6),
        ("BŪSTAS, STATYBA", 140, 5),
        ("RELIGIJOS", 150, 5),
        ("KELIONĖS, ATRADIMAI", 160, 5),
        ("AGRESIJA, DOMINAVIMAS", 170, 4),
        ("FIZINĖ JĖGA", 180, 3),
        ("MAISTAS", 190, 3),
        ("SEKSAS, VAIKAI", 200, 2),
        ("ŠILUMA, BUITIS", 210, 2),
        ("VALGIO RUOŠIMAS", 220, 3),
        ("GLOBA/RŪPYBA", 230, 3),
        ("EMPATIJA", 240, 4),
        ("PUOŠYBA", 250, 4),
        ("MUZIKA, ŠOKIS", 260, 4),
        ("DRAMATIKA, GINČAI", 270, 4),
        ("LITERATŪRA", 280, 5),
        ("MEDIA, DIZAINAS", 290, 5),
        ("ISTORIJA, ŽURNALISTIKA", 300, 6)
    ]

def create_circular_diagram(user_skills=None):
    """Sukuria apskritimo diagramą su įgūdžių duomenimis"""
    skills_data = get_skills_data()
    level_colors = {
        1: "#808080",   # Pilka
        2: "#FFD700",   # Geltona
        3: "#FF69B4",   # Rožinė
        4: "#FFA500",   # Oranžinė
        5: "#FF0000",   # Raudona
        6: "#7CFC00",   # Salotinė
        7: "#008000",   # Žalia
        8: "#4B0082",   # Indigo
        9: "#0000FF",   # Mėlyna
        10: "#FFFFFF"   # Balta
    }

    fig = go.Figure()
    
    # Fono įgūdžiai
    for skill_name, angle, level in skills_data:
        theta_rad = math.radians(90 - angle)
        x_line = [0, level * math.cos(theta_rad)]
        y_line = [0, level * math.sin(theta_rad)]
        
        # Linija
        fig.add_trace(go.Scatter(
            x=x_line, y=y_line, 
            mode="lines", 
            line=dict(color=level_colors.get(level, "gray"), width=1), 
            showlegend=False, 
            hoverinfo="skip"
        ))
        
        # Taškas
        fig.add_trace(go.Scatter(
            x=[level * math.cos(theta_rad)], 
            y=[level * math.sin(theta_rad)],
            mode="markers", 
            marker=dict(
                color=level_colors.get(level, "gray"), 
                size=6, 
                line=dict(color="white", width=1)
            ),
            name=f"FONAS: {skill_name}",
            hovertemplate=f"<b>FONAS: {skill_name}</b><br>Kampas: {angle}°<br>Sudėtingumas: {level}/10<extra></extra>", 
            showlegend=False
        ))

    # Vartotojo įgūdžiai
    if user_skills:
        for skill_name, angle, max_level in skills_data:
            user_level = user_skills.get(skill_name, 0)
            if user_level > 0:
                theta_rad = math.radians(90 - angle)
                x_line = [0, user_level * math.cos(theta_rad)]
                y_line = [0, user_level * math.sin(theta_rad)]
                
                # Linija
                fig.add_trace(go.Scatter(
                    x=x_line, y=y_line, 
                    mode="lines", 
                    line=dict(color=level_colors.get(user_level, "#FFF"), width=3), 
                    showlegend=False, 
                    hoverinfo="skip"
                ))
                
                # Taškas
                fig.add_trace(go.Scatter(
                    x=[user_level * math.cos(theta_rad)], 
                    y=[user_level * math.sin(theta_rad)],
                    mode="markers", 
                    marker=dict(
                        color=level_colors.get(user_level, "#FFF"), 
                        size=12,
                        line=dict(color="white", width=2)
                    ),
                    name=f"Tavo: {skill_name}",
                    hovertemplate=f"<b>TAVO ĮVERTINIMAS: {skill_name}</b><br>Kampas: {angle}°<br>Tavo lygis: {user_level}/10<br>Maksimalus: {max_level}/10<extra></extra>", 
                    showlegend=False
                ))

    # Koncentriniai apskritimai
    for r in range(1, 13):
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        x_circle = r * np.cos(theta_circle)
        y_circle = r * np.sin(theta_circle)
        
        circle_color = "orange" if r >= 11 else "gray"
        
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle, 
            mode="lines", 
            line=dict(color=circle_color, width=0.5), 
            showlegend=False, 
            hoverinfo="skip"
        ))

    # Radialinės linijos kas 5 laipsniai
    for angle in range(0, 360, 5):
        theta_rad = math.radians(90 - angle)
        x_line = [0, 12 * math.cos(theta_rad)]
        y_line = [0, 12 * math.sin(theta_rad)]
        fig.add_trace(go.Scatter(
            x=x_line, y=y_line, 
            mode="lines", 
            line=dict(color="gray", width=0.2),
            showlegend=False, 
            hoverinfo="skip"
        ))

    # Sudėtingumo laipsniai ant 85 laipsnių vektoriaus
    for level in range(1, 11):
        theta_rad = math.radians(90 - 85)
        x = level * math.cos(theta_rad)
        y = level * math.sin(theta_rad)
        fig.add_trace(go.Scatter(
            x=[x], y=[y], 
            mode="text", 
            text=[str(level)], 
            textposition="middle center", 
            showlegend=False, 
            hoverinfo="skip", 
            textfont=dict(color="white", size=10, family="Arial Black")
        ))

    # Laipsnių žymės kas 15 laipsnių ant 11.5 spinduliu apskritimo
    for angle in range(0, 360, 15):
        theta_rad = math.radians(90 - angle)
        x = 11.5 * math.cos(theta_rad)
        y = 11.5 * math.sin(theta_rad)
        fig.add_trace(go.Scatter(
            x=[x], y=[y], 
            mode="text", 
            text=[f"{angle}°"], 
            textposition="middle center", 
            showlegend=False, 
            hoverinfo="skip", 
            textfont=dict(color="lightgray", size=8)
        ))

    # Etiketės
    labels = {
        0: "MATEMATINIS, LOGINIS PROTAS",
        90: "ORGANIZACINIS, VALDŽIA",
        180: "FIZINIS, GENAI, JĖGA",
        270: "JAUSMAI, EMOCIJOS"
    }
    for angle, text in labels.items():
        theta_rad = math.radians(90 - angle)
        x = 13 * math.cos(theta_rad)
        y = 13 * math.sin(theta_rad)
        fig.add_trace(go.Scatter(
            x=[x], y=[y], 
            mode="text", 
            text=[text], 
            textposition="middle center", 
            showlegend=False, 
            hoverinfo="skip", 
            textfont=dict(color="white", size=12)
        ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            range=[-14, 14], 
            showgrid=False, 
            zeroline=False, 
            showticklabels=False, 
            scaleanchor="y", 
            scaleratio=1
        ),
        yaxis=dict(
            range=[-14, 14], 
            showgrid=False, 
            zeroline=False, 
            showticklabels=False
        ),
        plot_bgcolor="black", 
        paper_bgcolor="black",
        width=800, 
        height=800,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def render_downloads(fig, user_skills):
    """Atvaizduoja atsisiuntimo mygtukus"""
    col1, col2 = st.columns(2)
    
    with col1:
        # HTML su visa Plotly diagrama
        try:
            html_str = fig.to_html(include_plotlyjs="cdn", full_html=True)
            st.download_button(
                label="🖼️ Atsisiųsti HTML (diagrama + duomenys)", 
                data=html_str.encode("utf-8"), 
                file_name="hard_skills_diagrama.html", 
                mime="text/html"
            )
        except Exception as e:
            st.error(f"Klaida generuojant HTML: {e}")
    
    with col2:
        # CSV su lentelės duomenimis
        try:
            skills = get_skills_data()
            rows = []
            for name, angle, max_level in skills:
                user_level = user_skills.get(name, 0)
                if user_level is None:
                    user_level = 0
                rows.append({
                    "skill": name, 
                    "angle_deg": angle, 
                    "max_level": max_level, 
                    "user_level": int(user_level)
                })
            df = pd.DataFrame(rows)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📄 Atsisiųsti CSV (duomenys)", 
                data=csv, 
                file_name="hard_skills_data.csv", 
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Klaida generuojant CSV: {e}")

def main():
    st.title("🎯 Hard Skills Diagrama")
    
    st.markdown("""
    Pabandyk sąžiningai įsivertinti savo gebėjimus pagal unikalią sistemą, kuri daug aiškiau atskleis, kur esi ir kur nori nukeliauti, lavindamas savo kietuosius įgūdžius, susijusius su veikla ir profesija. Žiūrėk, žiūrėk, ir sėkmė greit nusišypsos.
    
    **Svarbiausias klausimas:** Kuri kryptis tau ar vaikui yra mėgiama ir kokio lygio tavo pažanga?
    
    Išvardintos 36 PROFESINĖS KRYPTYS. Apytiksliai. Pildyk tas, kurios atrodo svarbiausios ir taip kaip supranti. Arba įvertink visas, tuomet gausi daug detalesnį ataskaitą ir tikslesnių patarimų.
    
    Čia pirmas etapas iš [https://sekmes.lt](https://sekmes.lt) projekto švietimo tema. Antras etapas bus vartotojų profiliai (jei prireiks) ir psichologiniai tipai, o trečias - DI agentas, kuris duos neįtikėtinai tikslių patarimų. Greit :)
    """)
    
    st.markdown("---")

    skills_data = get_skills_data()

    # Inicializuojame session state
    if "user_skills" not in st.session_state:
        st.session_state.user_skills = {skill[0]: 0 for skill in skills_data}

    if "randomized_skills" not in st.session_state:
        st.session_state.randomized_skills = skills_data.copy()
        random.shuffle(st.session_state.randomized_skills)

    # Diagrama viršuje
    user_skills = st.session_state.user_skills
    fig = create_circular_diagram(user_skills)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistika
    evaluated_count = len([skill for skill, level in user_skills.items() if level and level > 0])
    total_count = len(skills_data)
    
    st.metric("📊 Įvertinta sričių", f"{evaluated_count} iš {total_count}")
    
    st.markdown("---")

    # Slideriai po diagrama
    st.header("🎯 Įvertink savo gebėjimus")
    st.markdown("*Nustatyk savo lygį kiekvienai sričiai (0—maksimumas)*")
    
    # Mygtukai viršuje
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔥 Išvalyti visus", use_container_width=True):
            for skill_name, _, _ in skills_data:
                st.session_state.user_skills[skill_name] = 0
            st.rerun()
    
    with col2:
        if st.button("🎲 Maišyti tvarką", use_container_width=True):
            st.session_state.randomized_skills = skills_data.copy()
            random.shuffle(st.session_state.randomized_skills)
            st.rerun()

    # Slideriai 3 stulpeliuose
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    for i, (skill_name, angle, max_level) in enumerate(st.session_state.randomized_skills):
        with columns[i % 3]:
            current_value = st.session_state.user_skills.get(skill_name, 0)
            safe_value = min(current_value, max_level) if current_value else 0
            
            # Kompaktiškas pavadinimas
            short_name = skill_name.replace(", ", "/")
            if len(short_name) > 30:
                short_name = short_name[:27] + "..."
            
            user_level = st.slider(
                f"{short_name}", 
                min_value=0, 
                max_value=max_level, 
                value=safe_value, 
                key=f"skill_{skill_name}",
                help=f"Pilnas pavadinimas: {skill_name} (max: {max_level})"
            )
            st.session_state.user_skills[skill_name] = user_level

    st.markdown("---")
    
    # Atsisiuntimo mygtukai
    st.header("⬇️ Atsisiųsti duomenis")
    render_downloads(fig, user_skills)

    # Sudėtingumo lygių paaiškinimas
    with st.expander("ℹ️ SUDĖTINGUMO LYGIŲ PAAIŠKINIMAS IR SPALVOS"):
        st.markdown("""
        **1—10 STIPRUMO (SUDĖTINGUMO) LYGIAI**

        - ⚫ **1 (Pilka)** — Kūdikiai (motorika, aplinkos suvokimas) / 3—5 m. vaikų lygis
        - 🟡 **2 (Geltona)** — 6—13 m. mokinių teorinės žinios, labiau nei praktiniai įgūdžiai
        - 🌸 **3 (Rožinė)** — 14—18 m. jaunimo lygis, stiprūs protiniai gebėjimai, silpnesnė praktika
        - 🟠 **4 (Oranžinė)** — Vidutinis lygis — paprasti darbai (Excel, Photoshop, blynų kepimas)
        - 🔴 **5 (Raudona)** — Mokyklos „devyntukai", vidutinio sudėtingumo lygis
        - 🟢 **6 (Salotinė)** — Automechaniko pameistrys, stiprus geimeris, pradedantis kūrėjas
        - 💚 **7 (Žalia)** — Studentų / jaunųjų profesionalų lygis (Middle developer)
        - 🔮 **8 (Indigo)** — Gyvenimo herojai, nacionalinio lygio senior specialistai
        - 🔵 **9 (Mėlyna)** — Aukščiausias meistršiškumas, tarptautinių projektų lygis
        - ⚪ **10 (Balta)** — Genijų lygis, pasaulinio masto inovatoriai
        """)

if __name__ == "__main__":
    main()
