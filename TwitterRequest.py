
BASEURL = "https://twitter.com/search?"

class TwitterRequest:

	def __init__(self,newSearchTerms):
		searchTerms = newSearchTerms
		self.url = BASEURL + "q="
		searchTerms.split()
		for term in searchTerms:
			self.url =self.url + term + "%20"
		self.url =self.url + "&src=typd"

	def changeTerms(newSearchTerms):
		self.url = BASEURL + "q="
		newSearchTerms.split()
		for term in newSearchterms:
			self.url =self.url + term + "%20"
		self.url =self.url + "&src=typd"

	def addTerms(addedSearchTerms):
		self.url = BASEURL + "q="
		self.url.split("&",1)
		addedSearchTerms.split( )
		self.url =self.url + "%20"
		for term in addedSearchterms:
			self.url =self.url + term + "%20"
		self.url =self.url + "&src=typd"
