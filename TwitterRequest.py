
BASEURL = "https://twitter.com/search?"

class TwitterRequest:

	def __init__(self,newSearchTerms):
		searchTerms = newSearchTerms.split()
		self.url = BASEURL + "q="
		for term in searchTerms:
			self.url = self.url + term + "%20"
		self.url =self.url + "&src=typd"

	def changeTerms(self,newSearchTerms):
		searchTerms = newSearchTerms.split()
		self.url = BASEURL + "q="
		for term in searchTerms:
			self.url =self.url + term + "%20"
		self.url =self.url + "&src=typd"

	def addTerms(self,addedSearchTerms):
		searchTerms = addedSearchTerms.split()
		self.url = BASEURL + "q="
		self.url.split("&",1) #TODO: working?
		self.url = self.url + "%20"
		for term in searchTerms:
			self.url =self.url + term + "%20"
		self.url =self.url + "&src=typd"

	def getURL(self):
		return self.url
