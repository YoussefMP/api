import streamlit as st
import requests
import time
import datetime
import os
import pandas as pd
from html import escape
import json 
import streamlit.components.v1 as components
import base64


CLIENTS = {
    "90": "Smart City Paderborn",
    "91": "Benutzer 2",
    "92": "Benutzer 3",
}

st.set_page_config(layout="wide")
main_top, main_bot = st.container(), st.container()
if "stage" not in st.session_state:
    st.session_state.stage = 0


def generate_table(data):
    rows = ""
    for i, row in enumerate(data.iterrows()):
        # Icons with tooltips and download links
        metadata_icon = f"""<span class="tooltip" style="cursor: pointer;">📄<span class="tooltiptext">{escape(row[1]["metadata"])}</span></span>"""
        download_icon = f'<a href="./SmartCity/DataPipeline/Data/{escape(st.session_state.client)}/{escape(row[1]["file"])}" download="{escape(row[1]["file"])}" style="margin-left: 10px; cursor: pointer;">⬇️</a>'
        start = "\n" if not rows else "" 
        rows += f"""{start}<tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{escape(row[1]['name'])}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{escape(row[1]['description'])}</td>
            <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{metadata_icon} {download_icon}</td>
        </tr>
        """

    return f"""
    <style>.tooltip {{position: relative;}} .tooltiptext {{visibility: hidden; width: 200px; background-color: #6c757d; color: #fff; text-align: center; border-radius: 5px; padding: 5px; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -100px; opacity: 0; transition: opacity 0.3s;}} .tooltip:hover .tooltiptext {{visibility: visible; opacity: 1;}}</style>
    <table style="font-family: 'IBM Plex Sans', sans-serif; color: #fff; width:100%; border-collapse: collapse;">
        <thead>
            <tr style="border-bottom: 1px solid #fff;">
                <th style="padding: 8px; border: 1px solid #fff;">Datensätze</th>
                <th style="padding: 8px; border: 1px solid #fff;">Beschreibung der Datensätze</th>
                <th style="padding: 8px; border: 1px solid #fff;">Metadaten</th>
            </tr>
        </thead>
        <tbody>
            {rows}</tbody>
    </table>
    """


def get_client_data(client):
    result = {"name": [],
              "description": [],
              "metadata": [],
              "file": []
              }

    cid = client.strip("cl")
    if not os.path.exists(f"./SmartCity/DataPipeline/Data/{cid}"):
        return None
    
    files_list = os.listdir(f"./SmartCity/DataPipeline/Data/{cid}")

    for f in files_list:
        if ".json" in f:
            continue
        else: 
            name = f[:f.rfind(".")]
            result["name"].append(name)
            
            metadata_file = open(f"./SmartCity/DataPipeline/Data/{cid}/{name}.json", "r", encoding="utf-8") 
            metadata = json.load(metadata_file)

            result["description"].append(metadata["text_desc"])
            result["file"].append(f)

            md = ""

            for k, v in dict(metadata["inspire_desc"]).items():
                md += f"{k}: {v}\n"

            result["metadata"].append(md)


    return result


def go_stage_two(client):
    st.session_state.stage = 2
    st.session_state.client = client.strip("cl")

def go_stage_three(client):
    st.session_state.stage = 3


with st.sidebar:
    top_section, bot_section, investors = st.container(), st.container(), st.container()

    with top_section: 
        t_col1, t_col2 = st.columns([2, 1])
        with t_col1:
            st.title(f"API Endpunkt")
        with t_col2:
            st.page_link("http://localhost:8080/docs", label="API Dokumentation")
        sb_col1, sb_col2 = st.columns([6, 2])
        with sb_col1:
            server_url = st.text_input("Endpoint URL", "http://localhost:8000", label_visibility="collapsed")
        with sb_col2:
            connect_btn = st.button("Verbinden")
    
    if connect_btn:
        st.session_state.stage += 1
    else: 
        st.session_state.connected = 0



lottie_paths = {
    1: "./SmartCity/DataPipeline/GUI/Connect_part.json",
    2: "./SmartCity/DataPipeline/GUI/Authenticate_part.json",
    3: "./SmartCity/DataPipeline/GUI/transfer_data.json", 
}

time_waits = [3.5, 2.5, 4.5] 

if st.session_state.stage >= 1:
    with open(lottie_paths[st.session_state.stage], "rb") as f:
        lottie_json = f.read()
    lottie_base64 = base64.b64encode(lottie_json).decode("utf-8")

    animation_html = f"""<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
    <div style="display: flex; justify-content: center; align-items: flex-start; height: auto; width: 100%; margin-top: -200px;">
        <dotlottie-player src="data:application/json;base64,{lottie_base64}" 
                        background="transparent" 
                        speed="1.5" 
                        style="width: 650px; height: 650px;" 
                        autoplay>
        </dotlottie-player>
    </div>
    """
    with main_top:
        components.html(animation_html, height=350)

    if st.session_state.stage == 1:
        time.sleep(time_waits[st.session_state.stage-1])
    with bot_section:
        sbb_col1, sbb_col2 = st.columns([4, 1])

        with sbb_col1:
            st.header("Wählen Sie bitte einen Benutzer aus ...")
            connect_as_btns = []
            connect_as_btns.append(st.button("Verbinden als Smart City Padeborn", on_click=go_stage_two, args=["cl90"]))
            connect_as_btns.append(st.button("Verbinden als Benutzer 2", on_click=go_stage_two, args=["cl91"]))
            connect_as_btns.append(st.button("Verbinden als Benutzer 3", on_click=go_stage_two, args=["cl92"]))
        
        with sbb_col2:
            st.image("./SmartCity/DataPipeline/GUI/Logo.png")
        

        if st.session_state.stage >= 2:
            if st.session_state.stage == 2:
                time.sleep(time_waits[st.session_state.stage-1])
            with sbb_col1:
                st.header("Sie können jetzt eine Anfrage senden...")                
                st.button("Verfügare Datensätze abfragen", on_click=go_stage_three, args=[st.session_state.client])


            if st.session_state.stage == 3:
                time.sleep(time_waits[st.session_state.stage -1])

            if st.session_state.stage >= 3:
                data = get_client_data(st.session_state.client)
                with main_bot: 
                    if data:
                        st.header(f"Diese Daten sind für den Benutzer {CLIENTS[st.session_state.client]} verfügbar")
                        # Render the table
                        table_html = generate_table(pd.DataFrame(data))
                        # st.markdown(table_html, unsafe_allow_html=True)
                        components.html(table_html, height=500)
                    else:
                        st.header(f"Für {CLIENTS[st.session_state.client]} stehen keine Daten zur Verfügung")


