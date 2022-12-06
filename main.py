from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys
import time
import re


#First we need to accept rules
def click_accept():
	time.sleep(0.1)
	accept_click = driver.find_element(By.XPATH, "//*[@class='btn btn--blue right']")
	accept_click.click()


def private_shows_download(info_location):
	for html_info in info_location:
	#print('Downloading information from : '+  profile)
		html_info = html_info.get_attribute('outerHTML')
		info = BeautifulSoup(html_info, features="html.parser")
		services = info.find_all("div", {"class": "streamSelect__content"})
		services = info.find_all('h5')
		services = list(services)
	return services	


def findings(services, profile, found_search_words):
	string_services = []
	#add every private show to the list
	for service in services:
		string_services.append(str(service))
	search_words = lower_upper_keyword()

	result = []
	#finding the keyword in the menu
	for string_service in string_services: 	
		for search_word in search_words:
			if search_word in string_service:
				result.append(f"We found the keyword : {search_word}, in the URL :{profile}")
			else:
				pass				

	return result			


def read_profiles(profile_urls):
	#### BIG, BIG MESS #####
			index_profile = 0
			found_search_words = 0
			for profile in profile_urls:
				index_profile += 1
				driver.get(profile)
				#Waiting for JS to pop up
				time.sleep(0.3)
				#Locating the privet show menu
				info_location = driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div[2]/form/div/div')
				services = private_shows_download(info_location)

				count_foundings = findings(services, profile, found_search_words)

				for count_founding in count_foundings:
					print(count_founding)
					found_search_words += 1

			driver.close()
					
			if found_search_words == 0:
				print('\nSorry...Found nothing,try again later...')
				print(f"Total profiles online : {index_profile}")
			else:
				print(f"\n\tTotal profiles online : {index_profile}")
				print(f"\tTotal founds : {found_search_words} \n")				

		
def main():
	try:
		start = time.time()	
		print('****************** starting... ****************** \n')	
		
		driver.get(url)		
		click_accept()
		
		print('Searching...\n')
		# Getting the URLs from each streamer.
		profile_urls = get_profiles()
		# Handling of the URLs
		read_profiles(profile_urls)
		# for profile_111 in profile_urls:
		# 	print(profile_111)
		print('******************     end     ****************** ')
		stop = time.time()
		print(stop - start)

	except:
		print("Please make sure that Chrome browser is installed on your PC ")

	finally:
		driver.quit()


def saved_keywords():
	#Reading the keywords from text file
	try:
		with open('keywords.txt', 'r') as f:
			keywords_saved_list = []
			data = f.readlines()
			if not data:
				print('Specify the keywords in "keywords.txt" ')
			else:
				for i_list in data:
					if i_list != '\n':
						#Removing the \n etc. from the readlines function and appending it to the main list.
						i_list = i_list.rstrip()
						keywords_saved_list.append(i_list)
					else:
						pass	
				#print(keywords_saved_list)
				return keywords_saved_list		
	
	except:
		with open('keywords.txt', 'w') as f:
			print('keywords.txt has been created....')


def get_profiles():
	#Find all streamer links.
	streams_list = []
	streams = driver.find_elements(By.XPATH, "//*[@class='streamList small-block-grid-2 medium-block-grid-3 large-block-grid-4']")
	streams = driver.find_elements(By.TAG_NAME, 'a')
	for stream in streams:
		all_streamers = stream.get_attribute('href')
		streams_list.append(all_streamers)
	#Removing the constant links on the website from the list.
	all_links = streams_list[14:-8]
	return all_links


def lower_upper_keyword():
	##Loading the keywords form the function "saved_keywords()" which reads the values from a file.
	search_words = saved_keywords()	
	#lowercase words
	search_lower = list(map(str.lower, search_words))
	search_words.extend(search_lower)
	#uppercase words
	search_up = list(map(str.upper, search_lower))
	search_words.extend(search_up)
	# print(search_words)
	return search_words

	
if __name__ == '__main__':
	##### Selenium Options #####
		while True:
			
			url = 'https://showup.tv/'

			options = webdriver.ChromeOptions()
			options.add_argument('--headless')
			#Stackoverflow example of bypassing the output form chromedriver on Windows OS(NOt testet yet!)
			options.add_experimental_option("excludeSwitches", ["enable-logging"])
			#chrome_options.add_argument('--user-agent=""')
			
			driver = webdriver.Chrome('chromedriver', options=options)

			main()
			
			answer = input('Press enter to exit...')

			if answer == 'r':
				pass
			else:
				sys.exit(0)		