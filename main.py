import streamlit as st
import assign_session_passport as asp

st.title('Get your session ID with a valid pass')
top_container = st.container()
down_container = st.container()
with top_container:
    st.info('''The assigned session ID can only be used once.
    \nEnter your pass id(passport)  and click the button to generate a session ID.\n
    There is no link between your pass and the session ID.''')

with down_container:
    with st.form(key='passid'):
        pass_num = st.text_input(label='Enter assigned Pass:').upper()

        gen_butt = st.form_submit_button(label='Click here')
        if gen_butt:
            with st.spinner('Fetching Please wait...'):
                pass_status = asp.assign_passport(pass_num)

                if pass_status:
                    sess_id = asp.assign_session()
                    st.subheader(f'Your Session ID is {sess_id}, Copy and Keep')
                else:
                    st.error('Either your pass is invalid or has been used to generate a session already')

