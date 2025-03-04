import streamlit as st

def main():
    st.title("김해여고 펀딩 사이트")
    st.header("2025 김해여고 펀딩 사이트")
    st.markdown("===")

    col1,col2,col3= st.columns([1,1,1])

    with col2:
        st.image('fund.png')
                 
        if st.button("학생용"):
            st.experimental_rerun('https://gimgirlpro-rpowqmyhh48fut3mpcoqpm.streamlit.app')
        st.button("관리자용")

  

if __name__ == '__main__':
    main()
  
