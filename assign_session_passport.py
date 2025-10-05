import json
from filelock import FileLock
import random

def assign_passport():
    lock_pass = FileLock('passport.json.lock')
    with lock_pass:
        with open('passport.json', 'r') as f:
            doc = json.load(f)

        unassigned_pass = [k for k, v in doc.items() if v[1] == 'unassigned']
        if not unassigned_pass:
            raise ValueError("No unassigned passports available.")
        select_random_pass = random.choice(unassigned_pass)
        doc[select_random_pass][1] = 'assigned'

    with lock_pass:
        with open('passport.json', 'w') as f:
            json.dump(doc, f, indent=4)

    return select_random_pass

def assign_session():
    lock_sess = FileLock('session.json.lock')
    with lock_sess:
        with open('session.json', 'r') as f:
            doc = json.load(f)

        unassigned_sess = [k for k, v in doc.items() if v[1] == 'unassigned']
        if not unassigned_sess:
            raise ValueError("No unassigned sessions available.")
        select_random_sess = random.choice(unassigned_sess)
        doc[select_random_sess][1] = 'assigned'
    print('finished and lock released')
    with lock_sess:
        print('here to write')
        with open('session.json', 'w') as f:
            json.dump(doc, f, indent=4)

    return select_random_sess

if __name__ == '__main__':
    pass_num = assign_passport()
    sess_id = assign_session()
    print(f'Your passport is {pass_num} and your session is {sess_id}')