import webbrowser

class Course():
	"""docstring for Course"""
	def __init__(self, ID, website_url, homework_url, grade_url):
		self.ID = ID
		self.main_website = website_url
		self.hw_url = homework_url
		self.grade_url = grade_url
		email = "gmail.com.....?"

	def check_grades(self):
		webbrowser.open(self.grade_url)

		