from mixer import real_profs_subjects as tree


source = '''
<html>
    <head>
        <title>우수 강사별 과목 조회</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="author" content="정겨울">
        <link href="best_subject.css" type="text/css" rel="stylesheet" />
    </head>
    <body>
        <h1>2017년 2학기 우수 강사별 과목 조회 시스템</h1>
        <p>
            2017년 8월 20일 0시 생성<br />
            <a href="http://winterj.me">정겨울</a><br />
            <a href="https://github.com/JungWinter/HongikBestSubject">Github repo</a><br />
        </p>
        <table>
            <tbody>
                <tr>
                    <th rowspan="3">구분</th>
                    <th rowspan="3">교수명</th>
                    <th rowspan="3">소속대학</th>
                    <th rowspan="3">소속학과</th>
                </tr>
                <tr>
                    <th colspan="6">과목</th>
                </tr>
                <tr>
                    <th>구분</th>
                    <th>학년</th>
                    <th>학과</th>
                    <th>학수번호</th>
                    <th>과목명</th>
                    <th>요일및시간</th>
                </tr>

                {}
            </tbody>
        </table>

    {}
    </body>
</html>
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
                    <td>{}</td>
                </tr>
'''
google = '''
<!-- Google Analytics -->
	<script async="" src="https://www.google-analytics.com/analytics.js"></script><script>
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

		ga('create', 'UA-89592553-1', 'auto');
		ga('send', 'pageview', {
		  'page': '/project/best_subject',
		  'title': '2017년 2학기 우수 강사별 과목 조회 시스템'
		});
	</script>
	<!-- End Google Analytics -->
'''
source_body = ""
for name in tree:
    subjects = tree[name]["과목"]
    rowspan = len(subjects) + 1

    # add subjects
    source_subjects = ""
    for subject in subjects:
        source_subjects = source_subjects + template_subjects.format(
            subject[6],
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

final_source = source.format(source_body, google)
with open("./output/result.html", mode="w", encoding="utf-8") as fp:
    fp.write(final_source)
