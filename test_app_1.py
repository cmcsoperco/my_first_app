import pandas as pd
import streamlit as st
import os
import shutil
import PyPDF2
import openpyxl

#Page configure
st.set_page_config(page_title="Field Wise File Maker and PDF(206AB) to excel", page_icon=":bar_chart:", layout="wide")
st.subheader(":green[This site has been developed by]:red[ Rajib Mondal(Manager-IT, CCD)]")
st.image(image="cbi_logo.png")

tabs = st.tabs(['Field Wise Files Making', '206AB pdf to excell making'])
with tabs[0]:
    #st.write('This is TAB-1')
    cols = st.columns([1.5, 5])
    with cols[0]:
        with st.container(border=True, height=600):
            # st.image(image="cbi_logo.png")
            file = st.file_uploader("Import file", label_visibility='collapsed', type=["csv"])
    with cols[1]:
        with st.container(border=True, height=600):
            if(file == None):
                st.warning(":red[You have not selected any csv file]", icon="❌")
            else:
                df = pd.read_csv(file)
                st.write(f"This file contains :green[{str(df.last_valid_index() + 1)}] records")
                st.dataframe(df)
with tabs[1]:
    #st.write('This is TAB-2')
    cols_tab_2 = st.columns([3,5])
    with cols_tab_2[0]:
        with st.container(border=True, height=500):
            files = st.file_uploader("Import file", accept_multiple_files=True, label_visibility='collapsed')
            atleast_one_pdf_file = False
            for f in files:
                if (f.name.split(".")[-1].lower() == "pdf"):
                    atleast_one_pdf_file = True
            data_read = []
            if (files != []):
                button_make_206AB_pdf_to_excel = st.button("Make_Excel")


    with cols_tab_2[1]:
        with st.container(border=True, height=500):
            if(atleast_one_pdf_file):
                if (button_make_206AB_pdf_to_excel):
                    result_file = "result__pdf_to_excel_206AB.xlsx"
                    for file in files:
                        if (file.name.split(".")[-1].lower() == "pdf"):
                            temp_list = []
                            reader = PyPDF2.PdfReader(file)
                            data = reader.pages[0].extract_text().split("\n")
                            temp_list.append(file.name)
                            temp_list.append(data[7][23:33])
                            temp_list.append(data[8][5:])
                            temp_list.append(data[9][19:])
                            temp_list.append(data[10][11:])
                            temp_list.append(data[11][36:])
                            data_read.append(temp_list)

                    dfrm = pd.DataFrame(data_read,
                                        columns=['File_Name', 'PAN', 'Name', 'PAN Allotment Date', 'PAN Status',
                                                 'Specified Person u/s 206AB & 206CCA'])
                    st.warning(":green[pdf files to excel making is completed😊]", icon="😊")
                    st.dataframe(dfrm)

            else:
                st.warning(":red[You have not selected any pdf file]", icon="❌")


