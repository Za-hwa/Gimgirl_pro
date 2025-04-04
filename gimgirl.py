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
    st.header("2025 김해여고 펀딩 사이트")
    st.subheader("학번 인증")
    
    with st.form("student_auth_form"):
        student_id = st.text_input("학번을 입력하세요 (예: 2712)")
        submitted = st.form_submit_button("인증하기")
        
        if submitted:
            # 관리자 로그인
            if student_id == "****":
                password = st.text_input("비밀번호를 입력하세요", type="password")
                if password == "2345":
                    st.session_state.authenticated = True
                    st.session_state.is_admin = True
                    st.session_state.student_id = "관리자"
                    st.success("관리자로 로그인했습니다!")
                    st.rerun()  # experimental_rerun() 대신 rerun() 사용
                else:
                    st.error("비밀번호가 올바르지 않습니다.")
                return
            
            # 학번 형식 검증 (4자리 숫자)
            if not student_id.isdigit() or len(student_id) != 4:
                st.error("올바른 학번 형식이 아닙니다.")
                return

            # 유효한 학번인지 확인
            if not is_valid_student_id(student_id):
                st.error("학번이 유효하지 않습니다. 올바른 학번인지 확인해주세요.")
                return

            # 중복 확인
            if check_student_id(student_id):
                st.error("이미 투표한 학번입니다.")
                return
                
            # 일반 학생 인증 성공
            register_student_id(student_id)
            st.session_state.authenticated = True
            st.session_state.student_id = student_id
            st.success("인증되었습니다!")
            st.rerun()  # experimental_rerun() 대신 rerun() 사용

def admin_page():
    """관리자 페이지"""
    st.header("관리자 페이지")
    
    # 관리자 기능 탭
    tab1, tab2, tab3 = st.tabs(["학급별 모금액", "참여 학생 목록", "학번 관리"])
    
    with tab1:
        classes = []
        for grade in [1, 2]:
            for class_num in range(1, 9):
                class_name = f"{grade}-{class_num}"
                classes.append(class_name)
        
        # 각 반별 금액 계산
        data = []
        for class_name in classes:
            result = session.query(Gimgirl).filter(Gimgirl.name == class_name).first()
            if result:
                total = (result.ten * 5) + (result.twe * 10) + (result.tre * 20) + (result.fiv * 30) + (result.fft * 50)
                data.append({
                    "반": class_name.replace('-', '학년 ') + '반',
                    "5만원": result.ten,
                    "10만원": result.twe,
                    "20만원": result.tre,
                    "30만원": result.fiv,
                    "50만원": result.fft,
                    "총액(만원)": total
                })
        
        # 데이터프레임으로 표시
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            
            # 각 반별 합계 출력
            for item in data:
                st.write(f"{item['반']} 총합: {item['총액(만원)']}만원")
    
    with tab2:
        # 참여 학생 목록 (학번만 표시)
        students = session.query(StudentAuth).all()
        student_ids = [s.student_id for s in students if s.student_id != "관리자"]
        st.write(f"총 {len(student_ids)}명 참여")
        st.dataframe(pd.DataFrame({"학번": student_ids}))
        
        # 학생 목록 다운로드 버튼
        student_df = pd.DataFrame({"학번": student_ids})
        csv = student_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="참여 학생 목록 다운로드 (CSV)",
            data=csv,
            file_name='student_participants.csv',
            mime='text/csv',
        )
        
        # 학생 데이터 초기화 버튼
        if st.button("참여 학생 데이터 초기화 (주의: 모든 기록이 삭제됩니다)"):
            confirm = st.text_input("확인을 위해 '초기화'를 입력하세요")
            if confirm == "초기화":
                # 관리자 계정 제외하고 삭제
                session.query(StudentAuth).filter(StudentAuth.student_id != "관리자").delete()
                session.commit()
                st.success("학생 참여 데이터가 초기화되었습니다.")
                st.rerun()  # experimental_rerun() 대신 rerun() 사용
    
    with tab3:
        # 학번 관리 탭에서 엑셀 업로드 기능
        upload_excel_student_ids()
        
        # 현재 등록된 유효한 학번 보기
        st.subheader("현재 등록된 유효한 학번")
        valid_ids = session.query(ValidStudentID).all()
        valid_id_list = [v.student_id for v in valid_ids]
        
        st.write(f"총 {len(valid_id_list)}개의 유효한 학번이 등록되어 있습니다.")
        
        show_ids = st.checkbox("학번 목록 보기")
        if show_ids and valid_id_list:
            st.dataframe(pd.DataFrame({"유효한 학번": valid_id_list}))
            
            # 유효한 학번 목록 다운로드
            valid_ids_df = pd.DataFrame({"학번": valid_id_list})
            csv = valid_ids_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="유효한 학번 목록 다운로드 (CSV)",
                data=csv,
                file_name='valid_student_ids.csv',
                mime='text/csv',
            )
        
        # 유효한 학번 초기화 버튼
        if st.button("유효한 학번 목록 초기화 (주의: 모든 유효한 학번이 삭제됩니다)"):
            confirm = st.text_input("확인을 위해 '학번초기화'를 입력하세요")
            if confirm == "학번초기화":
                session.query(ValidStudentID).delete()
                session.commit()
                st.session_state.valid_student_ids = []
                st.success("유효한 학번 목록이 초기화되었습니다.")
                st.rerun()  # experimental_rerun() 대신 rerun() 사용

def student_app():
    """학생 펀딩 애플리케이션"""
    st.header("2025 김해여고 펀딩 사이트")
    st.write(f"학번: {st.session_state.student_id}")

    page = st.selectbox("페이지를 선택하세요", ["2학년 1반", "2학년 2반", "2학년 3반", "2학년 4반", "2학년 5반", 
                                        "2학년 6반", "2학년 7반", "2학년 8반", "1학년 1반", "1학년 2반", 
                                        "1학년 3반", "1학년 4반", "1학년 5반", "1학년 6반", "1학년 7반", "1학년 8반"])

    class_name = page.replace("학년 ", "-")
        
    col1, col2, col3 = st.columns([1, 3, 1])
        
    with col2:
        try:
            st.image('fund.png')
        except:
            st.warning("이미지 파일 'fund.png'를 찾을 수 없습니다.")
        
    with st.form(key=f'funding_form_{class_name}'):
        donation = st.radio("펀딩을 얼마할 지 선택해주세요", 
                            ["5만원", "10만원", "20만원", "30만원", "50만원"], 
                            index=1)  # 기본값 10만원
        submit_button = st.form_submit_button(label="제출하기")
            
        if submit_button:
            update_donation(class_name, donation)
            st.success("제출되었습니다")

def main():
    # 인증 여부에 따라 다른 페이지 표시
    if not st.session_state.authenticated:
        login_page()
    else:
        # 관리자/학생 구분
        if st.session_state.is_admin:
            admin_page()
        else:
            student_app()
        
        # 로그아웃 버튼
        if st.sidebar.button("로그아웃"):
            st.session_state.authenticated = False
            st.session_state.is_admin = False
            st.session_state.student_id = ""
            st.rerun()  # experimental_rerun() 대신 rerun() 사용

if __name__ == '__main__':
    main()
