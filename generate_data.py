import json
from typing import TypedDict

class GenNumber(TypedDict):
    gen_num: list

def generate_passport(state: GenNumber) -> GenNumber:
    number_pool = [numb for numb in range(10000, 99999)]
    for i in number_pool:
        passport = 'P1'+str(i)
        state[passport] = [passport, 'unassigned']

    return state

def dump_passport_data():
    doc = generate_passport({})
    try:
        with open('passport.json', 'w') as f:
            json.dump(doc, f, indent=4)
        return True
    except Exception as e:
        print(f'error with file {e}')
        return False


def generate_session(state: GenNumber) -> GenNumber:
    number_pool = [numb for numb in range(10000, 99999)]
    for i in number_pool:
        sess_id = 'S1' + str(i)
        state[sess_id] = [sess_id, 'unassigned']

    return state


def dump_session_data():
    doc = generate_session({})
    try:
        with open('session.json', 'w') as f:
            json.dump(doc, f, indent=4)
        return True
    except Exception as e:
        print(f'error with file {e}')
        return False


if __name__ == '__main__':
    dump_passport_data()
    dump_session_data()