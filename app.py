# app_lunga_mappa_colonne.py
import base64, os
import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import folium_static
from folium.features import GeoJsonTooltip, GeoJsonPopup
from statistiche import analisi_diff_2012_2018, analisi_2018CLC, analisi_2012CLC
import matplotlib.pyplot as plt

st.set_page_config(page_title="Uso del Suolo Calabria", layout="wide")
st.title("Uso del Suolo - Reggio Calabria Dashboard")
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['font.size'] = 9

def load_and_simplify(path, tolerance=50): #zoom di tolleranza
    gdf = gpd.read_file(path).to_crs(3857)
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=tolerance)
    return gdf.to_crs(4326) #crs EU sud in metri

if "gdf_2012" not in st.session_state:
    st.session_state.gdf_2012 = load_and_simplify("data/Calabria_2012.geojson", tolerance=50)
if "gdf_2018" not in st.session_state:
    st.session_state.gdf_2018 = load_and_simplify("data/Calabria_2018.geojson", tolerance=50)
if "gdf_2012_2018" not in st.session_state:
    st.session_state.gdf_2012_2018 = load_and_simplify("data/change2012_2018.geojson", tolerance=50)

gdf_2012 = st.session_state.gdf_2012
gdf_2018 = st.session_state.gdf_2018
gdf_2012_2018 = st.session_state.gdf_2012_2018

anno_selezionato = st.sidebar.selectbox(
    "Seleziona anno",
    options=["2012", "2018", "2012-2018", "2024 (coming soon)"],
    index=1
)

mostra_2012 = anno_selezionato == "2012"
mostra_2018 = anno_selezionato == "2018"
mostra_2012_2018 = anno_selezionato == "2012-2018"
alert_coming = anno_selezionato == "2024 (coming soon)"

if mostra_2012:
    with st.sidebar.expander("Tabella 2012", expanded=True):
        st.dataframe(gdf_2012.drop(columns="geometry"))
elif mostra_2018:
    with st.sidebar.expander("Tabella 2018", expanded=True):
        st.dataframe(gdf_2018.drop(columns="geometry"))
elif mostra_2012_2018:
    with st.sidebar.expander("Tabella 2012-2018", expanded=True):
        st.dataframe(gdf_2012_2018.drop(columns="geometry"))
elif alert_coming:
    st.sidebar.info("I dati per il 2024 non sono ancora disponibili!")

# --- LAYOUT A DUE COLONNE ---
col1, col2 = st.columns([1.2, 1])

with col1:
    # --- MAPPA FOLIUM ---
    st.subheader("Mappa Interattiva")

    m = folium.Map(location=[38.1105, 15.6613], zoom_start=8)

    def add_geojson_layer(gdf, name, color):
        folium.GeoJson(
            gdf,
            name=name,
            style_function=lambda feat: {
                'fillColor': color,
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.4
            },
            tooltip=GeoJsonTooltip(fields=gdf.drop(columns="geometry").columns.tolist()),
            popup=GeoJsonPopup(fields=gdf.drop(columns="geometry").columns.tolist())
        ).add_to(m)

    if mostra_2012: add_geojson_layer(gdf_2012, "Uso Suolo 2012", "orange")
    if mostra_2018: add_geojson_layer(gdf_2018, "Uso Suolo 2018", "green")
    if mostra_2012_2018: add_geojson_layer(gdf_2012_2018, "Cambiamenti Uso del Suolo", "purple")
    if alert_coming:
        folium.CircleMarker(location=[38.1105, 15.6613], radius=30, color="blue",
                            fill=True, fill_opacity=0.2, popup="Sto arrivando!").add_to(m)

    folium.LayerControl().add_to(m)

    # mappa leggermente più lunga per arrivare ai pie
    folium_static(m, width=900, height=950)

with col2:
    # --- Grafici accanto alla mappa ---
    st.subheader("Analisi e Grafici")
    if mostra_2012:
        analisi_2012CLC(gdf_2012)
    if mostra_2018:
        analisi_2018CLC(gdf_2018)
    if mostra_2012_2018:
        analisi_diff_2012_2018(gdf_2012_2018)

# SEZIONE DESCRIZIONE
st.markdown("---")
st.subheader("Analisi e descrizione")
st.markdown(""" In questa sezione vengono illustrate le analisi relative ai dati CLC 2012 e 2018, 
incluse le distribuzioni delle classi di copertura del suolo, le macro-categorie 
e le principali transizioni avvenute nel periodo considerato. """)
img_dir = "data/img/"
img_width = 700  # larghezza fissa per tutte le immagini
img_height = 700
# Testo orizzontale da mettere sopra ogni immagine
#horizontal_text = "---"

