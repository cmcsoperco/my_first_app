import pandas as pd
import streamlit as st
import os
import shutil
import PyPDF2
import openpyxl
from PyPDF2 import PdfMerger
from io import BytesIO
from json import loads, dumps
import zipfile
from PyPDF2 import PdfReader, PdfWriter


#Page configure
st.set_page_config(page_title="Data Analysis", layout="wide")
st.subheader(":green[This site has been developed by]:red[ Rajib Mondal(Manager-IT, CCD)]")
st.image(image="rm_logo.png")

#TABs
tabs = st.tabs(['206AB PDF To Excell', 'Merge Files(txt, csv, excel)', 'Merge PDFs', 'Split PDF', 'Excel To JSON'])

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
            files = st.file_uploader("Import files to merge", accept_multiple_files=True, label_visibility='collapsed', type=['csv', 'txt', 'xlsx'])
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
    cols_tab_2 = st.columns([3,5])
    with cols_tab_2[0]:
        with st.container(border=True, height=500):
            pdf_files = st.file_uploader("Import pdf files to merge", accept_multiple_files=True, label_visibility='collapsed', type=['pdf'])
            if(pdf_files):
                merger = PdfMerger()
                for pdf in pdf_files:
                    merger.append(pdf)

                byteIo = BytesIO()
                merger.write(byteIo)
                st.download_button(label="Merge PDFs and Download", data=byteIo, file_name="merged.pdf")

#Split PDF
with tabs[3]:
    cols_tab_3 = st.columns([2.5, 5])
    with cols_tab_3[0]:
        with st.container(border=True, height=450):
            pdf_file_to_be_split = st.file_uploader("Import pdf file to split", accept_multiple_files=False, label_visibility='collapsed', type=['pdf'])
            if (pdf_file_to_be_split):
                if(st.button("Split")):
                    byteIo_zip = BytesIO()
                    zip_object = zipfile.ZipFile(byteIo_zip,'w')
                    pdf = PdfReader(pdf_file_to_be_split)
                    for page_number, page in enumerate(pdf.pages):
                        writer = PdfWriter()
                        writer.add_page(page)
                        output_filename = f'page_{page_number + 1}.pdf'
                        temp_file = f'temp_{page_number + 1}.pdf'
                        with open(temp_file, 'wb') as temp_output:
                            writer.write(temp_output)

                        zip_object.write(temp_file)
                        os.remove(temp_file)
                    zip_object.close()
                    #byteIo_zip.close()
                    st.warning(":green[PDF file splitting is completed😊]", icon="😊")
                    st.download_button(label="Download", data=byteIo_zip, file_name="pdf_files.zip")

#Excel To JSON
with tabs[4]:
    cols_tab_4 = st.columns([2.5,5])
    with cols_tab_4[0]:
        with st.container(border=True, height=450):
            df_json = []
            excel_file = st.file_uploader("Import excel file to make json", accept_multiple_files=False, label_visibility='collapsed', type=['xlsx'])
            if(excel_file):
                df_json.append(pd.read_excel(excel_file, dtype={'major_head': 'str', 'minor_head': 'str'}))
                json_content = df_json[0].to_json(orient="records")
                parsed = loads(json_content)
                json_output = dumps(parsed, indent=2)
                st.download_button(label="Make JSON file and Download", data=json_output, file_name="your_json_file.json")
    with cols_tab_4[1]:
        with st.container(border=True, height=450):
            if(excel_file):
                st.dataframe(df_json[0])
