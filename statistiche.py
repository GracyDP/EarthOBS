import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# legenda ufficiale CLC (estratto)
CLC_LEGEND = {
    111: "Tessuto urbano continuo",
    112: "Tessuto urbano discontinuo",
    121: "Zone industriali/commerciali",
    122: "Reti stradali/ferroviarie",
    123: "Porti",
    124: "Aeroporti",
    131: "Cave e cantieri",
    132: "Discariche",
    141: "Spazi verdi urbani",
    142: "Impianti sportivi/ricreativi",
    211: "Seminativi asciutti",
    212: "Seminativi irrigui",
    213: "Risaie",
    221: "Vigneti",
    222: "Frutteti/piantagioni",
    223: "Oliveti",
    231: "Prati stabili",
    241: "Colture miste",
    242: "Sistemi colturali complessi",
    243: "Agricoltura + vegetazione naturale",
    244: "Aree agro-forestali",
    311: "Boschi latifoglie",
    312: "Boschi conifere",
    313: "Boschi misti",
    321: "Praterie naturali",
    322: "Brughiere e macchia",
    323: "Vegetazione sclerofilla",
    324: "Transizione bosco-pascolo",
    331: "Spiagge/dune",
    332: "Rocce nude",
    333: "Vegetazione rada",
    334: "Aree bruciate",
    511: "Corsi d’acqua",
    512: "Bacini d’acqua",
}


# ---------- Funzioni di supporto ----------
def autopct_func(pct):
    """Mostra percentuale solo se >5%"""
    return ('%.1f%%' % pct) if pct > 5 else ''


def get_colors(n):
    """
    Restituisce n colori distinti combinando due colormap ('tab20' + 'tab20b'),
    arrivando fino a 40 colori unici.
    """
    base_cmap1 = cm.get_cmap('tab20', 20)
    base_cmap2 = cm.get_cmap('tab20b', 20)
    colors = [base_cmap1(i) for i in range(20)] + [base_cmap2(i) for i in range(20)]
    return colors[:n]


def style_legend(ax, wedges, legend_labels, title):
    """Applica stile leggibile alla legenda"""
    leg = ax.legend(
        wedges,
        legend_labels,
        title=title,
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        frameon=True,
    )
    leg.get_frame().set_facecolor("#333333")
    leg.get_frame().set_alpha(0.7)
    for text in leg.get_texts():
        text.set_color("white")
    return leg


