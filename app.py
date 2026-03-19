import io
import pandas as pd
import streamlit as st

# =========================
# LOGIN
# =========================
USERNAME = "user RECAP"
PASSWORD = "Recap26@"


def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.title("🔐 Login")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Accedi"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenziali non valide")

    return False


if not check_login():
    st.stop()

# =========================
# APP
# =========================
st.title("📊 Elaboratore Excel Esiti")

uploaded_file = st.file_uploader("Carica file Excel", type=["xlsx", "xls"])

if uploaded_file:

    df = pd.read_excel(uploaded_file, dtype=str)

    telefono = df.iloc[:, 20]   # U
    esito_ae = df.iloc[:, 30]   # AE
    esito_af = df.iloc[:, 31]   # AF
    codice = df.iloc[:, 33]     # AH

    result = {}

    for t, ae, af, c in zip(telefono, esito_ae, esito_af, codice):

        if pd.isna(c):
            continue

        # scegli AE o AF
        esito = ae if pd.notna(ae) and str(ae).strip() != "" else af

        if pd.isna(esito):
            continue

        esito = str(esito).strip()

        # trasformazioni
        if esito == "Operatore non disponibile":
            esito = "Occupato"

        if esito in ["Nuovo", "Errore Operatore"]:
            esito = "Nessuna risposta"

        # esclusioni
        if esito in ["Lavorato", "In Conversazione"]:
            continue

        telefono_str = "" if pd.isna(t) else str(t).strip()

        pair = f"{telefono_str} {esito}".strip()

        if c not in result:
            result[c] = []

        result[c].append(pair)

    # crea output
    out = []
    for k, v in result.items():
        out.append([k, "-".join(v)])

    result_df = pd.DataFrame(out, columns=["Codice", "Esiti"])

    st.dataframe(result_df)

    # download
    buffer = io.BytesIO()
    result_df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        "⬇️ Scarica file",
        buffer,
        "output.xlsx"
    )