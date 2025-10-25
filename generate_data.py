import json
from typing import TypedDict
import random as rd
import firebase_admin
from firebase_admin import  credentials, db
import streamlit as st



if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('ps-gen-app-firebase-admin.json')
    except Exception as e:
        fb_config = dict(st.secrets['firebase'])
        cred = credentials.Certificate(fb_config)

    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ps-gen-app-default-rtdb.europe-west1.firebasedatabase.app/'
            })

sess_ref = db.reference('sessions')
pass_ref = db.reference('passports')
real_pass = db.reference('real_passs')


def get_existing_batches():
    existing_batches = set()
    data = pass_ref.get()
    if data:
        for _, value in data.items():
            existing_batches.add(value[3])
    return existing_batches

def reset_data():
    pass_ref.set({})
    sess_ref.set({})
    real_pass.set({})

class GenNumber(TypedDict):
    gen_num: list



def generate_real_passport(state: GenNumber, num_of_id, type_of_pass, batch_num) -> GenNumber:
    number_pool = rd.sample(range(10000, 99999), num_of_id)

    for i in number_pool:

        real_pass = 'P'+type_of_pass+batch_num+str(i)
        state[real_pass] = [real_pass, 'unassigned', type_of_pass, batch_num]

    return state

def dump_real_passport_data(num_of_id, type_of_pass, batch_num):
    doc = generate_real_passport({}, num_of_id, type_of_pass, batch_num )
    try:

        real_pass.update(doc)

        #with open('passport.json', 'w') as f:
        #    json.dump(doc, f, indent=4)

        return True
    except Exception as e:
        print(f'error with file {e}')
        return False



def generate_passport(state: GenNumber, num_of_id, type_of_pass, batch_num) -> GenNumber:
    number_pool = rd.sample(range(10000, 99999), num_of_id)

    for i in number_pool:

        passport = 'V'+type_of_pass+batch_num+str(i)
        state[passport] = [passport, 'unassigned', type_of_pass, batch_num]

    return state

def dump_passport_data(num_of_id, type_of_pass, batch_num):
    doc = generate_passport({}, num_of_id, type_of_pass, batch_num )
    try:

        pass_ref.update(doc)

        #with open('passport.json', 'w') as f:
        #    json.dump(doc, f, indent=4)

        return True
    except Exception as e:
        print(f'error with file {e}')
        return False


def generate_session(state: GenNumber, num_of_id, type_of_pass, batch_num) -> GenNumber:
    number_pool = rd.sample(range(10000, 99999),num_of_id)
    for i in number_pool:
        sess_id = 'S'+type_of_pass+batch_num + str(i)
        state[sess_id] = [sess_id, 'unassigned', type_of_pass, batch_num]

    return state


def dump_session_data(num_of_id, type_of_pass, batch_num):
    doc = generate_session({},num_of_id, type_of_pass, batch_num )
    try:

        sess_ref.update(doc)
        #with open('session.json', 'w') as f:
        #    json.dump(doc, f, indent=4)
        return True
    except Exception as e:
        print(f'error with file {e}')
        return False

def get_pass_data():
    pass_doc = pass_ref.get()
    return pass_doc

def get_real_pass_data():
    real_pass_doc = real_pass.get()
    return real_pass_doc


def get_sess_data():
    sess_doc = sess_ref.get()
    return sess_doc



if __name__ == '__main__':
    #dump_passport_data(num_of_id = 100, type_of_pass='D',batch_num='B1' )
    #dump_session_data(num_of_id = 100, type_of_pass='D', batch_num='B1')
    reset_data()
    dump_passport_data(num_of_id=1, type_of_pass='D', batch_num='B0')
    dump_session_data(num_of_id = 1, type_of_pass='D', batch_num='B0')
    dump_real_passport_data(num_of_id=1, type_of_pass='D', batch_num='B0')