import streamlit as st
import pandas as pd
import base64
from collections import Counter

def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download csv file</a>'
    return href

def get_text_file_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download txt file</a>'
    return href

st.title('Domain Name Filter')

uploaded_file = st.file_uploader("Upload a file", type=["txt"])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    str_data = bytes_data.decode("utf-8")
    lines = str_data.split("\n")
    domain_extension_count = Counter([line.split('.')[-1] for line in lines if line])

    data = []
    for ext, count in domain_extension_count.items():
        row = {}
        row['Domain Extension'] = ext
        row['Domain Count'] = count
        row['Domains'] = "\n".join([url for url in lines if url and url.split('.')[-1] == ext])
        data.append(row)

    df = pd.DataFrame(data)

    # Popular Extensions - you may update this list as per your requirements
    popular_exts = ['.com', '.org', '.net', '.io']

    df['sort_col'] = df['Domain Extension'].apply(lambda x: popular_exts.index(x) if x in popular_exts else len(popular_exts))
    df.sort_values(['sort_col', 'Domain Extension'], inplace=True)
    df.drop('sort_col', axis=1, inplace=True)

    # Sorting buttons
    sort_by = st.selectbox('Sort by', ['Domain Extension', 'Domain Count'])
    if sort_by == 'Domain Extension':
        df = df.sort_values('Domain Extension', ascending=True)
    else:
        df = df.sort_values('Domain Count', ascending=False)

    # Headers
    cols = st.columns(4)
    cols[0].header('Domain Extension')
    cols[1].header('Domain Count')
    cols[2].header('Download CSV')
    cols[3].header('Download TXT')

    # Data
    for _, row in df.iterrows():
        cols = st.columns(4)
        cols[0].write(row['Domain Extension'])
        cols[1].write(row['Domain Count'])
        domain_df = pd.DataFrame(row['Domains'].split("\n"), columns=["Domains"])
        cols[2].markdown(get_table_download_link(domain_df, f"{row['Domain Extension']}.csv"), unsafe_allow_html=True)
        cols[3].markdown(get_text_file_download_link(row['Domains'], f"{row['Domain Extension']}.txt"), unsafe_allow_html=True)
