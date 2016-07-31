def course_info_converter(text):
	for line in text.splitlines():
		lst = line.split('\t')
		crn = int(lst[0])
		subject,number,section = lst[1].split()
		name = lst[2]
		prof = lst[-1]
		credit = int(lst[4][0])
		print(lst)


mine = '''30268	ASTR 210 1	Introduction to Astrophysics	Urbana-Champaign	3.000	1U	Aug 22, 2016	Dec 07, 2016	MWF	11:00 am - 11:50 am	Transportation Building 101	Mouschovias
51498	CS 173 ADD	Discrete Structures	Urbana-Champaign	3.000	1U	Aug 22, 2016	Dec 07, 2016	R	5:00 pm - 5:50 pm	Siebel Center for Comp Sci 1111	Fleck
30102	CS 173 AL1	Discrete Structures	Urbana-Champaign	0.000	1U	Aug 22, 2016	Dec 07, 2016	TR	9:30 am - 10:45 am	Electrical & Computer Eng Bldg 1002	Fleck
35919	CS 225 AL2	Data Structures	Urbana-Champaign	4.000	1U	Aug 22, 2016	Dec 07, 2016	MWF	2:00 pm - 2:50 pm	Electrical & Computer Eng Bldg 1002	Heeren
58758	CS 225 AYM	Data Structures	Urbana-Champaign	0.000	1U	Aug 22, 2016	Dec 07, 2016	F	5:00 pm - 6:50 pm	Siebel Center for Comp Sci 0224	Heeren
47039	MATH 241 BDA	Calculus III	Urbana-Champaign	0.000	1U	Aug 22, 2016	Dec 07, 2016	TR	8:00 am - 8:50 am	Altgeld Hall 143	TBA
47058	MATH 241 BL2	Calculus III	Urbana-Champaign	4.000	1U	Aug 22, 2016	Dec 07, 2016	MWF	12:00 pm - 12:50 pm	Altgeld Hall 314	TBA
34734	PHYS 212 A2	University Physics: Elec & Mag	Urbana-Champaign	4.000	1U	Aug 22, 2016	Dec 07, 2016	TR	2:00 pm - 2:50 pm	Loomis Laboratory 141	Grosse Perdekamp
52447	PHYS 212 D1B	University Physics: Elec & Mag	Urbana-Champaign	0.000	1U	Aug 22, 2016	Dec 07, 2016	M	8:00 am - 9:50 am	Loomis Laboratory 32	TBA
45661	PHYS 212 L3B	University Physics: Elec & Mag	Urbana-Champaign	0.000	1U	Aug 22, 2016	Dec 07, 2016	W	8:00 am - 9:50 am	Loomis Laboratory 234	TBA'''
print(course_info_converter(mine))