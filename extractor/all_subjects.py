import requests
from bs4 import BeautifulSoup


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


def _get_soup():
    payload = {
        "p_yyhakgi": 20171,
        "p_y2014": 2014,
        "p_abeek": 1,
    }
    r = requests.post("http://sugang.hongik.ac.kr/cn4000.jsp", payload)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def _check_validity(title, category_root):
    if title in tree[category_root]:
        return True
    else:
        return False


def _assign_root(title):
    for category_root in tree:
        if _check_validity(title, category_root):
            return category_root
    else:
        print("mismatch! -> %s" % (title))
        return None


def _get_sub_category(soup):
    return soup.select("#table_seoul > tr > td > a")


def _assign_sub(category_sub):
    sub = {}
    for category in category_sub:
        title = category.get_text()
        root = _assign_root(title)

        sub[category.get_text()] = {
            "href": category["href"][19:],
            "root": root
        }
    return sub


soup = _get_soup()
category_sub = _get_sub_category(soup)
sub = _assign_sub(category_sub)


from pprint import pprint
pprint(sub)