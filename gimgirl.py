import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import os

# 상태 관리를 위한 세션 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'valid_student_ids' not in st.session_state:
    st.session_state.valid_student_ids = []

# 데이터베이스 파일 경로 확인
db_path = 'gimgirl1.db'
db_exists = os.path.exists(db_path)

# SQL 연결 및 엔진 생성
engine = create_engine(f'sqlite:///{db_path}')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 기존 모델 정의
class Gimgirl(Base):
    __tablename__ = 'gimgirs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ten = Column(Integer, default=0)  # 5만원으로 사용
    twe = Column(Integer, default=0)  # 10만원으로 사용
    tre = Column(Integer, default=0)  # 20만원으로 사용
    fiv = Column(Integer, default=0)  # 30만원으로 사용
    fft = Column(Integer, default=0)  # 50만원으로 사용

# 학생 인증 모델 추가
class StudentAuth(Base):
    __tablename__ = 'student_auth'
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True)
    has_voted = Column(Boolean, default=True)

# 유효한 학번 목록 모델 추가
class ValidStudentID(Base):
    __tablename__ = 'valid_student_ids'
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True)

# 테이블 생성
Base.metadata.create_all(engine)

# 세션 생성 (테이블 생성 이후에 세션 생성)
session = Session()

# 초기 데이터 추가 (한 번만 추가해야 함)
if not db_exists or session.query(Gimgirl).count() == 0:
    classes = []
    for grade in [1, 2]:
        for class_num in range(1, 9):
            classes.append(Gimgirl(name=f"{grade}-{class_num}", ten=0, twe=0, tre=0, fiv=0, fft=0))
    
    session.add_all(classes)
    session.commit()

def update_donation(class_name, donation_amount):
    """금액에 따라 적절한 열을 업데이트합니다"""
    if donation_amount == "5만원":
        session.query(Gimgirl).filter(Gimgirl.name == class_name).update({Gimgirl.ten: Gimgirl.ten + 1})
    elif donation_amount == "10만원":
        session.query(Gimgirl).filter(Gimgirl.name == class_name).update({Gimgirl.twe: Gimgirl.twe + 1})
    elif donation_amount == "20만원":
        session.query(Gimgirl).filter(Gimgirl.name == class_name).update({Gimgirl.tre: Gimgirl.tre + 1})
    elif donation_amount == "30만원":
        session.query(Gimgirl).filter(Gimgirl.name == class_name).update({Gimgirl.fiv: Gimgirl.fiv + 1})
    elif donation_amount == "50만원":
        session.query(Gimgirl).filter(Gimgirl.name == class_name).update({Gimgirl.fft: Gimgirl.fft + 1})
    session.commit()

def check_student_id(student_id):
    """학번이 이미 사용되었는지 확인"""
    result = session.query(StudentAuth).filter(StudentAuth.student_id == student_id).first()
    return result is not None

def is_valid_student_id(student_id):
    """학번이 유효한지 확인 (엑셀에서 로드된 학번인지)"""
    result = session.query(ValidStudentID).filter(ValidStudentID.student_id == student_id).first()
    return result is not None

def register_student_id(student_id):
    """학번을 데이터베이스에 등록"""
    new_student = StudentAuth(student_id=student_id)
    session.add(new_student)
    session.commit()

def upload_excel_student_ids():
    """엑셀 파일에서 유효한 학번 목록을 업로드합니다"""
    st.subheader("유효한 학번 목록 업로드")
    uploaded_file = st.file_uploader("학번이 포함된 엑셀 파일을 업로드하세요", type=['xlsx', 'xls'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        column_name = st.text_input("학번이 있는 열 이름", "학번")
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            # 지정된 열이 있는지 확인
            if column_name not in df.columns:
                st.error(f"'{column_name}' 열이 엑셀 파일에 없습니다. 파일을 확인해주세요.")
                st.write("사용 가능한 열 이름:")
                st.write(df.columns.tolist())
                return
            
            # 학번 추출 및 문자열로 변환
            student_ids = df[column_name].astype(str).tolist()
            
            with col2:
                preview_option = st.selectbox("미리보기 옵션", ["처음 10개", "모두 보기"])
                
                if preview_option == "처음 10개":
                    st.write("학번 미리보기 (처음 10개):")
                    st.write(student_ids[:10])
                else:
                    st.write("모든 학번:")
                    st.write(student_ids)
            
            if st.button("학번 목록 등록하기"):
                # 기존 데이터 초기화
                session.query(ValidStudentID).delete()
                session.commit()
                
                # 새 학번 추가
                valid_ids = []
                for sid in student_ids:
                    if pd.notna(sid) and sid.strip():  # 빈 값이나 NaN 제외
                        valid_ids.append(ValidStudentID(student_id=sid.strip()))
                
                if valid_ids:
                    session.add_all(valid_ids)
                    session.commit()
                    st.success(f"{len(valid_ids)}개의 학번이 성공적으로 등록되었습니다!")
                    
                    # 세션 상태에 유효한 학번 목록 저장
                    st.session_state.valid_student_ids = [v.student_id for v in valid_ids]
                else:
                    st.warning("등록할 유효한 학번이 없습니다.")
        
        except Exception as e:
            st.error(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

def login_page():
    """학번 인증 페이지"""
    st.header("2025
