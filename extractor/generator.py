from mixer import real_profs_subjects as tree


source = '''
<table border="1">
    <tr>
        <td rowspan="3">구분</td>
        <td rowspan="3">교수명</td>
        <td rowspan="3">소속대학</td>
        <td rowspan="3">소속학과</td>
    </tr>
    <tr>
        <td colspan="5">과목</td>
    </tr>
    <tr>
        <td>학년</td>
        <td>학과</td>
        <td>학수번호</td>
        <td>과목명</td>
        <td>요일및시간</td>
    </tr>

    {}
</table>
'''
template_header = '''
    <tr>
        <td rowspan="{}">{}</td>
        <td rowspan="{}">{}</td>
        <td rowspan="{}">{}</td>
        <td rowspan="{}">{}</td>
    </tr>
    {}
'''
template_subjects = '''
    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
'''

source_body = ""
for name in tree:
    subjects = tree[name]["과목"]
    rowspan = len(subjects) + 1

    # add subjects
    source_subjects = ""
    for subject in subjects:
        source_subjects = source_subjects + template_subjects.format(
            subject[0],
            subject[1],
            subject[2],
            subject[3],
            subject[5]
        )

    # add professor and subjects
    univ = tree[name]["소속대학"]
    univ = "" if univ == "Null" else univ
    source_body = source_body + template_header.format(
        rowspan, tree[name]["구분"],
        rowspan, name,
        rowspan, univ,
        rowspan, tree[name]["소속학과"],
        source_subjects
    )

final_source = source.format(source_body)
with open("./output/result.html", mode="w", encoding="utf-8") as fp:
    fp.write(final_source)
