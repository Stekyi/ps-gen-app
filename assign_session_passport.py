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


def assign_passport(pass_num):
    """Assigns a random unassigned passport and marks it as assigned."""
    # Get fresh data from Firebase
    pass_ref = ref_pass.get()
    #print(pass_ref)
    pass_data = [v for k,v in pass_ref.items() if k== pass_num ]
    #print(pass_data)



    if not pass_data:
        #raise ValueError("No passports found in database.")
        return False
    else:
        #print(12)
        if pass_data[0][1] == 'assigned':
            #print(23)
            return False
        else:
            #print(34)
            pass_ref[pass_num][1] = 'assigned'
            #print(45)
            ref_pass.child(pass_num).set(pass_ref[pass_num])

            return True

    #unassigned_pass = [k for k, v in pass_ref.items() if v[1] == 'unassigned']

    #if not unassigned_pass:
    #    raise ValueError("No unassigned passports available.")

    #select_random_pass = random.choice(unassigned_pass)

    # Update Firebase




def assign_session(visa_num):
    """Assigns a random unassigned session and marks it as assigned."""
    # Get fresh data from Firebase
    sess_ref = ref_sess.get()
    typ_of_visa = visa_num[1]
    if not sess_ref:
        raise ValueError("No sessions found in database.")

    unassigned_sess = [k for k, v in sess_ref.items() if v[1] == 'unassigned' and v[2]==typ_of_visa]

    if not unassigned_sess:
        raise ValueError("No unassigned sessions available.")

    select_random_sess = random.choice(unassigned_sess)
    sess_ref[select_random_sess][1] = 'assigned'

    # Update Firebase
    ref_sess.child(select_random_sess).set(sess_ref[select_random_sess])

    return select_random_sess


if __name__ == '__main__':
    try:
        pass_num = assign_passport('VGB399370') #     PDB461044 PDB474185
        if pass_num:
            sess_id = assign_session('VGB399370')
            print(f'Your passport is {pass_num} and your session is {sess_id}')
        else:
            print('Number not valid or already utilised')
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")