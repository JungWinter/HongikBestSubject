from best_professor import load as prof_load
from all_subjects import load as subj_load
from collections import OrderedDict

# load data
titles, best_profs = prof_load()
departs = subj_load()

# init main variable
profs_subjects = OrderedDict()
for prof in best_profs:
    profs_subjects[prof[1]] = {
        "구분": prof[0],
        "소속대학": prof[2],
        "소속학과": prof[3],
        "과목": [],
    }

# insert best subjects into main variable
for depart in departs:
    if departs[depart]["child"] is None:
        continue
    for subject in departs[depart]["child"]:
        subject.append(depart)
        name = subject[4]
        if name in profs_subjects:
            profs_subjects[name]["과목"].append(subject)

# filter subject count == 0
real_profs_subjects = OrderedDict()
for name in profs_subjects:
    if profs_subjects[name]["과목"] != []:
        real_profs_subjects[name] = profs_subjects[name]

# counting
subject_count = sum(
    len(real_profs_subjects[name]["과목"]) for name in real_profs_subjects
)
prof_count = len(real_profs_subjects)

