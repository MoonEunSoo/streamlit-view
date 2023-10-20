# app.py

import streamlit as st
from datetime import datetime, timedelta

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

st.title("시간표 관리 웹사이트")

# 세션 상태에 timetable 초기화
if 'timetable' not in st.session_state:
    st.session_state.timetable = []

menu = st.sidebar.radio("선택하세요", ["시간표 보기", "시간표에 추가하기"])

if menu == "시간표 보기":
    display_timetable()
elif menu == "시간표에 추가하기":
    add_to_timetable()
