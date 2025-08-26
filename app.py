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

# --- PATARIMAI ---
skill_tips = {
    "PSICHOLOGIJA": ["Skaityk atvejų analizes", "Gilinkis į psichoterapijos metodus", "Praktikuok aktyvų klausymą", "Dalyvauk psichologijos konferencijose", "Savanoriauk emocinės pagalbos linijoje"],
    "MĄSTYMAS, FILOSOFIJA": ["Analizuok filosofinius tekstus", "Diskutuok su bendraminčiais", "Kurti filosofinius esė", "Skaitinėk originalius šaltinius (Platonas, Kantas)", "Klausyk paskaitų YouTube ar podcast'uose"],
    "BIOLOGIJA, NEUROMOKSLAI": ["Tyrinėk laboratorinius darbus", "Sek naujausius mokslo straipsnius", "Eksperimentuok su duomenų analize", "Praktikuok mikroskopiją", "Gilinkis į genetiką"],
    "MEDICINOS MOKSLAI": ["Mokykis iš klinikinių atvejų", "Dalyvauk praktikose ligoninėse", "Gilinkis į anatomiją", "Studijuok farmacijos pagrindus", "Sek medicinos naujienas"],
    "CHEMIJA, BIOTECHNOLOGIJOS": ["Atlik eksperimentus laboratorijoje", "Studijuok chemijos reakcijas", "Sek biotechnologijų startuolius", "Eksperimentuok su naujomis medžiagomis", "Skaityk mokslinius žurnalus"],
    "MATEMATIKA, KVANTINĖ FIZIKA": ["Sprėsk konkursinės užduotis", "Dalyvauk olimpiadose", "Studijuok pažangius vadovėlius", "Mokyk kitus – dėstymas gilina suvokimą", "Programuok matematikos modelius"],
    "DIRBTINIS INTELEKTAS, MAŠINŲ MOKYMAS": ["Mokykis programavimo bibliotekos (TensorFlow, PyTorch)", "Sprėsk Kaggle užduotis", "Dalyvauk AI hackathonuose", "Kurti savo projektus", "Sek AI mokslines publikacijas"],
    "FIZIKA, ELEKTRONIKA, KOMPIUTERIJA": ["Eksperimentuok su Arduino/Raspberry Pi", "Sprėsk fizikos uždavinius", "Sek technologijų naujienas", "Kurk mažus elektronikos projektus", "Išbandyk kompiuterių architektūros kursus"],
    "INŽINERIJA": ["Kurk prototipus", "Dalyvauk inžineriniuose projektuose", "Studijuok CAD įrankius", "Eksperimentuok su konstrukcijomis", "Dalyvauk studentų inžinerijos organizacijose"],
    "ELEKTROTECHNIKA": ["Studijuok elektros grandines", "Praktikuok su matavimo prietaisais", "Sek naujausias energetikos tendencijas", "Eksperimentuok su saulės baterijomis", "Kurk mažus elektros projektus"],
    "MECHANIKA": ["Ardyk ir surink variklius", "Mokykis mechanikos teorijos", "Eksperimentuok su konstrukcijų stiprumu", "Dalyvauk automobilių remonto dirbtuvėse", "Kurk 3D modelius"],
    "ARCHITEKTŪRA, MODELIAVIMAS": ["Studijuok architektūros istoriją", "Kurk 3D modelius", "Naudok AutoCAD/SketchUp", "Dalyvauk architektūriniuose konkursuose", "Sek tvariąją architektūrą"],
    "STATISTIKA, DUOMENYS": ["Analizuok duomenų rinkinius", "Mokykis R/Python analizės bibliotekos", "Dalyvauk Kaggle konkursuose", "Gilinkis į tikimybių teoriją", "Vizualizuok duomenis"],
    "FINANSAI, EKONOMIKA": ["Analizuok rinkas", "Sek ekonomikos naujienas", "Simuliuok investavimo scenarijus", "Studijuok įmonių finansus", "Kurk finansinius modelius"],
    "ĮSTATYMAI, TEISĖ": ["Skaityk teismo bylas", "Mokykis argumentavimo", "Sek teisės reformų naujienas", "Imituok teismo procesus su draugais", "Gilinkis į tarptautinę teisę"],
    "POLITIKA": ["Sek politinius procesus", "Diskutuok apie aktualijas", "Skaityk istorinius politinius veiksmus", "Analizuok partijų programas", "Būk aktyvus politinėse bendruomenėse"],
    "VALDŽIA, VALSTYBĖ": ["Analizuok istorinius valdymo modelius", "Sek politines naujienas", "Studijuok valdymo teorijas", "Būk aktyvus pilietinėse veiklose", "Rašyk politines analizes"],
    "RAŠTAS, SKAIČIAI": ["Rašyk kasdien", "Praktikuok loginį mąstymą per uždavinius", "Dalyvauk rašymo kursuose", "Kurk tinklaraštį", "Sprėsk kryžiažodžius"],
    "AMATAI, PREKYBA": ["Mokykis amato iš meistrų", "Praktikuok prekybos įgūdžius turguje", "Kurti rankdarbius", "Sek e. prekybos tendencijas", "Dalyvauk mugėse"],
    "BŪSTAS, STATYBA": ["Mokykis statybinių medžiagų savybių", "Stebėk meistrų darbą", "Eksperimentuok su mažais remontais", "Sek statybų naujienas", "Projektuok mažus namus"],
    "RELIGIJOS": ["Skaityk religinius tekstus", "Lygink skirtingas religijas", "Dalyvauk bendruomenės apeigose", "Diskutuok apie tikėjimo filosofiją", "Analizuok religijos poveikį istorijai"],
    "KELIONĖS, ATRADIMAI": ["Planuok keliones", "Skaityk kelionių tinklaraščius", "Studijuok geografiją", "Bendrauk su kitų šalių žmonėmis", "Dokumentuok savo atradimus"],
    "AGRESIJA, DOMINAVIMAS": ["Stebėk savo emocijas", "Mokykis konfliktų valdymo", "Praktikuok kovos menus", "Analizuok galios struktūras", "Gilinkis į psichologiją"],
    "FIZINĖ JĖGA": ["Praktikuok sporto treniruotes", "Mokykis fizinės sveikatos pagrindų", "Dalyvauk varžybose", "Sek mitybos režimą", "Konsultuokis su treneriu"],
    "MAISTAS": ["Domėkis mitybos mokslu", "Eksperimentuok su receptais", "Studijuok skirtingų kultūrų virtuvę", "Mokykis sveikos gyvensenos", "Rašyk receptų tinklaraštį"],
    "SEKSAS, VAIKAI": ["Domėkis šeimos psichologija", "Skaityk apie vaikų ugdymą", "Mokykis saugaus sekso pagrindų", "Diskutuok apie lyčių vaidmenis", "Stebėk vaikų raidos etapus"],
    "ŠILUMA, BUITIS": ["Mokykis buities darbų", "Eksperimentuok su interjero dizainu", "Tvarkyk buitį efektyviau", "Naudok ekologiškus sprendimus", "Sistemink namų užduotis"],
    "VALGIO RUOŠIMAS": ["Mokykis kulinarijos pagrindų", "Eksperimentuok su prieskoniais", "Studijuok maisto chemijos pagrindus", "Dalyvauk kulinarijos kursuose", "Sek virtuvės šefų technikas"],
    "GLOBA/RŪPYBA": ["Mokykis empatiškos komunikacijos", "Studijuok slaugos pagrindus", "Praktikuok kantrybę", "Dalyvauk savanoriškose veiklose", "Sek gerųjų praktikų naujienas"],
    "EMPATIJA": ["Praktikuok aktyvų klausymą", "Skaičiuk apie psichologiją", "Stebėk žmonių elgesį", "Dalyvauk grupės terapijose", "Mokykis konfliktų sprendimo"],
    "PUOŠYBA": ["Studijuok mados istoriją", "Eksperimentuok su stiliais", "Sek dizaino tendencijas", "Mokykis spalvų teorijos", "Dalyvauk mados kursuose"],
    "MUZIKA, ŠOKIS": ["Praktikuok instrumentą kasdien", "Studijuok muzikos teoriją", "Mokykis šokio technikos", "Dalyvauk ansambliuose", "Klausykis įvairių muzikos stilių"],
    "DRAMATIKA, GINČAI": ["Dalyvauk teatro grupėse", "Mokykis retorikos", "Praktikuok scenos kalbą", "Studijuok argumentavimo technikas", "Stebėk aktorių veiklą"],
    "LITERATŪRA": ["Skaityk klasikus", "Rašyk recenzijas", "Dalyvauk literatūros diskusijose", "Studijuok literatūros teoriją", "Kurk savo tekstus"],
    "MEDIA, DIZAINAS": ["Mokykis dizaino programų", "Studijuok tipografiją", "Praktikuok kompoziciją", "Sek dizaino tendencijas", "Kurk projektų portfelį"],
    "ISTORIJA, ŽURNALISTIKA": ["Skaityk pirminius šaltinius", "Rašyk straipsnius", "Praktikuok interviu technikas", "Studijuok žiniasklaidos etiką", "Sek naujienų analizę"]
}

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
                
                # Taškas (truputį sumažintas)
                fig.add_trace(go.Scatter(
                    x=[user_level * math.cos(theta_rad)], 
                    y=[user_level * math.sin(theta_rad)],
                    mode="markers", 
                    marker=dict(
                        color=level_colors.get(user_level, "#FFF"), 
                        size=12,  # Sumažinta nuo 16
                        line=dict(color="white", width=2)
                    ),
                    name=f"Tavo: {skill_name}",
                    hovertemplate=f"<b>TAVO ĮVERTINIMAS: {skill_name}</b><br>Kampas: {angle}°<br>Tavo lygis: {user_level}/10<br>Maksimalus: {max_level}/10<extra></extra>", 
                    showlegend=False
                ))

    # Koncentriniai apskritimai (papildyti iki 12)
    for r in range(1, 13):
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        x_circle = r * np.cos(theta_circle)
        y_circle = r * np.sin(theta_circle)
        
        # Dviems išoriniams apskritimams pakeista spalva į oranžinę
        circle_color = "orange" if r >= 11 else "gray"
        
        fig.add_trace(go.Scatter(
            x=x_circle, y=y_circle, 
            mode="lines", 
            line=dict(color=circle_color, width=0.5), 
            showlegend=False, 
            hoverinfo="skip"
        ))

    # Radialinės linijos kas 5 laipsniai - susiaurinta
    for angle in range(0, 360, 5):
        theta_rad = math.radians(90 - angle)
        x_line = [0, 12 * math.cos(theta_rad)]
        y_line = [0, 12 * math.sin(theta_rad)]
        fig.add_trace(go.Scatter(
            x=x_line, y=y_line, 
            mode="lines", 
            line=dict(color="gray", width=0.2),  # Sumažinta nuo 0.3
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
    st.sidebar.markdown("### ⬇️ Atsisiųsti duomenis")
    
    # HTML su visa Plotly diagrama
    try:
        html_str = fig.to_html(include_plotlyjs="cdn", full_html=True)
        st.sidebar.download_button(
            label="🖼️ HTML (diagrama + duomenys)", 
            data=html_str.encode("utf-8"), 
            file_name="hard_skills_diagrama.html", 
            mime="text/html"
        )
    except Exception as e:
        st.sidebar.error(f"Klaida generuojant HTML: {e}")
    
    # CSV su lentelės duomenimis
    try:
        skills = get_skills_data()
        rows = []
        for name, angle, max_level in skills:
            user_level = user_skills.get(name, 0)
            # Užtikriname, kad user_level yra int
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
        st.sidebar.download_button(
            label="📄 CSV (duomenys)", 
            data=csv, 
            file_name="hard_skills_data.csv", 
            mime="text/csv"
        )
    except Exception as e:
        st.sidebar.error(f"Klaida generuojant CSV: {e}")


def calculate_statistics(user_skills):
    """Apskaičiuoja statistikas apie vartotojo įgūdžius"""
    skills_data = get_skills_data()
    evaluated_skills = [skill for skill, level in user_skills.items() if level and level > 0]
    levels = [level for level in user_skills.values() if level and level > 0]
    total_skills_count = len(skills_data)
    evaluated_count = len(evaluated_skills)
    
    # Saugi statistikų apskaičiavimas
    max_skill_level = max(levels) if levels else 0
    min_skill_level = min(levels) if levels else 0
    avg_level = sum(levels) / evaluated_count if evaluated_count > 0 else 0
    median_level = np.median(levels) if levels else 0
    
    return {
        'evaluated_count': evaluated_count,
        'total_skills_count': total_skills_count,
        'max_skill_level': max_skill_level,
        'min_skill_level': min_skill_level,
        'avg_level': avg_level,
        'median_level': median_level,
        'evaluated_skills': evaluated_skills
    }


def main():
    st.title("🎯 Hard Skills Diagrama")
    
    # Pridėtas naujas tekstas su https linku
    st.markdown("""
    Pabandyk sąžiningai įsivertinti savo gebėjimus pagal unikalią sistemą, kuri daug aiškiau atskleis, kur esi ir kur nori nukeliauti, lavindamas savo kietuosius įgūdžius, susijusius su veikla ir profesija. Šitaip, žiūrėk, ir sėkmė greit nusišypsos.
    
    **Svarbiausias klausimas:** Kuri kryptis tau ar vaikui yra mėgiama ir kokio lygio tavo pažanga?
    
    Išvardintos 36 PROFESINĖS KRYPTYS. Apytiksliai. Pildyk tas, kurios atrodo svarbiausios ir taip kaip supranti. Arba įvertink visas, tuomet gausi daug detalesni ataskaitą ir tikslesnių patarimų.
    
    Čia pirmas etapas iš [https://sekmes.lt](https://sekmes.lt) projekto švietimo tema. Antras etapas bus vartotojų profiliai (jei prireiks) ir psichologiniai tipai, o trečias - DI agentas, kuris duos neįtikėtinai tikslių patarimų. Greit :)
    """)
    
    st.markdown("---")

    st.sidebar.header("🎯 Įvertink savo gebėjimus")
    st.sidebar.markdown("*Nustatyk savo lygį kiekvienai sričiai (0–maksimumas)*")
    skills_data = get_skills_data()

    # Inicializuojame session state
    if "user_skills" not in st.session_state:
        st.session_state.user_skills = {skill[0]: 0 for skill in skills_data}

    if "randomized_skills" not in st.session_state:
        st.session_state.randomized_skills = skills_data.copy()
        random.shuffle(st.session_state.randomized_skills)

    # Sidebar slideriai - kompaktiškesni
    st.sidebar.markdown("### 📊 Tavo įvertinimai:")
    user_skills = {}
    
    # Kompaktiškesnis dizainas su aiškiais maksimaliais lygiais
    for skill_name, angle, max_level in st.session_state.randomized_skills:
        current_value = st.session_state.user_skills.get(skill_name, 0)
        # Užtikriname, kad vertė neviršija maksimalaus lygio
        safe_value = min(current_value, max_level) if current_value else 0
        
        # Kompaktiškesnis pavadinimas su matomu maksimumu
        short_name = skill_name.replace(", ", "/").replace(" ", " ")
        if len(short_name) > 25:
            short_name = short_name[:22] + "..."
        
        user_level = st.sidebar.slider(
            f"{short_name} (max: {max_level})", 
            min_value=0, 
            max_value=max_level, 
            value=safe_value, 
            key=f"skill_{skill_name}",
            help=f"Pilnas pavadinimas: {skill_name}"
        )
        user_skills[skill_name] = user_level
        st.session_state.user_skills[skill_name] = user_level

    # Mygtukai
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔥 Išvalyti", use_container_width=True):
            for skill_name, _, _ in skills_data:
                st.session_state.user_skills[skill_name] = 0
            st.rerun()
    
    with col2:
        if st.button("🎲 Maišyti", use_container_width=True):
            st.session_state.randomized_skills = skills_data.copy()
            random.shuffle(st.session_state.randomized_skills)
            st.rerun()

    # Diagrama
    fig = create_circular_diagram(user_skills)
    st.plotly_chart(fig, use_container_width=True)
    
    # Eksporto mygtukai
    render_downloads(fig, user_skills)

    # Statistikos
    stats = calculate_statistics(user_skills)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Įvertinta sričių", f"{stats['evaluated_count']}/{stats['total_skills_count']}")
    with col2:
        skill_range = stats['max_skill_level'] - stats['min_skill_level']
        st.metric("Skirtumas max-min", f"{skill_range}")
    with col3:
        st.metric("Vidurkis", f"{stats['avg_level']:.1f}")
    with col4:
        st.metric("Medianinis lygis", f"{stats['median_level']:.1f}")

    # Sudėtingumo lygių paaiškinimas
    with st.expander("ℹ️ SUDĖTINGUMO LYGIŲ PAAIŠKINIMAS IR SPALVOS"):
        st.markdown("""
        **1–10 STIPRUMO (SUDĖTINGUMO) LYGIAI**

        - ⚫ **1 (Pilka)** – Kūdikiai (motorika, aplinkos suvokimas) / 3–5 m. vaikų lygis
        - 🟡 **2 (Geltona)** – 6–13 m. mokinių teorinės žinios, labiau nei praktiniai įgūdžiai
        - 🌸 **3 (Rožinė)** – 14–18 m. jaunimo lygis, stiprūs protiniai gebėjimai, silpnesnė praktika
        - 🟠 **4 (Oranžinė)** – Vidutinis lygis – paprasti darbai (Excel, Photoshop, blynų kepimas)
        - 🔴 **5 (Raudona)** – Mokyklos „devyntukai", vidutinio sudėtingumo lygis
        - 🟢 **6 (Salotinė)** – Automechaniko pameistrys, stiprus geimeris, pradedantis kūrėjas
        - 💚 **7 (Žalia)** – Studentų / jaunųjų profesionalų lygis (Middle developer)
        - 🔮 **8 (Indigo)** – Gyvenimo herojai, nacionalinio lygio senior specialistai
        - 🔵 **9 (Mėlyna)** – Aukščiausias meistiriškumas, tarptautinių projektų lygis
        - ⚪ **10 (Balta)** – Genijų lygis, pasaulinio masto inovatoriai
        """)

    # TOP įgūdžiai ir patarimai
    if stats['evaluated_skills']:
        top_5_skills = sorted(
            stats['evaluated_skills'], 
            key=lambda x: user_skills.get(x, 0), 
            reverse=True
        )[:5]
        
        # Silpniausios 5 sritys
        bottom_5_skills = sorted(
            stats['evaluated_skills'], 
            key=lambda x: user_skills.get(x, 0)
        )[:5]
        
        tab_top, tab_tips, tab_bottom = st.tabs(["🏆 5 stipriausios sritys", "💡 Kaip tobulėti", "🎯 5 silpniausios sritys"])
        
        with tab_top:
            for i, skill in enumerate(top_5_skills, 1):
                level = user_skills.get(skill, 0)
                max_level = next((s[2] for s in skills_data if s[0] == skill), 10)
                percentage = (level / max_level * 100) if max_level > 0 else 0
                st.write(f"**{i}.** {skill}: {level}/{max_level} ({percentage:.0f}%)")
        
        with tab_tips:
            st.markdown("#### Rekomenduojami žingsniai kiekvienai sričiai")
            for skill in top_5_skills:
                level = user_skills.get(skill, 0)
                st.markdown(f"**{skill}** – dabartinis lygis: **{level}**")
                tips = skill_tips.get(skill, ["Skirk daugiau laiko praktikai", "Ieškok mentoriaus", "Dalyvauk bendruomenės veiklose"])
                # Parodyti 5 patarimus, bet atsitiktinai parinkti, jei jų yra daugiau
                sample_tips = random.sample(tips, min(5, len(tips)))
                for tip in sample_tips:
                    st.write(f"• {tip}")
                st.markdown("---")

        with tab_bottom:
            st.markdown("#### 🎯 Sritys, kurioms reikia daugiau dėmesio")
            for i, skill in enumerate(bottom_5_skills, 1):
                level = user_skills.get(skill, 0)
                max_level = next((s[2] for s in skills_data if s[0] == skill), 10)
                percentage = (level / max_level * 100) if max_level > 0 else 0
                st.write(f"**{i}.** {skill}: {level}/{max_level} ({percentage:.0f}%)")
            
            st.markdown("#### 💡 Rekomendacijos tobulėjimui")
            for skill in bottom_5_skills:
                level = user_skills.get(skill, 0)
                st.markdown(f"**{skill}** – dabartinis lygis: **{level}**")
                tips = skill_tips.get(skill, ["Pradėk nuo pagrindų", "Rask pradedančiųjų kursus", "Praktikuok reguliariai"])
                # Parodyti 3-4 patarimus silpniausioms sritims
                sample_tips = random.sample(tips, min(4, len(tips)))
                for tip in sample_tips:
                    st.write(f"• {tip}")
                st.markdown("---")


if __name__ == "__main__":
    main()
