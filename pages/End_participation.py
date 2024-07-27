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

st.title("Danke für deinen Beitrag!")
st.write("Vielen Dank, dass du an unserer Studie teilgenommen hast und uns hilfst, das Alignment von Large Language Models zu verbessern.")
st.balloons()

st.write("Wenn du auf die folgende Schaltfläche klickst, wirst du zurück zu Prolifics weitergeleitet, damit dein Beitrag gezählt werden kann.")
st.link_button("Weiterleiten zu Prolifics", "https://app.prolific.com/submissions/complete?cc=C13U5HGT")

st.write("Alternativ kannst du direkt den folgenden Completion-Code kopieren: C13U5HGT")