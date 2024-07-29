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
st.subheader(":red[This site has been developed by]:green[ Rajib Mondal")
st.image(image="rm_logo.png")

#TABs
tabs = st.tabs(['206AB PDF To Excell', 'Merge Files(txt, csv, excel)', 'Merge PDFs', 'Split PDF', 'Excel To JSON', 'Field Wise Files Making', 'Split File(txt, csv, excel)', 'Find and Remove Duplicates'])

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
            files = st.file_uploader("Import files to merge(txt, csv, excel)", accept_multiple_files=True, label_visibility='collapsed', type=['csv', 'txt', 'xlsx'])
            merged_dfs = []
            if (files):
                text_input_separator_merge_files = st.text_input(label="Enter text separator_merge_files", placeholder="Enter text separator for text/csv file (comma is default)", label_visibility="collapsed")
                button_merge_files = st.button("Merge Files")

                if(button_merge_files):
                    separator = ","
                    if(text_input_separator_merge_files != ""):
                        separator = text_input_separator_merge_files

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
                    st.download_button(label="Download Split Files", data=byteIo_zip, file_name="pdf_files.zip")

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

#Field Wise Files Making
with tabs[5]:
    cols_tab_5 = st.columns([2, 5])
    with cols_tab_5[0]:
        with st.container(border=True, height=560):
            text_input_separator_field_wise_files_making = st.text_input(label="Enter text separator_field_wise_files", placeholder="Enter text separator for text/csv file (comma is default)", label_visibility="collapsed")
            separator = ","
            if (text_input_separator_field_wise_files_making != ""):
                separator = text_input_separator_field_wise_files_making
            file_to_make_field_wise_files = st.file_uploader("Import file to field wise file making", accept_multiple_files=False, label_visibility='collapsed', type=['csv', 'txt', 'xlsx'])
            if (file_to_make_field_wise_files):
                #@st.cache_resource()
                def read_file(file_to_make_field_wise_files):
                    if((file_to_make_field_wise_files.name.split(".")[-1].lower() == "csv") or (file_to_make_field_wise_files.name.split(".")[-1].lower() == "txt")):
                        df = pd.read_csv(file_to_make_field_wise_files, low_memory=False, encoding_errors='ignore', sep=separator, keep_default_na=False)
                    if(file_to_make_field_wise_files.name.split(".")[-1].lower() == "xlsx"):
                        df = pd.read_excel(file_to_make_field_wise_files, keep_default_na=False)
                    return df

                df = read_file(file_to_make_field_wise_files)
                field_wise_file_name = st.selectbox("Select field wise file name:", list(df.columns), index=None, placeholder="Select field...")
                if(field_wise_file_name != None):
                    button_make_field_wise_files = st.button(f"Make {field_wise_file_name} Wise Files")

                    if(button_make_field_wise_files):
                        byteIo_zip = BytesIO()
                        zip_object = zipfile.ZipFile(byteIo_zip, 'w')

                        field_names_list = list(df.pivot_table(index=[field_wise_file_name], aggfunc='count').index.values)
                        for field_name in field_names_list:
                            if (field_name == ""):
                                fie_name = "blank_field.csv"
                            else:
                                fie_name = str(field_name) + ".csv"
                            df[df[field_wise_file_name] == field_name].to_csv(fie_name, index=False)
                            zip_object.write(fie_name)
                            os.remove(fie_name)
                        zip_object.close()
                        st.warning(f":green[{field_wise_file_name} wise files making is completed😊]", icon="😊")
                        st.download_button(label=f"Download {field_wise_file_name} Wise Files", data=byteIo_zip, file_name=f"{field_wise_file_name}_wise_files.zip")

    with cols_tab_5[1]:
        with st.container(border=True, height=560):
            if (file_to_make_field_wise_files):
                st.warning(":green[For better experience, showing first 10000 records only]", icon="😊")
                st.dataframe(df.head(10000))

