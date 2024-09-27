import streamlit as st
import streamlit_survey as ss
import streamlit_scrollable_textbox as stx
import time

import json
import pandas as pd
from sqlalchemy import create_engine, text

import pymysql
import sqlalchemy
import os
import pymysql
from sshtunnel import SSHTunnelForwarder
from fabric import Connection
from sqlalchemy.exc import SQLAlchemyError


##set config
# Set the page config at the top of the file
st.set_page_config(
    page_title="Aligniverse",
    page_icon="🌍",
    initial_sidebar_state="collapsed"  # Collapsed sidebar by default
)


# Initialize session state for sidebar state if not already set
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# Function to collapse the sidebar
def collapse_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {
                display: none;
            }
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply the sidebar collapse dynamically based on session state
if st.session_state.sidebar_state == 'collapsed':
    collapse_sidebar()

##start survey
survey = ss.StreamlitSurvey("Survey Aligniverse")

st.title("Willkommen bei Aligniverse")
    
text1 = "Hi, schön dich zu sehen! Aligniverse ist ein Forschungsprojekt mit der Mission, große Sprachmodelle (LLMs) so auszurichten, dass sie Positivität fördern und Diskriminierung gegenüber Minderheitengruppen reduzieren."
st.write(text1)

text2 = "LLMs sind fortschrittliche Computerprogramme, die darauf ausgelegt sind, menschenähnlichen Text basierend auf den Daten, auf denen sie trainiert wurden, zu verstehen und zu generieren. Ausrichtung bezieht sich auf den Prozess, sicherzustellen, dass sich diese Modelle in einer Weise verhalten, die mit menschlichen Werten und ethischen Prinzipien übereinstimmt. In diesem Zusammenhang benötigen wir Ihre Hilfe - wie können wir LLMs dazu bringen, kontroverse Fragen angemessen zu beantworten?"
st.write(text2)

text3 = "Nimm an unserer Studie teil, um LLM-generierte Texte zu sensiblen Themen zu überprüfen und zu bewerten. Wir werden die gesammelten Bewertungen als Ausrichtungsdatensatz für die Gemeinschaft veröffentlichen."
st.write(text3)

text4 = "Die Teilnahme dauert in der Regel zwischen 10 und 30 Minuten. Du kannst so viele Texte bewerten, wie du möchtest. Wir schätzen deine Bereitschaft, einen Beitrag zu leisten."
st.write(text4)

st.divider()

