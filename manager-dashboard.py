import streamlit as st
import pandas as pd
import generate_data as gd
from streamlit.components.v1 import html

# Constants
ALL_BATCHES = [f"B{i}" for i in range(1, 11)]
STATUS_ASSIGNED = "assigned"
STATUS_UNASSIGNED = "unassigned"

# Page configuration
st.set_page_config(page_title="Dashboard", layout="wide"

)

# Hide Streamlit elements using custom CSS
def hide_streamlit_elements():
    """Hide default Streamlit UI elements like GitHub icon, Deploy button, and menu."""
    hide_style = """
                           <style>
                           /* Hide GitHub icon */
                           #MainMenu {visibility: hidden;}

                           /* Hide Streamlit footer */
                           footer {visibility: hidden;}

                           /* Hide the Deploy button and GitHub toolbar */
                           .stDeployButton {display: none;}

                           /* Optional: Hide the hamburger menu completely */
                           header[data-testid="stHeader"] {
                               display: none;
                           }

                           /* Optional: Reduce top padding when header is hidden */
                           .block-container {
                               padding-top: 2rem;
                           }
                           </style>
                       """
    st.markdown(hide_style, unsafe_allow_html=True)


# Call this function at the start of your app
#hide_streamlit_elements()

st.title('Dashboard')


def reload_page():
    """Reload the current page using JavaScript."""
    html("""
        <script>
            window.parent.location.reload();
        </script>
    """)


def create_status_dataframe(data_dict, filter_type=None, hide_status_threshold=None):
    """
    Create a DataFrame from passport/session data with optional filtering and status hiding.

    Args:
        data_dict: Dictionary of passport/session data
        filter_type: Filter by Type_of_ID ('D', 'G', or None for all)
        hide_status_threshold: If assigned/unassigned ratio is below this, hide status

    Returns:
        pandas.DataFrame with columns ['passport#', 'status', 'Type_of_ID', 'Batch']
    """
    data_list = list(data_dict.values())

    # Apply filter if specified
    if filter_type and filter_type != 'All':
        data_list = [item for item in data_list if item[2] == filter_type]

    df = pd.DataFrame(data_list, columns=['passport#', 'status', 'Type_of_ID', 'Batch'])

    if hide_status_threshold is not None and len(data_list) > 0:
        assigned_count = sum(1 for _, status, _, _ in data_list if status == STATUS_ASSIGNED)
        unassigned_count = sum(1 for _, status, _, _ in data_list if status == STATUS_UNASSIGNED)

        if unassigned_count > 0 and (assigned_count / unassigned_count) < hide_status_threshold:
            df['status'] = ''

    return df


def render_data_table(data_dict, label, filename, filter_type, hide_status_threshold=None, key_prefix=""):
    """
    Render a data table with download button.

    Args:
        data_dict: Dictionary of data to display
        label: Label for the download button
        filename: Filename for CSV download
        filter_type: Filter by Type_of_ID ('D', 'G', or 'All')
        hide_status_threshold: Optional threshold for hiding status column
        key_prefix: Prefix for widget keys to ensure uniqueness
    """
    df = create_status_dataframe(data_dict, filter_type=filter_type, hide_status_threshold=hide_status_threshold)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime='text/csv',
        key=f"{key_prefix}_download"
    )

    # Display count
    st.caption(f"Showing {len(df)} record(s)")


def render_generation_panel():
    """Render the ID generation panel in the right column."""
    passports = gd.get_pass_data()
    assigned_passports = list(passports.values())
    count_assigned = sum(1 for _, status, _, _ in assigned_passports if status == STATUS_ASSIGNED)

    # Display counter
    st.text(f'Assigned Pass and Sess_id: *** {count_assigned} ***  ')
    st.write('Generate fresh session and passport blocks')

    # Get available batches
    existing_batches = gd.get_existing_batches()
    available_batches = [b for b in ALL_BATCHES if b not in existing_batches]

    # Input fields
    number_of_ids = st.number_input('Number of IDs to generate', min_value=0, step=1)
    type_of_id = st.selectbox('Generate for (D-Delegates, G-General Voter):', ['D', 'G'])

    # Batch selection
    if available_batches:
        batch_num = st.selectbox("Select Batch", options=available_batches, index=0)
        can_generate = True
    else:
        st.warning("All batches (B1-B10) are already in use!")
        batch_num = None
        can_generate = False

    # Generate button
    gen_pass = st.button(label='Generate #s')

    if gen_pass:
        if not can_generate or number_of_ids == 0:
            st.warning("⚠️ Number of IDs must be greater than 0 and a batch must be available!")
        else:
            with st.spinner('Generating, please wait...'):
                gd.dump_passport_data(number_of_ids, type_of_id, batch_num)
                gd.dump_session_data(number_of_ids, type_of_id, batch_num)
                st.success('New Numbers Generated, refresh page to load')
                reload_page()


# Main layout
col1, col2, col3 = st.columns([4, 4, 4])

# Global filter at the top
st.sidebar.header("Filter Options")
filter_option = st.sidebar.radio(
    "Filter by ID Type:",
    options=['All', 'D', 'G'],
    index=0,
    help="D = Delegates, G = General Voters"
)

# Left column - Passport data
with col2:
    passports = gd.get_pass_data()
    render_data_table(
        passports,
        label="Download pass as CSV",
        filename="passport_table.csv",
        filter_type=filter_option,
        hide_status_threshold=0.25,
        key_prefix="passport"
    )

# Middle column - Session data
with col3:
    sessions = gd.get_sess_data()
    render_data_table(
        sessions,
        label="Download table as CSV",
        filename="session_table.csv",
        filter_type=filter_option,
        hide_status_threshold=0.10,
        key_prefix="session"
    )

# Right column - Generation panel
with col1:
    render_generation_panel()