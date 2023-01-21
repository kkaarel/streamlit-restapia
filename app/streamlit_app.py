import streamlit as st
import pandas as pd
import requests
import json



url = "https://avoindata.prh.fi/tr/v1/"
verodata = "https://streamlitinfradev.blob.core.windows.net/datastreamlit/export.csv"

df_pre = pd.read_csv(verodata)

df = df_pre[df_pre['Verotettava tulo'] > 0]

option = df['Business_ID']

st.title("PRH")

Business_id = st.selectbox("Search by business id:", option) #st.text_input("Enter a business id", placeholder="Format: 000000-0")



def send_request_to_prh(Business_id):

    data = requests.get("https://avoindata.prh.fi/tr/v1/{}".format(Business_id)).json()

    return st.write(pd.json_normalize(data['results']))


def vero_tulot(Business_id):
    filtered_df = df[df['Business_ID'].str.contains(Business_id, case=False, na=False)]

    return st.write(filtered_df)


def kpis(Business_id):

    st.title("Verot ja tulot")
    calulcated_data = df[df['Business_ID'].str.contains(Business_id, case=False, na=False)]
    tulo = calulcated_data['Verotettava tulo'].sum()
    vero = calulcated_data['Maksuunpannut verot yhteensä'].sum()
    # WE CREATE FOUR COLUMNS HERE TO HOLD THE METRIC
    col1, col2 = st.columns(2)

    col1.metric(label = "Verotettava tulo",
    value = "{} €".format(tulo),
    #delta = "{} %".format(round(float((Carbon - Carbon)/Carbon) *100, 1))
    )
    col2.metric(label="Maksuunpannut verot yhteensä",
    value = "{} €".format(vero),
    #delta = "{} %".format(round(float((engery - Carbon)/Carbon) *100, 1))
    )

def bar_chart_vero(Business_id):
    
    calulcated_data = df[df['Business_ID'].str.contains(Business_id, case=False, na=False)]
    return st.bar_chart(calulcated_data, y={"Verotettava tulo","Maksuunpannut verot yhteensä"}, x={"Verotettava tulo","Maksuunpannut verot yhteensä"})
    

# Send the number using request post
if st.button("Submit"):
    if Business_id is not None and Business_id.strip()!='':
        try:
            send_request_to_prh(Business_id)
            vero_tulot(Business_id)
            kpis(Business_id)
            bar_chart_vero(Business_id)

        except ValueError:
            st.error("Invalid Business id, please enter a valid number.")    
    else:
        st.error("Invalid Business id, please enter a valid number.")

