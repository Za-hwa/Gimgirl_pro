import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQL 연결 및 엔진 생성
engine = create_engine('sqlite:///gimgirl1.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# 모델 정의
class Gimgirl(Base):
    __tablename__ = 'gimgirs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ten = Column(Integer)
    twe = Column(Integer)
    tre = Column(Integer)

# 테이블 생성 (이미 생성된 경우에는 다시 생성되지 않음)
Base.metadata.create_all(engine)

# 데이터 추가 (한 번만 추가해야 함)
if session.query(Gimgirl).count() == 0:
    ex1 = Gimgirl(name="예제1", ten=0, twe=0, tre=0)
    ex2 = Gimgirl(name="예제2", ten=0, twe=0, tre=0)
    ex3 = Gimgirl(name="예제3", ten=0, twe=0, tre=0)

    session.add(ex1)
    session.add(ex2)
    session.add(ex3)
    session.commit()

def main():
    st.title("김해여고 펀딩 사이트")
    st.header("2025 김해여고 펀딩 사이트")
    st.markdown("===")

    page = st.selectbox("페이지를 선택하세요", ["예제1", "예제2", "관리자용"])

    # 예제1 페이지
    if page == "예제1":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1'):
            donation = st.radio("질문:", [10, 20, 30], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == 10:
                    session.query(Gimgirl).filter(Gimgirl.name == "예제1").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == 20:
                    session.query(Gimgirl).filter(Gimgirl.name == "예제1").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == 30:
                    session.query(Gimgirl).filter(Gimgirl.name == "예제1").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.toast("예제1 제출되었습니다")
        


    # 예제2 페이지
    if page == "예제2":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form2'):
            donation = st.radio("질문:", [10, 20, 30], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == 10:
                    session.query(Gimgirl).filter(Gimgirl.name == "예제2").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == 20:
                    session.query(Gimgirl).filter(Gimgirl.name == "예제2").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == 30:
                    session.query(Gimgirl).filter(Gimgirl.name == "예제2").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.toast("예제2 제출되었습니다")
                #st.empty() # 폼 제출 후 페이지 새로 고침

    # 관리자용 페이지
    if page == "관리자용":
        password = st.text_input("비밀번호를 입력하세요", type="password")

        if password == "2345":
            ex1 = session.query(Gimgirl).filter(Gimgirl.name == "예제1").first()
            ex2 = session.query(Gimgirl).filter(Gimgirl.name == "예제2").first()

            total1 = ex1.ten * 10 + ex1.twe * 20 + ex1.tre * 30
            total2 = ex2.ten * 10 + ex2.twe * 20 + ex2.tre * 30

            st.write(f"예제1 총합: {total1}만원")
            st.write(f"예제2 총합: {total2}만원")

        else:
            st.warning("비밀번호가 틀렸습니다.")

if __name__ == '__main__':
    main()
