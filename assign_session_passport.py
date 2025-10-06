import json
import random
import firebase_admin
from firebase_admin import db, credentials
import streamlit as st

# Initialize Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('ps-gen-app-firebase-admin.json')
    except Exception as e:
        # Fixed: st.secrets is accessed like a dictionary, not a function
        fb_config = dict(st.secrets["firebase"])
        cred = credentials.Certificate(fb_config)

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ps-gen-app-default-rtdb.europe-west1.firebasedatabase.app/'
    })

# Reference setup
ref_sess = db.reference('sessions')
ref_pass = db.reference('passports')


def assign_passport():
    """Assigns a random unassigned passport and marks it as assigned."""
    # Get fresh data from Firebase
    pass_ref = ref_pass.get()

    if not pass_ref:
        raise ValueError("No passports found in database.")

    unassigned_pass = [k for k, v in pass_ref.items() if v[1] == 'unassigned']

    if not unassigned_pass:
        raise ValueError("No unassigned passports available.")

    select_random_pass = random.choice(unassigned_pass)
    pass_ref[select_random_pass][1] = 'assigned'

    # Update Firebase
    ref_pass.child(select_random_pass).set(pass_ref[select_random_pass])

    return select_random_pass


def assign_session():
    """Assigns a random unassigned session and marks it as assigned."""
    # Get fresh data from Firebase
    sess_ref = ref_sess.get()

    if not sess_ref:
        raise ValueError("No sessions found in database.")

    unassigned_sess = [k for k, v in sess_ref.items() if v[1] == 'unassigned']

    if not unassigned_sess:
        raise ValueError("No unassigned sessions available.")

    select_random_sess = random.choice(unassigned_sess)
    sess_ref[select_random_sess][1] = 'assigned'

    # Update Firebase
    ref_sess.child(select_random_sess).set(sess_ref[select_random_sess])

    return select_random_sess


if __name__ == '__main__':
    try:
        pass_num = assign_passport()
        sess_id = assign_session()
        print(f'Your passport is {pass_num} and your session is {sess_id}')
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")