st.subheader("Teilnehmerinformation und Einverständniserklärung")
st.write("Wir verpflichten uns, deine Privatsphäre zu schützen. Bitte lies die Studienbedingungen sorgfältig durch.")
if st.button("Überprüfung der allgemeinen Informationen und der Einverständniserklärung"):

    content = """**Teilnehmerinformationen und Einwilligungserklärung für Aligniverse** 
    Liebe Teilnehmerinnen und Teilnehmer, wir laden euch ein, an unserer Forschungsstudie teilzunehmen. Alle relevanten Informationen findet ihr im Teilnehmerinformationsblatt unten. Bitte lest es sorgfältig durch, und wir stehen euch für alle Fragen zur Verfügung.
    Unser Ziel ist es, etwa 10.000 Teilnehmer an mehr als fünf Standorten zu rekrutieren. An der Technischen Universität München (TUM) beabsichtigen wir, etwa 1.000 Teilnehmer zu rekrutieren. Die Studie wurde von der TUM geplant und wird in Zusammenarbeit mit der Eidgenössischen Technischen Hochschule (ETH) durchgeführt, mit Finanzierung durch unser Institut. 
    Die Teilnahme an der Studie ist freiwillig. Wenn du nicht teilnehmen möchtest oder später deine Einwilligung widerrufst, entstehen dir keine Nachteile.
    
    **Warum führen wir diese Studie durch?**
    Unsere Mission besteht darin, Daten zu sammeln, um große Sprachmodelle (LLMs) so auszurichten, dass sie Positivität fördern und Diskriminierung, insbesondere gegenüber Minderheitengruppen, reduzieren. 
    In diesem Zusammenhang sind wir an deiner Meinung interessiert. Wie stellst du dir vor, dass ein LLM auf sensible Fragen antwortet?
    Im Verlauf der Studie wirst du verschiedene Texte, die von großen Sprachmodellen (LLMs) zu sensiblen Themen erstellt wurden, überprüfen. Deine Aufgabe wird es sein, diese Texte nach verschiedenen Kriterien zu bewerten. 
    Wir werden diese Bewertungen als Ausrichtungsdatensatz veröffentlichen und mit der Gemeinschaft teilen. Dieser Datensatz kann von Praktikern genutzt werden, um die Ausrichtung von LLMs zu verbessern.
    
    **Wie läuft die Studie ab?**
    Die Teilnahme dauert in der Regel zwischen 10 und 30 Minuten. Das Bewerten eines vorgefertigten Textes dauert etwa 10 Minuten. Du kannst so viele Texte bewerten, wie du möchtest, und wir schätzen deine Bereitschaft, einen Beitrag zu leisten.
    
    **Gibt es persönliche Vorteile durch die Teilnahme an dieser Studie?**
    Du wirst keinen persönlichen Nutzen aus der Teilnahme an dieser Studie ziehen. Die Ergebnisse der Studie könnten jedoch anderen Menschen in der Zukunft helfen.
    Welche Risiken sind mit der Teilnahme an der Studie verbunden?
    Die angezeigten Texte können Stereotype und Diskriminierung enthalten, die negative Gefühle bei dir auslösen können. Bei Fragen und Anregungen zu den Texten kannst du dich jederzeit an uns wenden unter der E-Mail-Adresse mwieland@ethz.ch. 
    In Notfällen wende dich bitte an die folgenden Organisationen:
    (1) Deutschland: Telefonseelsorge unter +49 800 111 0 111
    (2) Schweiz: Dargebotene Hand unter +41 143

    **WWen kann ich kontaktieren, wenn ich weitere Fragen habe?**
    Wenn du weitere Fragen hast, kontaktiere bitte: Michèle Wieland, mwieland@ethz.ch
    
    **Informationen zum Datenschutz**
    In dieser Studie ist Orestis Papakyriakopoulos für die Datenverarbeitung verantwortlich. Die rechtliche Grundlage für die Verarbeitung ist die persönliche Einwilligung (Art. 6 Abs. 1 lit. a, Art. 9 Abs. 2 lit. a DSGVO). Die Daten werden stets vertraulich behandelt. Die Daten werden ausschließlich zu dem oben beschriebenen Zweck der Studie erhoben und nur in diesem Rahmen verwendet. Wir erheben keine persönlichen Daten. Wir erheben jedoch zusätzliche sensible personenbezogene Daten. 
    Dazu gehören Alter, Geschlechtsidentifikation, Aufenthaltsland, Abstammung und ethnische Zugehörigkeit. Alle Daten werden anonym erhoben. Dies bedeutet, dass niemand, einschließlich der Studienleiter, feststellen kann, wem die Daten gehören. Die Daten werden auf einem Server der TUM gespeichert. Wir übertragen deine Daten nicht an andere Institutionen in Deutschland, der EU oder an ein Drittland außerhalb der EU, noch an eine internationale Organisation. Die Forschungsdaten können für wissenschaftliche Publikationen verwendet und/oder anderen Forschern in wissenschaftlichen Datenbanken auf unbestimmte Zeit zur Verfügung gestellt werden. Die Daten werden in einer Form verwendet, die keine Rückschlüsse auf die einzelnen Studienteilnehmer zulässt (anonymisiert).
    
    Die Einwilligung zur Verarbeitung deiner Daten erfolgt freiwillig. Du kannst deine Einwilligung jederzeit ohne Angabe von Gründen und ohne Nachteile für dich widerrufen. Nach dem Widerruf werden keine weiteren Daten erhoben. 
    Die Rechtmäßigkeit der aufgrund der Einwilligung bis zum Widerruf erfolgten Verarbeitung bleibt unberührt. Du hast das Recht, Auskunft über die Daten, einschließlich einer kostenlosen Kopie, zu erhalten. Darüber hinaus kannst du die Berichtigung, Sperrung, Einschränkung der Verarbeitung oder Löschung der Daten sowie gegebenenfalls die Übertragung der Daten verlangen. In diesen Fällen wende dich bitte an: Prof. Dr. Orestis Papakyriakopoulos, orestis.p(at)tum.de. Nach der Anonymisierung können die Daten jedoch keiner Person mehr zugeordnet werden. Sobald die Anonymisierung erfolgt ist, ist der Zugriff auf die Daten, deren Sperrung oder Löschung nicht mehr möglich. Bei Fragen zur Datenverarbeitung und Einhaltung der Datenschutzvorschriften steht dir der folgende Datenschutzbeauftragte zur Verfügung:
    Offizieller Datenschutzbeauftragter der Technischen Universität München
    Post Adresse: Arcisstr. 21, 80333 München
    Telefon: 089/289-17052
    E-Mail: beauftragter@datenschutz.tum.de
    Du hast auch das Recht, dich bei einer Datenschutzaufsichtsbehörde zu beschweren. Eine Liste der Aufsichtsbehörden in Deutschland findest du unter: https://www.bfdi.bund.de/DE/Infothek/Anschriften_Links/anschriften_links-node.html
    """
    stx.scrollableTextbox(content, height = 150)