# Lista immagini + testi affiancati
images_texts = [
    ("barplotclc.png", 
     "Le 10 transizioni più rilevanti.",  # caption breve
     """
     Il grafico confronta la composizione percentuale tra 2012 (viola) e 2018 (verde). Le categorie dominanti sono:

Broad-leaved forest (boschi a foglia larga): ~24%, stabile
Olive groves (oliveti): ~17%, stabile
Le altre categorie mostrano variazioni minime, indicando una generale stabilità del territorio"""),

    ("cambiamento 20 suoli.png", 
     "Top 20 cambiamenti",
     """Questa figura evidenzia i 20 cambiamenti più significativi di uso del suolo, offrendo un focus sulle trasformazioni maggiormente rilevanti.
     La sovrapposizione quasi perfetta delle barre indica una sostanziale 
        stabilità del territorio reggino. Le foreste aspromontane e gli oliveti 
        rappresentano la caratteristica identitaria del paesaggio calabrese"""),
    
    ("caambaimenticlassi.png", 
     "Evoluzioni del suolo tra il 2012 e il 2018",
     """Il barplot orizzontale indica il tipo di transizione che è avvenuta per i 10 suoli più cambiati tra l'anno 2012 e l'anno 2018, il piechart mostra invece la percentuale cambiata di ognuna delle transizioni avvenute."""),

    ("classiOriginali_2012.png", 
     "Classi del 2012 destinate a cambiare",
     """Le classi mostrate qui indicano quali aree, partendo dal 2012, hanno subito modifiche di destinazione d’uso entro il 2018."""),

    ("classiOriginali_2018.png", 
     "Classi risultanti al 2018",
     """In questa immagine sono mostrate le classi finali di destinazione delle aree cambiate, fornendo una panoramica su come il paesaggio si è riconfigurato."""),

    ("Heatmap.png", 
     "Heatmap dei cambiamenti",
     """Questa matrice mostra i flussi di trasformazione tra le classi di copertura del suolo più dinamiche tra 2012 e 2018. Lettura: righe = classi di origine (2012), colonne = classi di destinazione (2018).Transizioni più significative (valori in ettari):• Mineral extraction → Mineral extraction (17.7 ha - rosso scuro)
Le aree estrattive rimangono stabili, confermando l'attività mineraria continua (probabilmente cave di aggregati) nel territorio reggino, senza dismissione o riconversione.• Construction site → Land without current use (16.7 ha - rosso scuro)
Fenomeno critico: cantieri edili del 2012 che sei anni dopo risultano terreni abbandonati senza uso. Questo rappresenta il problema delle opere incompiute tipico del Sud Italia - investimenti non completati che diventano aree degradate.• Forests → Construction site (16.0 ha - rosso scuro)
Disboscamento per urbanizzazione: foreste di latifoglie (probabilmente sulle pendici dell'Aspromonte) convertite in cantieri. Indica pressione edilizia sulle aree boschive periurbane.• Arable land → Construction site (11.1 ha - arancione)
Consumo di suolo agricolo: seminativi trasformati in aree edificabili. Fenomeno di sprawl urbano che sottrae terreno produttivo all'agricoltura.• Pastures → Industrial, commercial units (9.6 ha - arancione)
Pascoli convertiti in aree produttive/commerciali. Espansione delle zone industriali/artigianali nell'hinterland reggino.• Herbaceous vegetation → Construction site (9.0 ha - arancione)
Vegetazione erbacea (incolti, aree marginali) urbanizzata, indicando espansione edilizia su terreni non coltivati.• Land without current use → Industrial units (8.1 ha - arancione)
Riqualificazione positiva: aree dismesse che diventano zone produttive, recupero di terreni degradati.• Construction site → Industrial units (6.5 ha - giallo)
Cantieri che si completano diventando strutture produttive funzionali.La diagonale quasi vuota indica che la maggior parte delle aree non cambia categoria - i cambiamenti sono concentrati in poche transizioni specifiche.""")
]

# Mostra immagini con caption + testo lungo sotto l’immagine
# Mostra immagini centrali con testo sotto
for img_name, caption, long_text in images_texts:
    if os.path.exists(img_dir + img_name):
        st.markdown("---")

        # Codifica immagine base64
        with open(img_dir + img_name, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()

        # HTML immagine centrata e più grande
        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:20px;">
                <img src="data:image/png;base64,{img_base64}" 
                     style="width:{img_width}px; border:1px solid #ccc; border-radius:8px;"
                     alt="{caption}">
            </div>
            <div style="margin-bottom:40px;">
                <p style="text-align:center;"><strong>{caption}</strong></p>
                <p style="text-align:justify;">{long_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

#st.markdown(horizontal_text)