# ---------- Analisi CLC 2018 ----------
def analisi_2018CLC(gdf_2018):
    st.markdown("### Distribuzione codici CLC 2018")

    col_name = "Classe_LandCover"
    if col_name not in gdf_2018.columns:
        st.warning(f"Il dataset non contiene la colonna '{col_name}'")
        return

    counts = gdf_2018[col_name].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    colors = get_colors(len(counts))

    wedges, texts, autotexts = ax.pie(
        counts,
        startangle=90,
        autopct=autopct_func,
        colors=colors,
        pctdistance=0.8
    )
    ax.set_title("Copertura del suolo (CLC 2018)", color="white")
    ax.set_ylabel("")

    total = counts.sum()
    legend_labels = [
        f"{CLC_LEGEND.get(idx, idx)} ({val/total*100:.1f}%)"
        for idx, val in zip(counts.index, counts)
    ]
    style_legend(ax, wedges, legend_labels, "Classe")
    st.pyplot(fig)

    # --- Macro-categorie (urbano vs naturale/altro)
    st.markdown("### Macro-categorie semplificate (2018)")
    urban_codes = ["11100", "11200", "12100", "12200", "12300", "12400", "13100", "13200", "14100", "14200"]
    gdf_2018["macro"] = gdf_2018[col_name].apply(
        lambda x: "Urban/Industrial" if str(x) in urban_codes else "Natural/Other"
    )
    macro_counts = gdf_2018["macro"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    fig2.patch.set_alpha(0)
    ax2.set_facecolor("none")
    colors = get_colors(len(macro_counts))

    wedges, _, _ = ax2.pie(
        macro_counts,
        startangle=90,
        autopct=autopct_func,
        colors=colors,
        pctdistance=0.8
    )
    ax2.set_title("Urban/Industrial vs Natural/Other (2018)", color="white")
    legend_labels = [
        f"{idx}: {val/macro_counts.sum()*100:.1f}%" for idx, val in zip(macro_counts.index, macro_counts)
    ]
    style_legend(ax2, wedges, legend_labels, "Macro")
    st.pyplot(fig2)


# ---------- Analisi CLC 2012 ----------
def analisi_2012CLC(gdf_2012):
    st.markdown("### Distribuzione codici CLC 2012")

    col_name = "clc"
    col_area = "area"
    if col_name not in gdf_2012.columns:
        st.warning(f"Il dataset non contiene la colonna '{col_name}'")
        return

    counts = gdf_2012.groupby(col_name)[col_area].sum()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    colors = get_colors(len(counts))

    wedges, _, _ = ax.pie(
        counts,
        startangle=90,
        autopct=autopct_func,
        colors=colors,
        pctdistance=0.8
    )
    ax.set_title("Copertura del suolo (CLC 2012)", color="white")
    legend_labels = [
        f"{CLC_LEGEND.get(idx, idx)} ({val/counts.sum()*100:.1f}%)"
        for idx, val in zip(counts.index, counts)
    ]
    style_legend(ax, wedges, legend_labels, "Classe CLC12")
    st.pyplot(fig)

    # --- Macro-categorie
    st.markdown("### Macro-categorie semplificate (2012)")

    def macro_class(code):
        code = int(code)
        if code in [111, 112, 121, 122, 123, 124, 131, 132, 141, 142]:
            return "Urban/Industrial"
        elif 200 <= code < 300:
            return "Agricoltura"
        elif 300 <= code < 400:
            return "Foreste/Vegetazione"
        else:
            return "Altro"

    gdf_2012["macro"] = gdf_2012[col_name].apply(macro_class)
    macro_counts = gdf_2012.groupby("macro")[col_area].sum()

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    fig2.patch.set_alpha(0)
    ax2.set_facecolor("none")
    colors = get_colors(len(macro_counts))

    wedges, _, _ = ax2.pie(
        macro_counts,
        startangle=90,
        autopct=autopct_func,
        colors=colors,
        pctdistance=0.8
    )
    ax2.set_title("Urban/Agricoltura vs Foreste/Vegetazione (2012)", color="white")
    legend_labels = [
        f"{idx}: {val/macro_counts.sum()*100:.1f}%" for idx, val in zip(macro_counts.index, macro_counts)
    ]
    style_legend(ax2, wedges, legend_labels, "Macro")
    st.pyplot(fig2)


# ---------- Analisi differenze 2012–2018 ----------
def analisi_diff_2012_2018(gdf_diff):
    st.markdown("### Differenze 2012–2018")

    required_cols = {"campo2012P", "code_2018", "AREA"}
    if not required_cols.issubset(gdf_diff.columns):
        st.warning(f"Il dataset deve contenere le colonne {required_cols}")
        return

    gdf_diff = gdf_diff[gdf_diff["campo2012P"] != gdf_diff["code_2018"]]
    if gdf_diff.empty:
        st.info("Nessuna area risulta cambiata tra 2012 e 2018.")
        return

    transizioni = gdf_diff.groupby(["campo2012P", "code_2018"])["AREA"].sum().sort_values(ascending=False)
    totale = transizioni.sum()

    # --- Pie delle transizioni
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    colors = get_colors(len(transizioni))

    wedges, _, _ = ax.pie(
        transizioni,
        startangle=90,
        autopct=lambda pct: ('%.1f%%' % pct) if pct > 3 else '',
        colors=colors
    )
    ax.set_title("Transizioni di uso del suolo (2012 → 2018)", color="white")
    legend_labels = [
        f"{CLC_LEGEND.get(src, src)} → {CLC_LEGEND.get(dst, dst)} ({val/totale*100:.1f}%)"
        for (src, dst), val in transizioni.items()
    ]
    style_legend(ax, wedges, legend_labels, "Transizioni")
    st.pyplot(fig)

    # --- Barplot Top 10 transizioni
    st.markdown("### Top 10 transizioni per superficie")
    top10 = transizioni.head(10)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    top10.plot(kind="barh", ax=ax2, color="purple")
    ax2.set_xlabel("Superficie (unità)")
    ax2.set_ylabel("Transizione")
    ax2.set_title("Top 10 transizioni (2012 → 2018)")
    ax2.invert_yaxis()
    ax2.set_yticklabels([
        f"{CLC_LEGEND.get(src, src)} → {CLC_LEGEND.get(dst, dst)}"
        for (src, dst) in top10.index
    ])
    st.pyplot(fig2)
