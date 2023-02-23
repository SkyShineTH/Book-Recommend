import streamlit as st
import shutil
import pandas as pd
from new_sys import *

ratings_path="data_template/Ratings.csv"
users_path="data_template/Users.csv"
Books_path = 'data_template/Books.csv'
st.markdown(
    f"""
       <style>
       .css-1n76uvr{{
        background-image: url("https://wallpaperaccess.com/full/2825710.gif");
        background-size:     cover;                  
        background-repeat:   no-repeat;
        background-position: center center;
        border-radius:5px;
        display:flex;
        flex-direction:column;
        justify-content:space-around;
        padding:20px;

        box-shadow: 10px 10px 5px 0px rgba(0,0,0,0.75);
        -webkit-box-shadow: 10px 10px 5px 0px rgba(0,0,0,0.75);
        -moz-box-shadow: 10px 10px 5px 0px rgba(0,0,0,0.75);
        }}
        img:hover{{
        -webkit-transform: scale(1.2);
        -ms-transform: scale(1.2);
        transform: scale(1.2);
        transition: 1s ease;
        }}
        .css-1b0udgb{{
            color:white;
        }}
        </style>
       """,
    unsafe_allow_html=True
)
st.markdown("""<h1 classname="name-title" style="color:White;text-align: center;">Book Recommend<h1/>""",unsafe_allow_html=True)
first,second, third,fourth = st.columns(4)
def Generate():
    src_file="data_template/Books.csv"
    st.markdown("""<h2 style="color:White;">Generate Page<h2/>""",unsafe_allow_html=True)
    left,right = st.columns(2)
    title = right.text_input('', 'ชื่อไฟล์',label_visibility="collapsed")
    left.markdown("""<p style="color:White">กรอกชื่อไฟล์ที่ต้องการสร้าง<p/>""",unsafe_allow_html=True)
    left.markdown(f"""<p style="color:White">คุณต้องการสร้างไฟล์ชื่อ: {title} ใช่ไหม<p/>""",unsafe_allow_html=True) 
    csv = pd.read_csv(Books_path).to_csv()
    right.download_button(label="Create",data=csv,file_name=f"{title}.csv",mime='text/csv')

def Load():
    st.markdown("""<h2 style="color:White;">Load Page<h2/>""",unsafe_allow_html=True)
    left,right = st.columns(2)
    with st.container():
        book_up = left.file_uploader("Choose a file",label_visibility="collapsed",key="book_upload")
        btn_book_ok = right.button("OK",key="btn_book_ok")
        btn_current = right.button("Use Current file",key="current_file_btn")
        if btn_book_ok:
            if book_up is not None:
                with open(f"user_data/{book_up.name}", "wb") as f:
                    shutil.copyfileobj(book_up, f)
                    Books_path = f"user_data/{book_up.name}"
                    dataframe = pd.read_csv(f"user_data/{book_up.name}")
                    st.write(dataframe)
                    st.markdown("""<h2 style="color:White;">ได้ทำการเซ็ทไฟล์เสร็จแล้วไปที่หน้า Train ได้เลย<h2/>""",unsafe_allow_html=True)

            else:
                st.markdown("""<h2 style="color:White;">กรุณาอัพไฟล์หรือกด Use Current file<h2/>""",unsafe_allow_html=True)
        if btn_current:
            Books_path = 'data_template/Books.csv'
            dataframe = pd.read_csv(Books_path)
            st.write(dataframe)
            st.markdown("""<h2 style="color:White;">ได้ทำการเซ็ทไฟล์เสร็จแล้วไปที่หน้า Train ได้เลย<h2/>""",unsafe_allow_html=True)

def Train():
    st.markdown("""<h2 style="color:White;">Train Page<h2/>""",unsafe_allow_html=True)
    left,right = st.columns(2)
    with st.container():
        book_train = left.file_uploader("Choose a file",label_visibility="collapsed",key="book_upload")
        btn_book_ok = right.button("Train",key="btn_book_train")
        btn_current = right.button("Use Current file",key="current_file_btn")
        if btn_book_ok:
            if book_train is not None:
                data = pd.read_csv(f"user_data/{book_train.name}")
                st.dataframe(data)
                st.markdown("""<h2 style="color:White;">Train สำเร็จ<h2/>""",unsafe_allow_html=True)

            else:
                st.markdown("""<h2 style="color:White;">กรุณาอัพไฟล์หรือกด Use Current file<h2/>""",unsafe_allow_html=True)
        if btn_current:
            dataframe = pd.read_csv(Books_path)
            st.write(dataframe)
            st.markdown("""<h2 style="color:White;">เสร็จเรียบร้อย<h2/>""",unsafe_allow_html=True)

def Predict():
    st.markdown("""<h2 style="color:White;">Predict Page<h2/>""",unsafe_allow_html=True)
    left,right = st.columns(2)
    search = left.text_input("","Book Title or Book Year or Rating or Author",label_visibility="collapsed")
    if right.button('Show as table'):  
        with st.container():
            if "top" in search or  'popular' in search:
                text_search = search.split(" ")
                st.write(popular_books(ratings_path,Books_path,int(text_search[1])))
            else:
                filter_book = search_books(search,ratings_path,Books_path)
                dataframe = pd.read_csv(filter_book)
                st.write(dataframe)

    if right.button('Show as picture'):
        with st.container():
            if "top" in search or  'popular' in search:
                text_search = search.split(" ")
                data_callback = popular_books(ratings_path,Books_path,int(text_search[1]),image_show=True)
                image_links = data_callback.loc[:, 'Image-URL-M']
                book_title = data_callback.loc[:, 'Book-Title']
                book_title_list = book_title.tolist()
                image_links_list = image_links.tolist()
                columns = st.columns(3)
                for i in range(len(image_links_list)):
                    card = columns[i % 3]
                    card.image(image_links_list[i], caption=book_title_list[i],width=100)
            
            else:
                columns = st.columns(3)
                filter_book = search_books(search,ratings_path,Books_path)
                for i in range(len(filter_book)):
                    card = columns[i % 3]
                    card.image(filter_book[i]["image_url"])
                    card.markdown(f"""<p style="color:White;">Title:{filter_book[i]['title']}<p/>""",unsafe_allow_html=True)
                    card.markdown(f"""<p style="color:White;">Rating:{filter_book[i]['rating']}<p/>""",unsafe_allow_html=True)

pages = {
    "Generate": Generate,
    "Load": Load,
    "Train": Train,
    "Predict": Predict
}


if 'selection' not in st.session_state:
    st.session_state.selection = 'Generate'

page = pages[st.session_state.selection]

if first.button('Generate'):
    st.session_state.selection = 'Generate'
if second.button('Load'):
    st.session_state.selection = 'Load'
if third.button('Train'):
    st.session_state.selection = 'Train'
if fourth.button('Predict'):
    st.session_state.selection = 'Predict'

if st.session_state.selection != page.__name__:
    page = pages[st.session_state.selection]

page()