# app.py

import streamlit as st
from datetime import datetime, timedelta
from datetime import datetime
import os


def display_timetable():
    """시간표 전체를 화면에 표시하고 삭제 버튼 추가"""
    for idx, item in enumerate(st.session_state.timetable):
        row = f"{item['day']} {item['start_time']} ~ {item['end_time']}: {item['subject']}"
        cols = st.columns([0.8, 0.15, 0.05])
        
        cols[0].write(row)
        
        with cols[1]:
            if st.button("삭제", key=f"delete_{idx}"):
                st.session_state.timetable.pop(idx)
                st.success(f"'{row}' 항목이 삭제되었습니다!")
                st.experimental_rerun()


def add_to_timetable():
    """새로운 항목을 시간표에 추가하고 화면에 표시"""
    day = st.selectbox("요일 선택", ["월", "화", "수", "목", "금", "토", "일"])
    start_time = st.selectbox("시작 시간", ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"])
    duration = st.selectbox("수업 시간", [1, 2, 3, 4, 5])
    
    start_datetime = datetime.strptime(start_time, '%I%p')
    end_time = (start_datetime + timedelta(hours=duration)).time()

    subject = st.text_input("과목 혹은 활동 이름")

    if st.button("추가하기"):
        new_item = {
            'day': day,
            'start_time': start_datetime.time(),
            'end_time': end_time,
            'subject': subject
        }
        st.session_state.timetable.append(new_item)
        st.success("시간표에 추가되었습니다!")


def record_class_content():
    """수업 내용을 기록하는 페이지"""
    subject_name = st.text_input("수업 과목")
    class_content = st.text_area("수업내용")

    if st.button("저장"):
        new_content = {
            'subject': subject_name,
            'content': class_content,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.class_contents.append(new_content)
        st.success("수업 내용이 저장되었습니다!")
           # 파일에 저장 버튼 추가
# ... (나머지 코드는 그대로 유지)

def save_class_contents_to_txt():
    """세션의 수업 내용을 txt 파일로 저장하는 함수"""
    with open('class_contents.txt', 'w', encoding='utf-8') as file:
        for item in st.session_state.class_contents:
            file.write("수업 이름: " + item['subject'] + "\n")
            file.write("날짜: " + item['date'] + "\n")
            file.write("수업 내용:\n" + item['content'] + "\n")
            file.write("-" * 50 + "\n")  # 구분선

def view_class_content():
    """저장된 수업 내용을 보는 페이지"""
    subjects_with_date = ["{} - {}".format(item['subject'], item['date']) for item in st.session_state.class_contents]
    selected = st.selectbox("수업과 날짜 선택", subjects_with_date)

    for item in st.session_state.class_contents:
        if "{} - {}".format(item['subject'], item['date']) == selected:
            st.write("수업 이름:", item['subject'])
            st.write("수업 내용:")
            st.write(item['content'])

    # txt 파일로 저장하기 버튼 추가 (키 추가)
    if st.button("txt 파일로 저장하기", key="save_to_txt"):
        save_class_contents_to_txt()
        st.success("class_contents.txt 파일로 저장되었습니다!")





st.title("시간표 관리 웹사이트")

# 세션 상태에 timetable 및 class_contents 초기화
if 'timetable' not in st.session_state:
    st.session_state.timetable = []

if 'class_contents' not in st.session_state:
    st.session_state.class_contents = []

menu = st.sidebar.radio("선택하세요", ["시간표 보기", "시간표에 추가하기", "수업내용 기록", "수업내용 기록 보기"])

if menu == "시간표 보기":
    display_timetable()
elif menu == "시간표에 추가하기":
    add_to_timetable()
elif menu == "수업내용 기록":
    record_class_content()
elif menu == "수업내용 기록 보기":
    view_class_content()