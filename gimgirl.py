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
    Re2_1 = Gimgirl(name="2-1", ten=0, twe=0, tre=0)
    Re2_2 = Gimgirl(name="2-2", ten=0, twe=0, tre=0)
    Re2_3 = Gimgirl(name="2-3", ten=0, twe=0, tre=0)
    Re2_4 = Gimgirl(name="2-4", ten=0, twe=0, tre=0)
    Re2_5 = Gimgirl(name="2-5", ten=0, twe=0, tre=0)
    Re2_6 = Gimgirl(name="2-6", ten=0, twe=0, tre=0)
    Re2_7 = Gimgirl(name="2-7", ten=0, twe=0, tre=0)
    Re2_8 = Gimgirl(name="2-8", ten=0, twe=0, tre=0)
    Re1_1 = Gimgirl(name="1-1", ten=0, twe=0, tre=0)
    Re1_2 = Gimgirl(name="1-2", ten=0, twe=0, tre=0)
    Re1_3 = Gimgirl(name="1-3", ten=0, twe=0, tre=0)
    Re1_4 = Gimgirl(name="1-4", ten=0, twe=0, tre=0)
    Re1_5 = Gimgirl(name="1-5", ten=0, twe=0, tre=0)
    Re1_6 = Gimgirl(name="1-6", ten=0, twe=0, tre=0)
    Re1_7 = Gimgirl(name="1-7", ten=0, twe=0, tre=0)
    Re1_8 = Gimgirl(name="1-8", ten=0, twe=0, tre=0)



    session.add(Re2_1)
    session.add(Re2_2)
    session.add(Re2_3)
    session.add(Re2_4)
    session.add(Re2_5)
    session.add(Re2_6)
    session.add(Re2_7)
    session.add(Re2_8)
    session.add(Re1_1)
    session.add(Re1_2)
    session.add(Re1_3)
    session.add(Re1_4)
    session.add(Re1_5)
    session.add(Re1_6)
    session.add(Re1_7)
    session.add(Re1_8)
    session.commit()

