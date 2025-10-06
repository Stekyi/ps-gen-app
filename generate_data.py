import json
from typing import TypedDict
import random as rd
import firebase_admin
from firebase_admin import db, credentials
import streamlit as st

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('ps-gen-app-firebase-adminsdk-fbsvc-5ebdb64a45.json')
    except Exception as e:
        fb_config = st.secrets('firebase')
        cred = credentials.Certificate(fb_config)

    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ps-gen-app-default-rtdb.europe-west1.firebasedatabase.app/'
            })

sess_ref = db.reference('sessions')
pass_ref = db.reference('passports')


class GenNumber(TypedDict):
    gen_num: list

def generate_passport(state: GenNumber) -> GenNumber:
    number_pool = rd.sample(range(10000, 99999), 100)
    for i in number_pool:
        passport = 'P1'+str(i)
        state[passport] = [passport, 'unassigned']

    return state

def dump_passport_data():
    doc = generate_passport({})
    try:
        pass_ref.set(doc)

        #with open('passport.json', 'w') as f:
        #    json.dump(doc, f, indent=4)

        return True
    except Exception as e:
        print(f'error with file {e}')
        return False


def generate_session(state: GenNumber) -> GenNumber:
    number_pool = rd.sample(range(10000, 99999),100)
    for i in number_pool:
        sess_id = 'S1' + str(i)
        state[sess_id] = [sess_id, 'unassigned']

    return state


def dump_session_data():
    doc = generate_session({})
    try:

        sess_ref.set(doc)
        #with open('session.json', 'w') as f:
        #    json.dump(doc, f, indent=4)
        return True
    except Exception as e:
        print(f'error with file {e}')
        return False

def get_pass_data():
    pass_doc = pass_ref.get()
    return pass_doc


def get_sess_data():
    sess_doc = sess_ref.get()
    return sess_doc



if __name__ == '__main__':
    dump_passport_data()
    dump_session_data()