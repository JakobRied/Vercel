from bs4 import BeautifulSoup  
import requests, webbrowser

loginurl = "https://portal.windhoekcc.org.na/Services/Core/User/Login?ReturnUrl=%2FServices%2FStatements%2FAccounts" 
loggedinurl = "https://portal.windhoekcc.org.na/Services/Statements/Accounts"
verificationurl = "https://portal.windhoekcc.org.na/Services/TaxiVerification"

def verification_request(number):
	with requests.session() as s:
		##get the RequestVerificationToken
		home_page = s.get(loginurl)
		soup = BeautifulSoup(home_page.content, "html.parser")
		rvt = soup.find("input", attrs={"name" : "__RequestVerificationToken"})['value']

		payload = { 
		"Email": "jakobried0@gmail.com", 
		"Password": "Weichering#1",
		"__RequestVerificationToken": rvt,
		"RememberMe": "false"
		} 

		response = s.post(loginurl, data=payload)
		print(response)

		##Request to Verification Page
		verification_page = s.get(verificationurl)
		soup = BeautifulSoup(verification_page.content, "html.parser")
		rvt = soup.find("input", attrs={"name" : "__RequestVerificationToken"})['value']

		request_payload = {
			"__RequestVerificationToken": rvt,
			"DistinguishedNumber": number
		}

		r = s.post(verificationurl, data = request_payload)
		versoup = BeautifulSoup(r.content, "html.parser")

		##write to file
		f = open('response.html','w')
		f.write(r.text)
		f.close()
		
		
		""" Alternative for searching soup object
		if len(soup.find_all(text=lambda text: text and "The Taxi Number format is invalid" in text)) == 0:
			return False"""

		paragraph = versoup.find("div", class_="alert alert-warning alert-dismissible fade show")
		if(paragraph == None):
			print("Taxi is registered!")
			return True
		
		else:
			print("Taxi is not registered. Report that bastard!")
			return False

