import streamlit as st
import json
import pandas as pd
import generate_data as gd
st.title('Dashboard')
col1, col2, col3 = st.columns([4,4,4])

with col1:
    #with open('passport.json') as f:
    passports =  gd.get_pass_data()

    assigned_passports = [v for _, v in passports.items()]
    df_assigned_passports = pd.DataFrame(assigned_passports, columns=['passport#', 'status'])
    st.dataframe(df_assigned_passports)
    # Convert to CSV for download
    csv = df_assigned_passports.to_csv(index=False).encode('utf-8')

    # Add a download button
    st.download_button(
        label="Download table as CSV",
        data=csv,
        file_name='passport_table.csv',
        mime='text/csv'
    )


with col2:
    #with open('session.json') as f:
    sessions = gd.get_sess_data()

    assigned_session = [v for _, v in sessions.items() ]
    df_assigned_session = pd.DataFrame(assigned_session, columns=['session_id', 'status'])
    st.dataframe(df_assigned_session)
    # Convert to CSV for download
    csv = df_assigned_session.to_csv(index=False).encode('utf-8')

    # Add a download button
    st.download_button(
        label="Download table as CSV",
        data=csv,
        file_name='session_table.csv',
        mime='text/csv'
    )

with col3:
    top_cont = st.container()
    bottom_cont = st.container()
    with bottom_cont:
        number_placeholder = st.empty()

    with top_cont:
        count_of_pass = len(df_assigned_passports[df_assigned_passports['status'] == 'assigned'])

        number_placeholder.text(f'Assigned Pass and Sess_id: *** {count_of_pass} ***  ')
        st.write('Generate fresh session and passport blocks')

        gen_pass = st.button(label='Generate #s')
        if gen_pass:
            with st.spinner('Generating, please wait'):
                gd.dump_passport_data()
                gd.dump_session_data()
                st.write('New Numbers Generated, refresh page to load')
                number_placeholder.text(f'Assigned Pass and Sess_id: *** {count_of_pass} ***  ')



