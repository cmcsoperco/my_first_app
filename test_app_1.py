import pandas as pd
import streamlit as st
import os
import shutil
import PyPDF2
import openpyxl


#Page configure
st.set_page_config(page_title="Field Wise File Maker", page_icon=":bar_chart:", layout="wide")
st.subheader(":green[This site has been developed by]:red[ Rajib Mondal(Manager-IT, CCD)]")
#st.image(image="cbi_logo.png")

tabs = st.tabs(['Field Wise Files Making', '206AB pdf to excell making'])
with tabs[0]:
    #st.write('This is TAB-1')
    cols = st.columns([1.5, 5])
    with cols[0]:
        with st.container(border=True, height=600):
            #st.image(image="cbi_logo.png")
            file = st.file_uploader("Import file", label_visibility='collapsed')
            read_right_file = False
            if (file == None):
                st.warning(":red[You have not chosen any file!!!]", icon="⚠️")
                st.warning(":red[Please select a file to proceed]", icon="⚠️")
            else:
                if ((file.name.split(".")[-1].lower() == "csv") or (file.name.split(".")[-1].lower() == "txt") or (file.name.split(".")[-1].lower() == "xlsx")):
                    @st.cache_resource()
                    def read_file(file):
                        if ((file.name.split(".")[-1].lower() == "csv") or (file.name.split(".")[-1].lower() == "txt")):
                            df = pd.read_csv(file, low_memory=False).fillna('')
                        else:
                            df = pd.read_excel(file).fillna('')
                        return df


                    df = read_file(file)
                    field_wise_file_name = st.selectbox("Select field wise file name:", list(df.columns), index=None,
                                                        placeholder="Select field...")
                    field_wise_folder_name = st.selectbox("Select field wise folder name(Optional):", list(df.columns),
                                                          index=None, placeholder="Select folder...")

                    read_right_file = True
                    button_make_field_wise_file = st.button("Make")
                    st.markdown("")
                    st.markdown("")
                    checkbox_full_data_view = st.checkbox(
                        f":green[Show full data (]:red[ It may take too much time!]:green[ )]")

                else:
                    st.warning(":red[You have chosen a wrong file type!!!]", icon="⚠️")

    with cols[1]:
        with st.container(border=True, height=600):
            if (read_right_file):
                # st.write("Showing first 1000 rows out of ", str(df.last_valid_index() + 1))
                if (checkbox_full_data_view):
                    st.write(
                        f":green[Showing] :red[{str(df.last_valid_index() + 1)}] :green[rows out of] :red[{str(df.last_valid_index() + 1)}]")
                    st.dataframe(df)
                else:
                    st.write(
                        f":green[Showing first] :red[1000] :green[rows out of] :red[{str(df.last_valid_index() + 1)}]")
                    st.dataframe(df.head(1000))

                if (button_make_field_wise_file):
                    if (field_wise_file_name == None):
                        st.warning(":red[Select Field Wise File Name from dropdown!!!]", icon="⚠️")

                    elif (field_wise_folder_name == None):
                        field_names_list = list(
                            df.pivot_table(index=[field_wise_file_name], aggfunc='count').index.values)

                        field_wise_file_path = os.getcwd().replace(chr(92), "/") + "/FIELD_WISE_FILEs/"
                        if (os.path.exists(field_wise_file_path)):
                            shutil.rmtree(field_wise_file_path, ignore_errors=True)
                        os.makedirs(field_wise_file_path)

                        field_count = 1
                        for field_name in field_names_list:
                            st.write(field_count, ") File making for: ", field_name)
                            if (field_name == ""):
                                # field_name = "blank_field"
                                df[df[field_wise_file_name] == field_name].to_csv(
                                    field_wise_file_path + "Blank_Field_Name" + ".csv", index=False)
                            else:
                                df[df[field_wise_file_name] == field_name].to_csv(
                                    field_wise_file_path + str(field_name) + ".csv", index=False)
                            field_count = field_count + 1
                            st.write("======== Files making done ========")

                    else:
                        folder_names_list = list(
                            df.pivot_table(index=[field_wise_folder_name], aggfunc='count').index.values)
                        path = os.getcwd().replace(chr(92), "/") + "/FIELD_WISE_FILEs_MAIN_FOLDER/"
                        if (os.path.exists(path)):
                            shutil.rmtree(path, ignore_errors=True)
                        os.makedirs(path)

                        for folder_name in folder_names_list:
                            st.write(folder_name)
                            if (folder_name == ""):
                                folder_path = path + "Blank_Folder_Name" + "/"
                            else:
                                folder_path = path + str(folder_name) + "/"

                            if (os.path.exists(folder_path)):
                                shutil.rmtree(folder_path, ignore_errors=True)
                            os.makedirs(folder_path)

                            field_wise_names_list = list(
                                df[df[field_wise_folder_name] == folder_name].pivot_table(index=[field_wise_file_name],
                                                                                          aggfunc='count').index.values)
                            field_count_under_folder = 1
                            for field_wise_name in field_wise_names_list:
                                # print(field_wise_name)
                                st.write(field_count_under_folder, ") File making for: ", field_wise_name)
                                if (field_wise_name == ""):
                                    df[df[field_wise_folder_name] == folder_name][
                                        df[field_wise_file_name] == field_wise_name].to_csv(
                                        folder_path + "Blank_Field_Name" + ".csv", index=False)
                                else:
                                    df[df[field_wise_folder_name] == folder_name][
                                        df[field_wise_file_name] == field_wise_name].to_csv(
                                        folder_path + str(field_wise_name) + ".csv", index=False)
                                field_count_under_folder = field_count_under_folder + 1
                            st.write("======== Files under Folder making done ========")
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

