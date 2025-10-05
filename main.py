import streamlit as st
import assign_session_passport as asp

st.title('Get your passport number and session ID')
top_container = st.container()
down_container = st.container()
with top_container:
    st.write('''Keep your passport safe. The assigned session ID can only be used once. 
            \n click the button is visible below to access your passport and session ID''')

with down_container:
    place_hold = st.empty()

gen_butt = place_hold.button(label='Click here')

if gen_butt:
    with st.spinner('Fetching Please wait...'):
        pass_num = asp.assign_passport()
        sess_id = asp.assign_session()
    place_hold.write(f'Your passport is {pass_num} and your session is {sess_id}')

