from google.appengine.ext import ndb

class Course(ndb.Model):
	subject = ndb.StringProperty(required=True)
	number = ndb.IntegerProperty(required=True)
	hw = ndb.StringProperty()
	grade = ndb.StringProperty()



def course_info_converter(text):
	instructions = '''Instructions

Open up the "Student Schedule - Concise" page on UI-Integrate Self-Service. (Registration & Records → Registration → Student Schedule - Concise)
Copy the class table and paste it into the form below.
Each line should look something like this: 39725	GER 102 B	Beginning German II	Urbana-Champaign	4.000	1U	Aug 22, 2011	Dec 07, 2011	MTWR	9:00 am - 9:50 am	Foreign Languages Building G46	Castle

Any lines that can't be understood, including ones where class times are "TBA", will be ignored.'''
	for line in text.splitlines():
		print(line)


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