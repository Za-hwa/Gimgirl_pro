import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import os

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

# 상태 관리를 위한 세션 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'valid_student_ids' not in st.session_state:
    st.session_state.valid_student_ids = []

# 학급 번호와 이름 매핑 (이제 숫자만 표시)
def get_class_name_from_number(class_num):
    """숫자만 반환"""
    return f"{class_num}"

def get_original_class_code(class_num):
    """숫자를 원래 형식인 '2-1' 형식으로 변환 (데이터베이스 호환성)"""
    if 1 <= class_num <= 8:
        return f"2-{class_num}"
    elif 9 <= class_num <= 16:
        return f"1-{class_num-8}"
    else:
        return str(class_num)

def get_db_session():
    """데이터베이스 세션을 생성하고 반환합니다"""
    return Session()

def update_donation(class_code, donation_amount):
    """금액에 따라 적절한 열을 업데이트합니다"""
    session = get_db_session()
    try:
        if donation_amount == "5만원":
            session.query(Gimgirl).filter(Gimgirl.name == class_code).update({Gimgirl.ten: Gimgirl.ten + 1})
        elif donation_amount == "10만원":
            session.query(Gimgirl).filter(Gimgirl.name == class_code).update({Gimgirl.twe: Gimgirl.twe + 1})
        elif donation_amount == "20만원":
            session.query(Gimgirl).filter(Gimgirl.name == class_code).update({Gimgirl.tre: Gimgirl.tre + 1})
        elif donation_amount == "30만원":
            session.query(Gimgirl).filter(Gimgirl.name == class_code).update({Gimgirl.fiv: Gimgirl.fiv + 1})
        elif donation_amount == "50만원":
            session.query(Gimgirl).filter(Gimgirl.name == class_code).update({Gimgirl.fft: Gimgirl.fft + 1})
        session.commit()
        return True
    except Exception as e:
        st.error(f"데이터 저장 중 오류가 발생했습니다: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()

def check_student_id(student_id):
    """학번이 이미 사용되었는지 확인"""
    session = get_db_session()
    try:
        result = session.query(StudentAuth).filter(StudentAuth.student_id == student_id).first()
        return result is not None
    finally:
        session.close()

def is_valid_student_id(student_id):
    """학번이 유효한지 확인 (엑셀에서 로드된 학번인지)"""
    session = get_db_session()
    try:
        result = session.query(ValidStudentID).filter(ValidStudentID.student_id == student_id).first()
        return result is not None
    finally:
        session.close()

def register_student_id(student_id):
    """학번을 데이터베이스에 등록"""
    session = get_db_session()
    try:
        new_student = StudentAuth(student_id=student_id)
        session.add(new_student)
        session.commit()
        return True
    except Exception as e:
        st.error(f"학번 등록 중 오류가 발생했습니다: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()

def initialize_data():
    """초기 데이터가 없으면 추가합니다"""
    session = get_db_session()
    try:
        if session.query(Gimgirl).count() == 0:
            classes = []
            # 2학년 1-8반은 1-8번, 1학년 1-8반은 9-16번으로 변환하여 저장
            for i in range(1, 17):
                class_code = get_original_class_code(i)
                classes.append(Gimgirl(name=class_code, ten=0, twe=0, tre=0, fiv=0, fft=0))
            
            session.add_all(classes)
            session.commit()
            st.success("초기 데이터가 성공적으로 생성되었습니다.")
    except Exception as e:
        st.error(f"초기 데이터 생성 중 오류가 발생했습니다: {str(e)}")
        session.rollback()
    finally:
        session.close()

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
                session = get_db_session()
                try:
                    # 기존 데이터 초기화
                    session.query(ValidStudentID).delete()
                    
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
                    st.error(f"데이터베이스 저장 중 오류가 발생했습니다: {str(e)}")
                    session.rollback()
                finally:
                    session.close()
        
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
                    st.rerun()
                else:
                    st.error("비밀번호가 올바르지 않습니다.")
                return
                
            # 특별 테스트용 학번 (99999) - 중복 투표 허용
            if student_id == "99999":
                st.session_state.authenticated = True
                st.session_state.student_id = "테스트유저"
                st.success("테스트 모드로 인증되었습니다!")
                st.rerun()
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
            if register_student_id(student_id):
                st.session_state.authenticated = True
                st.session_state.student_id = student_id
                st.success("인증되었습니다!")
                st.rerun()

def admin_page():
    """관리자 페이지"""
    st.header("관리자 페이지")
    
    # 관리자 기능 탭
    tab1, tab2, tab3 = st.tabs(["학급별 모금액", "참여 학생 목록", "학번 관리"])
    
    with tab1:
        # 1~16까지의 학급 번호
        class_numbers = list(range(1, 17))
        
        # 각 반별 금액 계산
        session = get_db_session()
        try:
            data = []
            for class_num in class_numbers:
                class_code = get_original_class_code(class_num)
                result = session.query(Gimgirl).filter(Gimgirl.name == class_code).first()
                if result:
                    total = (result.ten * 5) + (result.twe * 10) + (result.tre * 20) + (result.fiv * 30) + (result.fft * 50)
                    data.append({
                        "반 번호": class_num,
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
                    st.write(f"{item['반 번호']}: {item['총액(만원)']}만원")
        finally:
            session.close()
    
    with tab2:
        # 참여 학생 목록 (학번만 표시)
        session = get_db_session()
        try:
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
        finally:
            session.close()
        
        # 학생 데이터 초기화 버튼
        if st.button("참여 학생 데이터 초기화 (주의: 모든 기록이 삭제됩니다)"):
            confirm = st.text_input("확인을 위해 '초기화'를 입력하세요")
            if confirm == "초기화":
                session = get_db_session()
                try:
                    # 관리자 계정 제외하고 삭제
                    session.query(StudentAuth).filter(StudentAuth.student_id != "관리자").delete()
                    session.commit()
                    st.success("학생 참여 데이터가 초기화되었습니다.")
                    st.rerun()
                except Exception as e:
                    st.error(f"데이터 초기화 중 오류가 발생했습니다: {str(e)}")
                    session.rollback()
                finally:
                    session.close()
    
    with tab3:
        # 학번 관리 탭에서 엑셀 업로드 기능
        upload_excel_student_ids()
        
        # 현재 등록된 유효한 학번 보기
        st.subheader("현재 등록된 유효한 학번")
        session = get_db_session()
        try:
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
        finally:
            session.close()
        
        # 유효한 학번 초기화 버튼
        if st.button("유효한 학번 목록 초기화 (주의: 모든 유효한 학번이 삭제됩니다)"):
            confirm = st.text_input("확인을 위해 '학번초기화'를 입력하세요")
            if confirm == "학번초기화":
                session = get_db_session()
                try:
                    session.query(ValidStudentID).delete()
                    session.commit()
                    st.session_state.valid_student_ids = []
                    st.success("유효한 학번 목록이 초기화되었습니다.")
                    st.rerun()
                except Exception as e:
                    st.error(f"데이터 초기화 중 오류가 발생했습니다: {str(e)}")
                    session.rollback()
                finally:
                    session.close()

def get_class_image(class_num):
    """학급 번호에 맞는 이미지 파일명을 반환합니다"""
    # class_num은 1부터 16까지의 정수
    image_name = f"{class_num}.png"
    
    # 이미지 파일이 존재하는지 확인
    if os.path.exists(image_name):
        return image_name
    else:
        # 없으면 기본 이미지 사용
        return "fund.png"

def student_app():
    """학생 펀딩 애플리케이션"""
    st.header("2025 김해여고 펀딩 사이트")
    st.write(f"학번: {st.session_state.student_id}")

    # 1부터 16까지의 반 선택
    class_numbers = list(range(1, 17))
    class_options = [f"{num}" for num in class_numbers]
    
    selected_option = st.selectbox("번호를 선택하세요", class_options)
    
    # 선택된 옵션에서 반 번호 추출 
    selected_class_num = int(selected_option)
    
    # 원래 코드 형식 (데이터베이스와 일치)
    class_code = get_original_class_code(selected_class_num)
        
    col1, col2, col3 = st.columns([1, 3, 1])
        
    with col2:
        # 해당 학급에 맞는 이미지 표시
        image_path = get_class_image(selected_class_num)
        try:
            st.image(image_path)
            st.caption(f"현재 선택된 번호: {selected_class_num}")
        except Exception as e:
            st.warning(f"이미지 파일 '{image_path}'를 표시할 수 없습니다. 오류: {str(e)}")
        
    with st.form(key=f'funding_form_{selected_class_num}'):
        donation = st.radio("펀딩을 얼마할 지 선택해주세요", 
                            ["5만원", "10만원", "20만원", "30만원", "50만원"], 
                            index=1)  # 기본값 10만원
        submit_button = st.form_submit_button(label="제출하기")
            
        if submit_button:
            if update_donation(class_code, donation):
                st.success(f"{selected_class_num}번에 {donation} 펀딩이 성공적으로 제출되었습니다.")
            else:
                st.error("펀딩 제출 중 오류가 발생했습니다. 다시 시도해주세요.")

def main():
    # 초기 데이터 확인 및 생성
    initialize_data()
    
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
            st.rerun()

if __name__ == '__main__':
    main()
