import streamlit as st
import streamlit_survey as ss
import json
import pandas as pd
from sqlalchemy import create_engine, text
import pymysql
import sqlalchemy
import os
import paramiko
import pymysql
from sshtunnel import SSHTunnelForwarder

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
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

# Set up port forwarding
tunnel = SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=(db_host, db_port)
)
tunnel.start()

# Function to create a new database connection
def getconn():
    conn = pymysql.connect(
        host='127.0.0.1',
        user=db_user,
        password=db_password,
        database=db_name,
        port=tunnel.local_bind_port
    )
    return conn

# Create a SQLAlchemy engine
pool = create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

def update_participant(participant_id, age, gender_identity, country_of_residence, ancestry, ethnicity):
    update_query = text("""
    UPDATE df_participants_german
    SET age = :age,
        gender_identity = :gender_identity,
        country_of_residence = :country_of_residence,
        ancestry = :ancestry,
        ethnicity = :ethnicity
    WHERE participant_id = :participant_id
    """)
    with pool.connect() as connection:
        connection.execute(update_query, {
            'participant_id': participant_id,
            'age': age,
            'gender_identity': gender_identity,
            'country_of_residence': country_of_residence,
            'ancestry': ancestry,
            'ethnicity': ethnicity
        })

##start survey
survey = ss.StreamlitSurvey("demographics_survey")

#load data
df_countries = pd.read_csv("UNSD_Methodology_ancestry.csv", sep = ";")

age_groups = ["Ich möchte keine Angaben machen","18-30", "31-40", "41-50","51-60", "60<"]
pronouns = [
    "Ich möchte keine Angaben machen",
    "she/her/hers",
    "he/him/his",
    "they/them/theirs",
    "ze/hir/hirs",
    "xe/xem/xyrs",
    "ey/em/eirs",
    "ve/ver/vis",
    "per/pers/perself"
]
racial_groups = [
    "Ich möchte keine Angaben machen",
    "Amerikanischer Indianer oder Alaska-Ureinwohner",
    "Asiatisch",
    "Schwarz oder Afroamerikaner",
    "Hispano- oder Latinoamerikaner",
    "Mittlerer Osten oder Nordafrika",
    "Eingeborener Hawaiianer oder Pazifikinsulaner",
    "Weiss"
]

list_countries = sorted(df_countries["Country or Area"].to_list())
list_countries.insert(0, "Ich möchte keine Angaben machen")

st.title("Du @ Aligniverse")
st.write("Deine Bewertungen werden zur Entwicklung eines Open-Source-Datensatzes beitragen, den KI-Praktiker nutzen können, um ihre großen Sprachmodelle (LLMs) abzustimmen. Für die Erstellung dieses Datensatzes ist es wichtig, einige Informationen über dich zu sammeln, um die spezifische demografische Gruppe, der du angehörst, zu bestimmen. Da demografische Daten aggregiert werden, wird es nicht möglich sein, einzelne Teilnehmer zu identifizieren.")

q1_demo = survey.selectbox("Zu welcher Altersgruppe gehörst du?", options=age_groups, id="Q1_demo", index=None)
q2_demo = survey.selectbox("Welche Pronomen verwendest du, um dich zu identifizieren?", options=pronouns, id="Q2_demo", index=None)

q3_demo = survey.multiselect("In welchem Land wohnst du?", options=list_countries, id="Q3_demo", max_selections = 3)
q3_demo_str = json.dumps(q3_demo)

q4_demo = survey.multiselect("Woher stammen deine Vorfahren (z. B. Urgroßeltern)?", options=list_countries, id="Q4_demo", max_selections = 3)
q4_demo_str = json.dumps(q4_demo)

q5_demo = survey.multiselect("Mit welcher(n) rassischen Gruppe(n) identifizierst du dich?", options=racial_groups, id="Q5_demo", max_selections = 3)
q5_demo_str = json.dumps(q5_demo)

def get_last_id():
    with pool.connect() as connection:
        last_id_query = text("SELECT LAST_INSERT_ID()")
        last_id_result = connection.execute(last_id_query)
        last_id = last_id_result.scalar()
        return last_id

if 'participant_id' not in st.session_state:
    last_id = get_last_id()
    st.session_state['participant_id'] = last_id

if not all([q1_demo, q2_demo, q3_demo, q4_demo, q5_demo]):
    st.write("Bitte wähle bei jeder Frage mindestens eine Option aus. Du hast immer die Möglichkeit, keine Angaben zu machen.")

elif all([q1_demo, q2_demo, q3_demo, q4_demo, q5_demo]):
    if st.button("Einreichen"):
        update_participant(
            st.session_state['participant_id'], #participant
            q1_demo, #age
            q2_demo, #gender identity
            q3_demo_str, #country of residence
            q4_demo_str, #ancestry
            q5_demo_str  #ethnicity
        )
        st.switch_page("pages/End_participation.py")
