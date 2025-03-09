import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
#Base.metadata.drop_all(engine)
#sql 연결
#엔진 생성성
engine = create_engine('sqlite:///gimgirl1.db')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

#gimgirl 모델 정의의
class Gimgirl(Base):
    __tablename__ = 'gimgirs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ten = Column(Integer)  
    twe = Column(Integer) 
    tre = Column(Integer) 

# 테이블 생성
Base.metadata.create_all(engine)

#Base.metadata.drop_all(engine)  # 테이블 삭제
#Base.metadata.create_all(engine) 

ex1 = Gimgirl(name="예제1", ten = 0, twe = 0, tre = 0)
ex2 = Gimgirl(name="예제2", ten = 0, twe = 0, tre = 0)
ex3 = Gimgirl(name="예제3", ten = 0, twe = 0, tre = 0)

session.add(ex1)
session.add(ex2)
session.add(ex3)

session.commit()

def main():


    st.title("김해여고 펀딩 사이트")
    st.header("2025 김해여고 펀딩 사이트")
    st.markdown("===")

    page = st.selectbox("페이지를 선택하세요", ["예제1", "예제2", "관리자용"])

    if page == "예제1":
        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
            st.image('fund.png')
            st.write("예제 글입니다.")
            col21, col22, col23 = st.columns(3)

        with col21:
            if st.button("10만원"):
                    # 10만원 버튼 클릭 시 예제1에 ten값 증가
                session.query(Gimgirl).filter(Gimgirl.name == "예제1").update(
                    {Gimgirl.ten: Gimgirl.ten + 1}
                )
                session.commit()

        with col22:
            if st.button("20만원"):
                    # 20만원 버튼 클릭 시 예제1에 twe값 증가
                session.query(Gimgirl).filter(Gimgirl.name == "예제1").update(
                    {Gimgirl.twe: Gimgirl.twe + 1}
                )
                session.commit()

        with col23:
            if st.button("30만원"):
                    # 30만원 버튼 클릭 시 예제1에 tre값 증가
                session.query(Gimgirl).filter(Gimgirl.name == "예제1").update(
                        {Gimgirl.tre: Gimgirl.tre + 1}
                )
                session.commit()
    
        if st.button("예제1 총합계산"):
                # 예제1의 기부 금액을 가져와서 총합 계산
                ex01 = session.query(Gimgirl).filter(Gimgirl.name == "예제1").first()
                ten1 = ex01.ten
                twe1 = ex01.twe
                tre1 = ex01.tre

                total = ten1 * 10 + twe1 * 20 + tre1 * 30
                st.write(f"{total}만원")
                st.write(f"ten: {ten1} twe: {twe1} tre: {tre1}")


        if page =="예제2":
                col1, col2, col3 = st.columns([1, 3, 1])

                with col2:
            # 이미지 클릭 시 부가 설명이 나오도록
                    st.image('fund.png')

            # st.form을 사용하여 10, 20, 30 선택지 제공
                    with st.form(key='funding_form2'):
                        donation = st.radio("질문:", [10, 20, 30], index=0)
                        submit_button = st.form_submit_button(label="제출하기")

                        if submit_button:
                            
                            
                            if donation == 10:
                                session.query(Gimgirl).filter(Gimgirl.name == "예제2").update(
                                    {Gimgirl.ten: Gimgirl.ten+ 1}
                                )

                                session.commit()
    
                            elif donation == 20:
                                session.query(Gimgirl).filter(Gimgirl.name == "예제1").update(
                                    {Gimgirl.twe: Gimgirl.twe+ 1}
                                )

                                session.commit()

                            elif donation == 30:
                                session.query(Gimgirl).filter(Gimgirl.name == "예제1").update(
                                    {Gimgirl.tre: Gimgirl.tre+ 1}
                                )
    
                                session.commit()
                            st.experimental_rerun()


if __name__ == '__main__':
    main()
