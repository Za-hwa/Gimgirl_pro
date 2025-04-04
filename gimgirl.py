import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

# 상태 관리를 위한 세션 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = ""

# SQL 연결 및 엔진 생성
engine = create_engine('sqlite:///gimgirl1.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# 기존 모델 정의
class Gimgirl(Base):
    __tablename__ = 'gimgirs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ten = Column(Integer)  # 5만원으로 사용
    twe = Column(Integer)  # 10만원으로 사용
    tre = Column(Integer)  # 20만원으로 사용
    fiv = Column(Integer)  # 30만원으로 사용
    fft = Column(Integer)  # 50만원으로 사용

# 학생 인증 모델 추가
class StudentAuth(Base):
    __tablename__ = 'student_auth'
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True)
    has_voted = Column(Boolean, default=True)

# 테이블 구조 업데이트 (새 열 추가)
try:
    engine.execute('ALTER TABLE gimgirs ADD COLUMN fiv INTEGER DEFAULT 0')
    engine.execute('ALTER TABLE gimgirs ADD COLUMN fft INTEGER DEFAULT 0')
except:
    pass  # 이미 열이 존재하면 무시

# 테이블 생성
Base.metadata.create_all(engine)

# 초기 데이터 추가 (한 번만 추가해야 함)
if session.query(Gimgirl).count() == 0:
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

def register_student_id(student_id):
    """학번을 데이터베이스에 등록"""
    new_student = StudentAuth(student_id=student_id)
    session.add(new_student)
    session.commit()

def login_page():
    """학번 인증 페이지"""
    st.header("2025 김해여고 펀딩 사이트")
    st.subheader("학번 인증")
    
    with st.form("student_auth_form"):
        student_id = st.text_input("학번을 입력하세요 (예: 20250101)")
        submitted = st.form_submit_button("인증하기")
        
        if submitted:
            # 학번 형식 검증 (6자리 또는 8자리 숫자)
            if not student_id.isdigit() or (len(student_id) != 6 and len(student_id) != 8):
                st.error("올바른 학번 형식이 아닙니다. 6자리 또는 8자리 숫자로 입력해주세요.")
                return
                
            # 중복 확인
            if check_student_id(student_id):
                st.error("이미 투표한 학번입니다. 다른 학번으로 시도해주세요.")
                return
                
            # 인증 성공
            register_student_id(student_id)
            st.session_state.authenticated = True
            st.session_state.student_id = student_id
            st.success("인증되었습니다!")
            st.experimental_rerun()

def main_app():
    """메인 펀딩 애플리케이션"""
    st.header("2025 김해여고 펀딩 사이트")
    st.write(f"학번: {st.session_state.student_id}")

    page = st.selectbox("페이지를 선택하세요", ["2학년 1반", "2학년 2반", "2학년 3반", "2학년 4반", "2학년 5반", 
                                        "2학년 6반", "2학년 7반", "2학년 8반", "1학년 1반", "1학년 2반", 
                                        "1학년 3반", "1학년 4반", "1학년 5반", "1학년 6반", "1학년 7반", "1학년 8반", "관리자용"])

    # 각 반별 페이지 - 모든 반에 동일한 업데이트 적용
    if page != "관리자용":
        class_name = page.replace("학년 ", "-")
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            st.image('fund.png')
        
        with st.form(key=f'funding_form_{class_name}'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", 
                                ["5만원", "10만원", "20만원", "30만원", "50만원"], 
                                index=1)  # 기본값 10만원
            submit_button = st.form_submit_button(label="제출하기")
            
            if submit_button:
                update_donation(class_name, donation)
                st.success("제출되었습니다")
                # 투표 후 로그아웃 옵션
                if st.button("로그아웃"):
                    st.session_state.authenticated = False
                    st.session_state.student_id = ""
                    st.experimental_rerun()
                
    # 관리자용 페이지
    else:
        password = st.text_input("비밀번호를 입력하세요", type="password")

        if password == "2345":
            # 통계 탭 나누기
            tab1, tab2 = st.tabs(["학급별 모금액", "참여 학생 목록"])
            
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
                        st.write(f"{class_name.replace('-', '학년 ')}반 총합: {total}만원")
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
            
            with tab2:
                # 참여 학생 목록 (학번만 표시)
                students = session.query(StudentAuth).all()
                student_ids = [s.student_id for s in students]
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
                        session.query(StudentAuth).delete()
                        session.commit()
                        st.success("학생 참여 데이터가 초기화되었습니다.")
                        st.experimental_rerun()
        else:
            st.warning("비밀번호가 틀렸습니다.")

def main():
    # 인증 여부에 따라 다른 페이지 표시
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()
        
        # 로그아웃 버튼
        if st.sidebar.button("로그아웃"):
            st.session_state.authenticated = False
            st.session_state.student_id = ""
            st.experimental_rerun()

if __name__ == '__main__':
    main()
