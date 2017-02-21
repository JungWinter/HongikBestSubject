import requests
import time
import os
import json
from bs4 import BeautifulSoup


MAX_COLUMN = 15
tree = {
    "ABEEK교양교과": ["기초교양", "일반교양", "핵심교양"],
    "일반교양(서울)": ["인문계열", "사회계열", "자연계열", "예체능계열", "영어계열", "제2외국어계열", "교직"],
    "공과대학": ["공대전공공통", "건설도시공학부", "전자전기공학부", "신소재화공시스템공학부", "정보컴퓨터공학부", "기계시스템디자인공학과"],
    "경영대학": ["경영학부"],
    "사범대학": ["사대공통", "수학교육과", "국어교육과", "영어교육과", "역사교육과", "교육학과"],
    "미술대학": ["미대전공공통", "동양화과", "회화과", "판화과", "조소과", "디자인학부", "금속조형디자인과", "도예유리과", "목조형가구학과", "섬유미술패션디자인과", "예술학과"],
    "문과대학": ["영어영문학과", "독어독문학과", "불어불문학과", "국어국문학과"],
    "MSC교과": ["MSC수학", "MSC과학", "MSC전산"],
    "건축대학": ["건축학부"],
    "경제학부": ["경제학부"],
    "융합전공": ["문화예술경영전공", "공연예술전공", "건축공간예술전공"],
    "법과대학": ["법대공통", "법학과", "법학부"],
    "산업정보융합학부": ["산업정보융합학부"],
}


def _get_soup(url, payload):
    r = requests.post(url, payload)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def _check_title_validity(title, category_root):
    if title in tree[category_root]:
        return True
    else:
        return False


def _assign_root(title):
    for category_root in tree:
        if _check_title_validity(title, category_root):
            return category_root
    else:
        print("mismatch! -> %s" % (title))
        return None


def _get_sub_category(soup):
    return soup.select("#table_seoul > tr > td > a")


def _get_subjects_title(soup):
    return soup.select("#select_list > tr > th")


def _get_subjects(soup):
    return soup.select("#select_list > tr")


def _assign_sub(category_sub):
    sub = {}
    for category in category_sub:
        title = category.get_text()
        root = _assign_root(title)

        sub[category.get_text()] = {
            "href": eval(category["href"][19:]),
            "root": root,
            "child": None,
        }
    return sub


def _set_payload(phase, sub=None, depart=None):
    if phase == 1:
        payload = {
            "p_yyhakgi": 20171,
            "p_y2014": 2014,
            "p_abeek": 1,
        }
    elif phase == 2 and depart is not None and sub is not None:
        payload = {
            "p_yy": 2017,
            "p_hakgi": 1,
            "p_campus": sub[depart]["href"][0],
            "p_gubun":  sub[depart]["href"][1],
            "p_dept":  sub[depart]["href"][2],
            "p_grade":  sub[depart]["href"][3],
            "p_abeek": 1,
            "p_2014": 2014,
            "p_2016": "on",
        }
    return payload


def _pick_needed_columns(subjects_title):
    cols = [
        subjects_title.index("개설학년"),
        subjects_title.index("개설학과"),
        subjects_title.index("학수번호"),
        subjects_title.index("과목명"),
        subjects_title.index("교수명"),
        subjects_title.index("요일및시간"),
    ]
    return cols


def _check_depart_validity(subjects):
    if "검색된 과목" in subjects[0][0]:
        return False
    else:
        return True


def _fill_subject_padding(subject):
    if len(subject) < MAX_COLUMN:
        subject = subject + ["Null"] * (MAX_COLUMN - len(subject))
    return subject


def save():
    # phase 1
    url = "http://sugang.hongik.ac.kr/cn4000.jsp"
    payload = _set_payload(1)
    soup = _get_soup(url, payload)
    category_sub = _get_sub_category(soup)
    sub = _assign_sub(category_sub)

    # phase 2
    url = "http://sugang.hongik.ac.kr/cn4001.jsp"
    for i, depart in enumerate(sub):
        payload = _set_payload(2, sub, depart)
        soup = _get_soup(url, payload)
        subjects_title = _get_subjects_title(soup)
        subjects = _get_subjects(soup)

        # subjects_title -> str의 list, 한글로 된 컬럼 명
        # columns -> int의 list, 정수로 된 필요한 컬럼의 인덱스
        # subjects -> str의 list들의 list, 모든 과목들
        # picked_subjects -> str의 list들의 list, 필요한 column만 걸러진 과목들
        subjects_title = [title.get_text() for title in subjects_title]
        columns = _pick_needed_columns(subjects_title)
        subjects = [subject.get_text().strip().split("\n") for subject in subjects[1:-2]]
        subjects = [_fill_subject_padding(subject) for subject in subjects]
        picked_subjects = []

        # 출력부분
        print(depart, "> 과목 수 :", len(subjects))
        if _check_depart_validity(subjects):
            for subject in subjects:
                picked_subjects.append([subject[index] for index in columns])

            sub[depart]["child"] = picked_subjects
        print("%d/%d processing" % (i+1, len(sub)))
        time.sleep(0.5)

    path = "./output"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/all_subject_output.txt", mode="w") as fp:
        json.dump(sub, fp)
    return None


def load():
    if os.path.exists("./output/all_subject_output.txt"):
        with open("./output/all_subject_output.txt", mode="r") as fp:
            sub = json.load(fp)
            return sub
    return None


if __name__ == "__main__":
    sub = load()
    if sub is None:
        save()
        sub = load()
    import pprint
    pprint.pprint(sub["법학과"])
    pprint.pprint(sub["사대공통"])
