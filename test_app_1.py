import pandas as pd
import streamlit as st
import os
import shutil
import PyPDF2
import openpyxl
from PyPDF2 import PdfMerger
from io import BytesIO


#Page configure
st.set_page_config(page_title="Data Analysis", layout="wide")
st.subheader(":green[This site has been developed by]:red[ Rajib Mondal(Manager-IT, CCD)]")
st.image(image="rm_logo.png")

#TABs
tabs = st.tabs(['206AB PDF To Excell', 'Merge Files(txt, csv, excel)', 'Merge PDFs'])

#206AB PDF To Excell
with tabs[0]:
    cols_tab_0 = st.columns([3,5])
    with cols_tab_0[0]:
        with st.container(border=True, height=500):
            files = st.file_uploader("Import 206AB pdf files", accept_multiple_files=True, label_visibility='collapsed', type=['pdf'])
            if(files):
                button_make_206AB_pdf_to_excel = st.button("Make Excel")

    with cols_tab_0[1]:
        with st.container(border=True, height=500):
            if(files):
                data_read = []
                if (button_make_206AB_pdf_to_excel):
                    result_file = "result__pdf_to_excel_206AB.xlsx"
                    for file in files:
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

#Merge Files(txt, csv, excel)
with tabs[1]:
    cols_tab_1 = st.columns([2, 5])
    with cols_tab_1[0]:
        with st.container(border=True, height=560):
            files = st.file_uploader("Import 206AB pdf files", accept_multiple_files=True, label_visibility='collapsed', type=['csv', 'txt', 'xlsx'])
            merged_dfs = []
            if (files):
                text_input_separator = st.text_input(label="", placeholder="Enter text separator for text/csv file (comma is default)")
                button_merge_files = st.button("Merge Files")

                if(button_merge_files):

                    separator = ","
                    if(text_input_separator != ""):
                        separator = text_input_separator


                    for file in files:
                        if((file.name.split(".")[-1].lower() == "csv") or (file.name.split(".")[-1].lower() == "txt")):
                            merged_dfs.append(pd.read_csv(file, low_memory=False, encoding_errors='ignore', sep=separator, keep_default_na=False))

                        if(file.name.split(".")[-1].lower() == "xlsx"):
                            merged_dfs.append(pd.read_excel(file, keep_default_na=False))

    with cols_tab_1[1]:
        with st.container(border=True, height=560):
            if(len(merged_dfs) > 0):
                df = pd.concat(merged_dfs, ignore_index=True)
                st.warning(":green[Files merging is completed😊]", icon="😊")
                st.dataframe(df)
                st.download_button(label="Download Merged File", data=df.to_csv(index=False), mime='csv', file_name="your_merged_file.csv")

#Merge PDFs
with tabs[2]:
    cols_tab_0 = st.columns([3,5])
    with cols_tab_0[0]:
        with st.container(border=True, height=500):
            pdf_files = st.file_uploader("Import pdf files to merge", accept_multiple_files=True, label_visibility='collapsed', type=['pdf'])
            if(pdf_files):
                merger = PdfMerger()
                for pdf in pdf_files:
                    merger.append(pdf)

                byteIo = BytesIO()
                merger.write(byteIo)
                st.download_button(label="Download Merged PDF", data=byteIo, file_name="merged.pdf")

#Split PDF