#File split(".txt", ".csv", ".xlsx")
with tabs[6]:
    cols_tab_6 = st.columns([3, 4])
    with cols_tab_6[0]:
        with st.container(border=True, height=570):
            text_input_separator_file_split = st.text_input(label="Enter text separator_split_file", placeholder="Enter text separator for text/csv file (comma is default)", label_visibility='collapsed')
            separator = ","
            if (text_input_separator_file_split != ""):
                separator = text_input_separator_file_split
            file_to_split = st.file_uploader("Import file to split(txt, csv, xlsx)", accept_multiple_files=False, label_visibility='collapsed', type=['csv', 'txt', 'xlsx'])
            if (file_to_split):
                def read_file(file_to_make_field_wise_files):
                    if((file_to_make_field_wise_files.name.split(".")[-1].lower() == "csv") or (file_to_make_field_wise_files.name.split(".")[-1].lower() == "txt")):
                        df = pd.read_csv(file_to_make_field_wise_files, low_memory=False, encoding_errors='ignore', sep=separator, keep_default_na=False)
                    if(file_to_make_field_wise_files.name.split(".")[-1].lower() == "xlsx"):
                        df = pd.read_excel(file_to_make_field_wise_files, keep_default_na=False)
                    return df

                df = read_file(file_to_split)
                #######
                cols_tab_6_1 = st.columns([1, 1])
                with cols_tab_6_1[0]:
                    with st.container(border=True, height=335):
                        number_input_start_index_file_split = st.number_input(":blue[Enter start index :]", value=1, placeholder="Enter start index...", min_value=1)
                        number_input_end_index_file_split = st.number_input(":blue[Enter end index :]", value=None, placeholder="Enter end index...", min_value=number_input_start_index_file_split + 1)
                        btn_split_index_wise = st.button(":red[Split Index Wise]")
                        if(btn_split_index_wise):
                            if(number_input_end_index_file_split == None):
                                st.warning(":red[End index should not be blank or less than start index]", icon="❌")
                            else:
                                data_index_wise = df[(int(number_input_start_index_file_split) - 1):int(number_input_end_index_file_split)].to_csv(index=False)
                                st.download_button(":green[Download Index Wise Split File]", data=data_index_wise, file_name=f"split_file_range_{int(number_input_start_index_file_split)}_to_{number_input_end_index_file_split}.csv")

                with cols_tab_6_1[1]:
                    with st.container(border=True, height=335):
                        number_input_records_per_file_file_split = st.number_input(":blue[Enter records per file :]", value=None, placeholder="Enter records per file...", min_value=1)
                        btn_split_auto= st.button(":red[Auto Split]")
                        if(btn_split_auto):
                            if (number_input_records_per_file_file_split == None):
                                st.warning(":red[End index should not be blank or less than 1]", icon="❌")
                            else:
                                loop_count = int((df.last_valid_index() + 1) / (int(number_input_records_per_file_file_split))) + 1

                                byteIo_zip_auto_split = BytesIO()
                                zip_object_auto_split = zipfile.ZipFile(byteIo_zip_auto_split, 'w')

                                for i in range(loop_count):
                                    start_index = int(number_input_records_per_file_file_split) * i
                                    end_index = int(number_input_records_per_file_file_split) * (i + 1)
                                    if (start_index == df.last_valid_index() + 1):
                                        break
                                    if (i == loop_count - 1):
                                        end_index = df.last_valid_index() + 1
                                    auto_split_file_name = str(i + 1) + "_" + "_Range_" + str(start_index + 1) + "_to_" + str(end_index) + ".csv"
                                    df[start_index: end_index].to_csv(auto_split_file_name, index=False)
                                    zip_object_auto_split.write(auto_split_file_name)
                                    os.remove(auto_split_file_name)
                                zip_object_auto_split.close()
                                st.warning(f":green[😊Auto splitting per file {number_input_records_per_file_file_split} records is done]")
                                st.download_button(label=":green[Download Auto Split Files]", data=byteIo_zip_auto_split, file_name="auto_split_files.zip")

    with cols_tab_6[1]:
        with st.container(border=True, height=560):
            if (file_to_split):
                st.warning(f"Total: :red[{df.last_valid_index() + 1}] 😊 :green[For better experience, showing first 10000 records only]")
                st.dataframe(df.head(10000))

#Find and Remove Duplicates
with tabs[7]:
    cols_tab_7 = st.columns([2, 4])
    with cols_tab_7[0]:
        with st.container(border=True, height=530):
            text_input_separator_find_and_remove_dup = st.text_input(label="", placeholder="Enter text separator for text/csv file (comma is default)", label_visibility='collapsed')
            separator = ","
            if (text_input_separator_find_and_remove_dup != ""):
                separator = text_input_separator_find_and_remove_dup
            file_to_find_and_remove_dup = st.file_uploader("Import file to find and remove duplicates", accept_multiple_files=False, label_visibility='collapsed', type=['csv', 'txt', 'xlsx'])
            if (file_to_find_and_remove_dup):
                def read_file(file_to_make_field_wise_files):
                    if((file_to_make_field_wise_files.name.split(".")[-1].lower() == "csv") or (file_to_make_field_wise_files.name.split(".")[-1].lower() == "txt")):
                        df = pd.read_csv(file_to_make_field_wise_files, low_memory=False, encoding_errors='ignore', sep=separator, keep_default_na=False)
                    if(file_to_make_field_wise_files.name.split(".")[-1].lower() == "xlsx"):
                        df = pd.read_excel(file_to_make_field_wise_files, keep_default_na=False)
                    return df

                df = read_file(file_to_find_and_remove_dup)
                ##########################################################
                with st.container(border=True, height=290):
                    cols_tab_7_1 = st.columns([2, 3])
                    with cols_tab_7_1[0]:
                        selectbox_find_or_remove_dups = st.selectbox(":green[Find or remove duplicates:]", ['Remove Duplicates', 'Find Duplicates'])
                    with cols_tab_7_1[1]:
                        #selectbox_duplicated_by_col = st.selectbox(":green[Select duplicated by col:]", list(df.columns), index=None, placeholder="Select duplicated by...")
                        selectbox_duplicated_by_col = st.multiselect(":green[Select duplicated by columns:]", list(df.columns), placeholder="Select duplicated by...")

                    st.markdown("");st.markdown("")
                    if(selectbox_duplicated_by_col != []):
                        if(selectbox_find_or_remove_dups == 'Remove Duplicates'):
                            button_remove_dups = st.button(f":red[Remove duplicates by]")
                            if(button_remove_dups):
                                st.write("Removed duplicates😊 Please download the file👇")
                                st.download_button(":green[Download Removed Duplicates]", data=df.drop_duplicates(subset=selectbox_duplicated_by_col).to_csv(index_label=False), file_name="removed_duplicates.csv")

                        elif(selectbox_find_or_remove_dups == 'Find Duplicates'):
                            button_find_dups = st.button(f":red[Find duplicates by]")
                            if(button_find_dups):
                                st.write("Found duplicates😊 Please download the file👇")
                                st.download_button(":green[Download Found Duplicates]", data=df[df.duplicated(selectbox_duplicated_by_col, keep=False)].to_csv(index_label=False), file_name="found_duplicates.csv")

    with cols_tab_7[1]:
        with st.container(border=True, height=530):
            if (file_to_find_and_remove_dup):
                st.warning(f"Total: :red[{df.last_valid_index() + 1}] 😊 :green[For better experience, showing first 10000 records only]")
                st.dataframe(df.head(10000))