## include consent questions plus information about contact
st.subheader("Einwilligungserklärung")
st.write("Ich wurde vom Studienteam über die Studie informiert. Ich habe die schriftliche Teilnehmerinformation und Einwilligungserklärung für die oben genannte Studie erhalten und gelesen. Ich wurde umfassend über den Zweck und den Ablauf der Studie, die Chancen und Risiken der Teilnahme sowie über meine Rechte und Pflichten aufgeklärt. Meine Zustimmung zur Teilnahme an der Studie erfolgt freiwillig. Ich habe das Recht, meine Zustimmung jederzeit ohne Angabe von Gründen zu widerrufen, ohne dass mir dadurch Nachteile entstehen.")
consent1 = survey.checkbox("Ich erkläre mich hiermit bereit, an der Studie teilzunehmen.")
st.write("Die Verarbeitung und Nutzung personenbezogener Daten für die oben genannte Studie erfolgt ausschliesslich wie in den Studieninformationen beschrieben. Die erhobenen und verarbeiteten personenbezogenen Daten umfassen insbesondere die ethnische Herkunft.")
consent2 = survey.checkbox("Ich erkläre mich mit der beschriebenen Verarbeitung meiner personenbezogenen Daten einverstanden.")
consent3 = survey.checkbox("Ich bestätige, dass ich mindestens 18 Jahre alt bin.")

# SSH and Database credentials
ssh_host = st.secrets["ssh_host"]
ssh_port = st.secrets["ssh_port"]
ssh_user = st.secrets["ssh_user"]
ssh_password = st.secrets["ssh_password"]

db_host = st.secrets["db_host"]
db_user = st.secrets["db_user"]
db_password = st.secrets["db_password"]
db_name = st.secrets["db_name"]
db_port = st.secrets["db_port"]

### Set up SSH connection and port forwarding
### Set up SSH tunnel with keep-alive
def start_ssh_tunnel():
    try:
        tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_host, db_port),
            set_keepalive=30  # Send keep-alive packets every 60 seconds to keep connection alive
        )
        tunnel.start()
        return tunnel
    except Exception as e:
        st.error(f"SSH tunnel connection failed: {e}")
        raise  

# Establish Database connection with retry logic and optimized timeouts
def get_connection(tunnel, retries=3, delay=5):
    for attempt in range(retries):
        try:
            conn = pymysql.connect(
                host='127.0.0.1',
                user=db_user,
                password=db_password,
                database=db_name,
                port=tunnel.local_bind_port,
                connect_timeout=20600,  # Increased 
                read_timeout=10600,     # Increased
                write_timeout=10600,    # Increased 
                max_allowed_packet=128 * 1024 * 1024  # 128MB
            )
            return conn
        except pymysql.err.OperationalError as e:
            st.error(f"Connection attempt {attempt + 1} failed: {e}")
            if "MySQL server has gone away" in str(e):
                # Specific handling for the lost connection error
                st.error("MySQL server has gone away. Trying to reconnect...")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                st.error("Failed to connect to the database after multiple retries.")
                raise

# SQLAlchemy connection pool with pre-ping and recycling for better connection management
def get_sqlalchemy_engine(tunnel):
    pool = create_engine(
        "mysql+pymysql://",
        creator=lambda: get_connection(tunnel),
        pool_pre_ping=True,    # Ensure connection is alive before executing a query
        pool_recycle=600,     # Recycle connections every 1 hour to prevent disconnection 
        pool_size=1000,           # Set pool size to handle multiple connections
        max_overflow=1000        # Allow 10 extra simultaneous connections if needed
    )
    return pool

# Database insertions
def insert_participant_and_get_id(pool):
    try:
        with pool.connect() as connection:
            insert_query = text("INSERT INTO df_participants_german (age, gender_identity, country_of_residence, ancestry, ethnicity) VALUES (NULL, NULL, NULL, NULL, NULL)")
            result = connection.execute(insert_query)
            last_id_query = text("SELECT LAST_INSERT_ID()")
            last_id_result = connection.execute(last_id_query)
            last_id = last_id_result.scalar()
            return last_id
    except SQLAlchemyError as e:
        st.error(f"Database insertion failed: {e}")
        raise

def insert_prolific_id(pool, participant_id, prolific_id):
    try:
        insert_query = """INSERT INTO df_prolific_ids_german (participant_id,prolific_id) VALUES (%s, %s)"""
        with pool.connect() as db_conn:
            db_conn.execute(insert_query, (participant_id, prolific_id))
    except SQLAlchemyError as e:
        st.error(f"Failed to insert Prolific ID: {e}")
        raise



# Main logic
if not all([consent1, consent2, consent3]):
    st.write("Bitte gib deine Zustimmung, indem du alle drei Kästchen ankreuzt.")

elif all([consent1, consent2, consent3]):
    st.write("Bitte gib deine eindeutige Prolific-ID ein, damit wir deine Teilnahme registrieren können.")
    prolific_id = st.text_input("Gib deine eindeutige Prolific-ID ein:", max_chars=50)
    
    if st.button("Submit ID"):
        if prolific_id:
            tunnel = start_ssh_tunnel()
            pool = get_sqlalchemy_engine(tunnel)
            
            last_inserted_id = insert_participant_and_get_id(pool)
            insert_prolific_id(pool, last_inserted_id, prolific_id)
            st.session_state['participant_id'] = last_inserted_id
            tunnel.stop()  # Stop tunnel when done
        else:
            st.write("Bitte gib deine Prolific ID ein, um fortzufahren.")

if 'participant_id' in st.session_state:
    st.write("Lassen uns einen besseren Datensatz erstellen!")
    st.switch_page("pages/Rate_responses.py")