def main():
    st.header("2025 김해여고 펀딩 사이트")
    #st.markdown("===")

    page = st.selectbox("페이지를 선택하세요", ["2학년 1반", "2학년 2반", "2학년 3반","2학년 4반","2학년 5반", "2학년 6반", "2학년 7반","2학년 8반","1학년 1반", "1학년 2반", "1학년 3반","1학년 4반","1학년 5반", "1학년 6반", "1학년 7반","1학년 8반"])

    # 예제1 페이지
    if page == "2학년 1반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원", "20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-1").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-1").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-1").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")
        


    # 예제2 페이지
    if page == "2학년 2반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form2'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-2").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-2").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-2").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "2학년 3반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form3'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-3").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-3").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-3").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "2학년 4반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form4'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-4").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-4").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-4").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "2학년 5반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form5'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-5").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-5").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-5").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "2학년 6반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form6'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-6").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-6").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-6").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "2학년 7반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form7'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-7").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-7").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-7").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "2학년 8반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form8'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-8").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-8").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "2-8").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 1반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_1'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-1").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-1").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-1").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 2반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_2'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-2").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-2").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-2").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 3반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_3'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-3").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-3").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-3").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 4반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_4'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-4").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-4").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-4").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 5반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_5'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-5").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-5").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-5").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 6반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_6'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-6").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-6").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-6").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 7반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form1_7'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-7").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-7").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-7").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")

    if page == "1학년 8반":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')

        with st.form(key='funding_form2'):
            donation = st.radio("펀딩을 얼마할 지 선택해주세요", ["10만원","20만원", "30만원"], index=0)
            submit_button = st.form_submit_button(label="제출하기")

            if submit_button:
                if donation == "10만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-8").update({Gimgirl.ten: Gimgirl.ten + 1})
                elif donation == "20만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-8").update({Gimgirl.twe: Gimgirl.twe + 1})
                elif donation == "30만원":
                    session.query(Gimgirl).filter(Gimgirl.name == "1-8").update({Gimgirl.tre: Gimgirl.tre + 1})
                session.commit()

                st.success("제출되었습니다")
                
    # 관리자용 페이지
    if page == "관리자용":
        password = st.text_input("비밀번호를 입력하세요", type="password")

        if password == "2345":
            re2_1 = session.query(Gimgirl).filter(Gimgirl.name == "2-1").first()
            re2_2 = session.query(Gimgirl).filter(Gimgirl.name == "2-2").first()
            re2_3 = session.query(Gimgirl).filter(Gimgirl.name == "2-3").first()
            re2_4 = session.query(Gimgirl).filter(Gimgirl.name == "2-4").first()
            re2_5 = session.query(Gimgirl).filter(Gimgirl.name == "2-5").first()
            re2_6 = session.query(Gimgirl).filter(Gimgirl.name == "2-6").first()
            re2_7 = session.query(Gimgirl).filter(Gimgirl.name == "2-7").first()
            re2_8 = session.query(Gimgirl).filter(Gimgirl.name == "2-8").first()
            re1_1 = session.query(Gimgirl).filter(Gimgirl.name == "1-1").first()
            re1_2 = session.query(Gimgirl).filter(Gimgirl.name == "1-2").first()
            re1_3 = session.query(Gimgirl).filter(Gimgirl.name == "1-3").first()
            re1_4 = session.query(Gimgirl).filter(Gimgirl.name == "1-4").first()
            re1_5 = session.query(Gimgirl).filter(Gimgirl.name == "1-5").first()
            re1_6 = session.query(Gimgirl).filter(Gimgirl.name == "1-6").first()
            re1_7 = session.query(Gimgirl).filter(Gimgirl.name == "1-7").first()
            re1_8 = session.query(Gimgirl).filter(Gimgirl.name == "1-8").first()
           

            total2_1 = re2_1.ten * 10 + re2_1.twe * 20 + re2_1.tre * 30
            total2_2 = re2_2.ten * 10 + re2_2.twe * 20 + re2_2.tre * 30
            total2_3 = re2_3.ten * 10 + re2_3.twe * 20 + re2_3.tre * 30
            total2_4 = re2_4.ten * 10 + re2_4.twe * 20 + re2_4.tre * 30
            total2_5 = re2_5.ten * 10 + re2_5.twe * 20 + re2_5.tre * 30
            total2_6 = re2_6.ten * 10 + re2_6.twe * 20 + re2_6.tre * 30
            total2_7 = re2_7.ten * 10 + re2_7.twe * 20 + re2_7.tre * 30
            total2_8 = re2_8.ten * 10 + re2_8.twe * 20 + re2_8.tre * 30
            total1_1 = re1_1.ten * 10 + re1_1.twe * 20 + re1_1.tre * 30
            total1_2 = re1_2.ten * 10 + re1_2.twe * 20 + re1_2.tre * 30
            total1_3 = re1_3.ten * 10 + re1_3.twe * 20 + re1_3.tre * 30
            total1_4 = re1_4.ten * 10 + re1_4.twe * 20 + re1_4.tre * 30
            total1_5 = re1_5.ten * 10 + re1_5.twe * 20 + re1_5.tre * 30
            total1_6 = re1_6.ten * 10 + re1_6.twe * 20 + re1_6.tre * 30
            total1_7 = re1_7.ten * 10 + re1_7.twe * 20 + re1_7.tre * 30
            total1_8 = re1_8.ten * 10 + re1_8.twe * 20 + re1_8.tre * 30
    

            st.write(f"2학년 1반 총합: {total2_1}만원")
            st.write(f"2학년 2반 총합: {total2_2}만원")
            st.write(f"2학년 3반 총합: {total2_3}만원")
            st.write(f"2학년 4반 총합: {total2_4}만원")
            st.write(f"2학년 5반 총합: {total2_5}만원")
            st.write(f"2학년 6반 총합: {total2_6}만원")
            st.write(f"2학년 7반 총합: {total2_7}만원")
            st.write(f"2학년 8반 총합: {total2_8}만원")
            st.write(f"1학년 1반 총합: {total1_1}만원")
            st.write(f"1학년 2반 총합: {total1_2}만원")
            st.write(f"1학년 3반 총합: {total1_3}만원")
            st.write(f"1학년 4반 총합: {total1_4}만원")
            st.write(f"1학년 5반 총합: {total1_5}만원")
            st.write(f"1학년 6반 총합: {total1_6}만원")
            st.write(f"1학년 7반 총합: {total1_7}만원")
            st.write(f"1학년 8반 총합: {total1_8}만원")

        else:
            st.warning("비밀번호가 틀렸습니다.")

if __name__ == '__main__':
    main()
