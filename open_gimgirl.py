import streamlit as st

def main():
    st.title("김해여고 펀딩 사이트")
    st.header("2025 김해여고 펀딩 사이트")
    st.markdown("===")

    col1,col2,col3= st.colums([1,1,1])

    with col2:
        st.write("
        
                 
                 
                 ")
                 
        if st.button("학생용"):
            streamlit run gimgirl.py
        st.button("관리자용")

  

  
