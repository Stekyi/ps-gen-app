import streamlit as st
#import json
import pandas as pd
import generate_data as gd
from streamlit.components.v1 import html

st.set_page_config(page_title="Dashboard Graph", layout="wide")
st.title('Dashboard')
col1, col2, col3 = st.columns([4,4,4])

reset_mode = True
generate = True
# All available batches
all_batches = [f"B{i}" for i in range(1, 11)]  # Creates ['B1', 'B2', ..., 'B10']
existing_batch = gd.get_existing_batches()



def reload_page():
    html("""
        <script>
            window.parent.location.reload();
        </script>
    """)


with col1:
    #with open('passport.json') as f:
    passports =  gd.get_pass_data()

    assigned_passports = [v for _, v in passports.items()]
    assigned, unassigned = [sum(status == s for _, status, _,_ in assigned_passports) for s in ("assigned", "unassigned")]
    if assigned/unassigned < 0.25:
        df_assigned_passports = pd.DataFrame(assigned_passports, columns=['passport#', 'status', 'Type_of_ID', 'Batch'])
        df_assigned_passports['status'] = ''
    else:
        df_assigned_passports = pd.DataFrame(assigned_passports, columns=['passport#', 'status', 'Type_of_ID', 'Batch'])
    st.dataframe(df_assigned_passports)
    # Convert to CSV for download
    csv = df_assigned_passports.to_csv(index=False).encode('utf-8')

    # Add a download button
    st.download_button(
        label="Download pass as CSV",
        data=csv,
        file_name='passport_table.csv',
        mime='text/csv'
    )


with col2:
    #with open('session.json') as f:
    sessions = gd.get_sess_data()

    assigned_session = [v for _, v in sessions.items() ]

    assigned, unassigned = [sum(status == s for _,status, _,_ in assigned_session) for s in ("assigned", "unassigned")]
    if assigned / unassigned < 0.25:
        df_assigned_session = pd.DataFrame(assigned_session, columns=['passport#', 'status', 'Type_of_ID', 'Batch'])
        df_assigned_session['status'] = ''
    else:
        df_assigned_session = pd.DataFrame(assigned_session, columns=['passport#', 'status', 'Type_of_ID', 'Batch'])

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

        if reset_mode:
            number_of_IDs = st.number_input('Number of IDs to generate', step=1)
            type_of_ID = st.selectbox('Generate for (D-Delegates, G-General Voter ):', ['D', 'G'])

            available_batches = [batch for batch in all_batches if batch not in existing_batch]

            if available_batches:
                batch_num = st.selectbox(
                    "Select Batch",
                    options=available_batches,
                    index=0
                )
                #st.write(f"You selected: {batch_num}")
            else:
                st.warning("All batches (B1-B10) are already in use!")
                generate = False
                selected_batch = None

            gen_pass = st.button(label='Generate #s')

            if gen_pass & generate:
                with st.spinner('Generating, please wait'):
                    gd.dump_passport_data(number_of_IDs, type_of_ID, batch_num)
                    gd.dump_session_data(number_of_IDs, type_of_ID, batch_num)

                    st.success('New Numbers Generated, refresh page to load')
                    number_placeholder.text(f'Assigned Pass and Sess_id: *** {count_of_pass} ***  ')
                    reload_page()
            else:
                # Warning alert (yellow)
                st.warning("⚠️ Number of IDs and/or batch ids to Generate can not be 0!")

