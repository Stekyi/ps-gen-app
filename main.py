import streamlit as st
import assign_session_passport as asp

# Page configuration
st.set_page_config(
    page_title="Session ID Generator",
    page_icon="🎫",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Hide Streamlit elements using custom CSS
def hide_streamlit_elements():
    """Hide default Streamlit UI elements like GitHub icon, Deploy button, and menu."""
    hide_style = """
        <style>
        /* Hide GitHub icon */
        #MainMenu {visibility: hiddestran;}

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
hide_streamlit_elements()


st.markdown(
    "<h5><b>Welcome to the NGA Session IDs Page</b></h5>",
    unsafe_allow_html=True
)

# Instructions section
st.info("""
**How it works:**
- The assigned Session ID can only be used once to complete a survey
- Enter your Visa # and click the button to generate a Session ID
- Please note that there is no link between your Visa # and the Session ID issued to you, to ensure anonymous voting
""")

st.divider()

# Main form
with st.form(key='session_form', clear_on_submit=False):
    st.markdown("<h5><b>Enter your Visa #:</b></h5>",
    unsafe_allow_html=True)

    pass_num = st.text_input(
        label='''#''',
        placeholder='''#''',
        max_chars=50,
        help="Enter the Visa # that was assigned to you"
    ).strip().upper()


    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.form_submit_button(
            label='🔐 Generate Session ID',
            use_container_width=True,
            type="primary"
        )

    if submit_button:
        # Validation
        if not pass_num:
            st.error("⚠️ Please enter a Visa #")
        else:
            with st.spinner('🔄 Verifying Visa # and generating Session ID...'):
                try:
                    pass_status = asp.assign_passport(pass_num)

                    if pass_status:
                        sess_id = asp.assign_session()

                        # Success message with session ID
                        st.success("✅ Session ID generated successfully!")

                        # Display session ID prominently
                        st.markdown("---")
                        st.markdown("### 🎟️ Your Session ID:")
                        st.code(sess_id, language=None)

                        st.warning("⚠️ **Important:** Copy and use this Session ID to complete your survey. It will only be displayed once!")

                        # Optional: Add copy button using custom component
                        st.info("💡 Use this Session ID to access the survey")

                    else:
                        st.error("""
                        ❌ **Authentication Failed** \n
                        
                        Your Visa # is either invalid or has already been assigned/used by someone else.
                        \nKindly verify your Visa # and try again or contact the issuer for help.
                        
                        
                        """)

                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    st.info("Please try again or contact the issuer if the problem persists.")

# Footer with additional information
st.divider()
with st.expander("ℹ️ Need Help?"):
    st.markdown("""
    **Common Issues:**
    - Make sure you're entering the correct Visa #
    - visa # is not case-insensitive
    - Each Visa # can only generate one Session ID
    - Session IDs are single-use only

    **Security Note:**
    Your Session ID is completely anonymous and cannot be traced back to your Visa #.
    """)