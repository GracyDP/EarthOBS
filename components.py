# components.py
import os
import base64
import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        /* Nasconde sidebar e menu */
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        button[kind="header"] {display: none;}

        /* Riduce spazio sopra ma NON nasconde toolbar (serve per Rerun/Settings) */
        .block-container { padding-top: 0.35rem !important; }
        header[data-testid="stHeader"] { height: auto !important; }
        div[data-testid="stToolbar"] { visibility: visible !important; height: auto !important; }

        /* Navbar style */
        .nav-wrap {
            position: sticky;
            top: 0;
            z-index: 9999;
            background: rgba(15, 18, 25, 0.96);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid rgba(255,255,255,0.10);
            padding: 0.35rem 0.75rem;
            border-radius: 0px;
            margin: 0 0 0.6rem 0;
        }

        .nav-link a{
            text-decoration: none;
            font-weight: 700;
            letter-spacing: 0.08em;
            font-size: 0.95rem;
            color: white;
        }
        .nav-link a:hover{ text-decoration: underline; }

        /* Selectbox label stile */
        div[data-testid="stSelectbox"] label {
            font-weight: 800 !important;
            letter-spacing: 0.08em;
        }

        /* Allinea verticalmente meglio link su alcune versioni */
        .nav-pad { padding-top: 1.9rem; text-align:center; }

        /* Personalizzare l'hover delle righe nella tabella/statistiche */
        .stDataFrame tbody tr:hover {
            background-color: #f0f0f0 !important;  /* Colore di sfondo quando si passa sopra una riga */
        }

        .stDataFrame tbody tr:nth-child(even):hover {
            background-color: #e6e6e6 !important;  /* Colore alternato per righe pari */
        }

        .stDataFrame tbody tr:hover td {
            color: #000 !important;  /* Cambia il colore del testo al passaggio del mouse */
        }

        /* Personalizzare l'hover sui link nella pagina */
        .stMarkdown a:hover {
            color: #0056b3 !important;  /* Colore del link durante hover ***** */ 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def _render_clickable_logo(logo_path: str, href: str = "/") -> None:
    """Logo cliccabile che riporta a href (di default home '/')."""
    if not os.path.exists(logo_path):
        st.warning(f"Logo non trovato: {logo_path}")
        return

    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")

    st.markdown(
        f"""
        <a href="{href}" target="_self" style="display:inline-block;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="height:55px; width:auto; cursor:pointer;">
        </a>
        """,
        unsafe_allow_html=True,
    )


def render_navbar(
    *,
    default_year: str = "2018",
    year_options=None,
    logo_primary: str = "data/LogoLabGis.png",
    logo_fallback: str = "LogoLabGis.png",
    home_href: str = "/",
    info_href: str = "Info",  
    gallery_href: str = "Galleria",  
) -> str:
    """
    Navbar (LOGO | ANNO | INFO | GALLERIA).
    Ritorna l'anno selezionato.
    Salva la scelta in session_state per mantenerla tra pagine.
    """
    if year_options is None:
        year_options = ["2012", "2018", "2012-2018", "2024"]

    if "anno_selezionato" not in st.session_state:
        st.session_state.anno_selezionato = default_year

    with st.container():
        st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)

        nav_logo, nav_year, nav_info, nav_gallery = st.columns(
            [2.6, 2.2, 1.2, 1.4], vertical_alignment="center"
        )

        with nav_logo:
            logo_path = logo_primary if os.path.exists(logo_primary) else logo_fallback
            _render_clickable_logo(logo_path, href=home_href)

        with nav_year:
            idx = year_options.index(st.session_state.anno_selezionato) if st.session_state.anno_selezionato in year_options else 1
            st.session_state.anno_selezionato = st.selectbox(
                "ANNO",
                options=year_options,
                index=idx,
            )

        with nav_info:
            #  link con st.markdown() per navigare 
            st.markdown(
                f"""
                <div class="nav-link nav-pad">
                  <a href="/{info_href}" target="_self">INFO</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with nav_gallery:
           # il link con st.markdown() per navigare correttamente
            st.markdown(
                f"""
                <div class="nav-link nav-pad">
                  <a href="/{gallery_href}" target="_self">GALLERIA</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    return st.session_state.anno_selezionato


def render_footer(text: str = "© 2026 — LabGis UNISA | Progetto HeartBOS") -> None:
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center; padding: 16px 0; opacity: 0.85;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
