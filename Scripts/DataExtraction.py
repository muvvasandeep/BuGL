# Importing required libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from time import sleep
from getpass import getpass
import time
import sys
import os
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict as dd
import json

options = Options()
options.add_argument("--disable-notifications")
# For Windows
# Path to the location of chrome driver
# Opens an instance of chrome driver using selenium web driver
driver = webdriver.Chrome(r"C:\Users\muvva\Documents\chromedriver.exe",chrome_options=options)

# For Ubuntu
# Path to the location of chrome driver
# Opens an instance of chrome driver using selenium web driver
#driver = webdriver.Chrome(r"/home/users/CS16B017/Downloads/chromedriver_linux64/chromedriver",chrome_options=options)

# repo_issues -> stores the metadata of the pull requests
# Metadata includes url of pull request, id of pull request, summary, description and info of files changed (i.e., path to files changed and number of files changed in each file)
repo_issues = {}

# This function is to get the metadata of open issues
def open_issues_info(open_pages,github_link):
        #repo_open_issues is used to store the metadata of open issues of a particular github repository
	repo_open_issues = {}
	k = 0 # k is used as a serial number of the open issues
	# for loop is runned for all the pages of open issues
	for i in range(1,open_pages+1):
                # General form of github link for open issues
		page_url = github_link + 'issues?page='+str(i)+'&q=is%3Aissue+is%3Aopen'
		# Get the link using chrome driver
		driver.get(page_url)
		sleep(1)
		try:
                        # All the links of open issues are stored in the variable repo_open_url (array)
			repo_open_url = [x.get_attribute('href') for x in driver.find_element_by_xpath('//div[@aria-label="Issues"]').find_elements_by_class_name('h4')]
			print(len(repo_open_url))
			for j in repo_open_url:
				k = k+1
				try:
                                        # Get the link of open issues
					driver.get(j)
					sleep(1)
					opened_by = driver.find_element_by_class_name('TableObject-item--primary')
					# Stores Issue reporting time
					reporting_timestamp = opened_by.find_element_by_xpath('relative-time').get_attribute('datetime')
					temp_issue = {}
					# url of open issue
					temp_issue['issue_url'] = j
					# issue_id of open issue
					temp_issue['issue_id'] = driver.find_element_by_class_name('gh-header-number').text
					# Summary of the issue
					temp_issue['issue_summary'] = driver.find_element_by_class_name('js-issue-title').text
					# Description of the issue
					temp_issue['issue_description'] = driver.find_elements_by_class_name('js-comment-container')[0].text
					# Status of the issue (Open)
					temp_issue['issue_status'] = driver.find_element_by_class_name('State').text
					# Storing the reporting time of the issue
					temp_issue['issue_reporting_time'] = reporting_timestamp
					repo_open_issues[str(k)] = temp_issue
				except:
					print(j)
		except:
			print("Issues label not found")
		print("open issues "+ str(i) + "th page done")
	repo_issues["open_issues"] = repo_open_issues

# This function is to get the metadata of closed issues
def closed_issues_info(closed_pages,github_link):
        #repo_closed_issues is used to store the metadata of closed pull requests of a particular github repository
	repo_closed_issues = {}
	k = 0 # k is used as a serial number of the closed issues
	# for loop is runned for all the pages of closed issues
	count = 0
	for i in range(1,closed_pages+1):
                # General form of github link for closed issues
		page_url = github_link + 'issues?page='+str(i)+'&q=is%3Aissue+is%3Aclosed'
		# Get the link using chrome driver
		driver.get(page_url)
		sleep(1)
		try:
                        # All the links of closed issues are stored in the variable repo_closed_url (array)
			repo_closed_url = [x.get_attribute('href') for x in driver.find_element_by_xpath('//div[@aria-label="Issues"]').find_elements_by_class_name('h4')]
			for j in repo_closed_url:
				try:
					k = k+1
					# Get the link of closed issue
					driver.get(j)
					sleep(1)
					opened_by = driver.find_element_by_class_name('TableObject-item--primary')
					# Stores the ID of the pull request that resolved the issue
					fixed_by = (opened_by.text).split('Fixed by ')
					# Stores Issue reporting time
					reporting_timestamp = opened_by.find_element_by_xpath('relative-time').get_attribute('datetime')
					pull_request_id = ""
					if(len(fixed_by)==2):
						pull_request_id = (fixed_by[1].split(' '))[0]
					temp_issue = {}
					# url of closed issue
					temp_issue['issue_url'] = j
					# ID of closed issue
					temp_issue['issue_id'] = driver.find_element_by_class_name('gh-header-number').text
					# Summary of closed issue
					temp_issue['issue_summary'] = driver.find_element_by_class_name('js-issue-title').text
					# Description of closed issue
					temp_issue['issue_description'] = driver.find_elements_by_class_name('js-comment-container')[0].text
					# Status of closed issue (Closed)
					temp_issue['issue_status'] = driver.find_element_by_class_name('State').text
					# Reporting time of the issue
					temp_issue['issue_reporting_time'] = reporting_timestamp
					# ID of pull request that closed the issue
					temp_issue['fixed_by'] = pull_request_id
					# If the issue is closed by merging of a pull request
					if pull_request_id != "" :
                                                # Get the link of pull request using chrome driver
						driver.get(github_link + 'pull/' + pull_request_id.split('#')[1])
						sleep(1)
						opened_by = driver.find_element_by_class_name('TableObject-item--primary')
						# Stores the time at which the pull request was merged (time at which issue is closed)
						fixed_timestamp = opened_by.find_element_by_xpath('relative-time').get_attribute('datetime')
						# Summary of the pull request
						temp_issue['pull_request_summary'] = driver.find_element_by_class_name('js-issue-title').text
						# Description of the pull request
						temp_issue['pull_request_description'] = driver.find_elements_by_class_name('js-comment-container')[0].text
						# Status of the pull request
						temp_issue['pull_request_status'] = 'Merged'
						# Time at which issue id fixed
						temp_issue['issue_fixed_time'] = fixed_timestamp
						# Get the information of files changed
						driver.get(github_link + 'pull/' + pull_request_id.split('#')[1]+'/files')
						sleep(1)
						files_changed = driver.find_elements_by_class_name('file-info')
						# Stores the metadata like files changed and number of lines changed in the corresponding file
						files = []
						count = count + 1
						for z in files_changed:
							files.append(list((z.text).split(' ')))
						temp_issue['files_changed'] = files
					else:
                                                # issue is not closed by merging a pull request then initalize the metadata with empty string for consistency
						temp_issue['pull_request_summary'] = ""
						temp_issue['pull_request_description'] = ""
						temp_issue['pull_request_status'] = ""
						temp_issue['issue_fixed_time'] = ""
						temp_issue['files_changed'] = []
					repo_closed_issues[str(k)] = temp_issue
				except:
					print(j)
		except:
			print("Issues label not found")
		print("closed issues "+ str(i) + "th page done")
		print("Number of bugs in page " + str(i) + "of " + github_link + "is " + str(count))
	repo_issues["closed_issues"] = repo_closed_issues

def get_issues_info(github_link):
	# Url of issues of a repository
	issues_url = github_link + 'issues'
	# Get the url of pull requests of a repository
	driver.get(issues_url)
	# Store the links to open and closed issues
	issues = driver.find_elements_by_xpath('//*[@id="js-issues-toolbar"]/div/div[1]/div/a')
	open_issues, closed_issues = issues[0].get_attribute('href'), issues[1].get_attribute('href')
	# Get meta data of Open issues
	driver.get(open_issues)
	sleep(1)
	try:
                # Number of pages of open issues
		pages = driver.find_element_by_class_name('pagination').find_elements_by_xpath('a')
		open_pages = int(pages[len(pages)-2].text)
	except:
		open_pages = 1
	sleep(1)
	# Get the metadata of the open issues
	open_issues_info(open_pages,github_link)
	# Traversing the open issues done
	print("Open issues done")
	# Get metadata of closed issues
	driver.get(closed_issues)
	sleep(1)
	try:
                # Number of pages of closed issues
		pages = driver.find_element_by_class_name('pagination').find_elements_by_xpath('a')	
		closed_pages = int(pages[len(pages)-2].text)
	except:
		closed_pages = 1
	sleep(1)
	# Get the metadata of closed issues
	closed_issues_info(closed_pages,github_link)
	# Traversing the closed issues done
	print("closed issues done")

# Dataset.json consists of information of github repositories
# With Key being name of the repository and value being the link to the github repository
# Opens the Dataset.json file then loads and stores the key value pairs in a variable named dataset_links (dictionary)
f = open('Dataset.json')	#Github links of the data set is present in this file
dataset_file = f.read()
dataset_links = json.loads(dataset_file)	# github links stored in this variable

# 'for' loop runs over all the key-value pairs for getting the required metadata from each repository
for i in dataset_links:
	print(str(dataset_links[i])+' started')
	# Started processing the repository with the name 'i' (key)
	# Gets the metadata required for the repository named 'i'
	get_issues_info(dataset_links[i])
	# Strores the metadata in a json file
	with open(str(i)+'.json','w') as f:
		json.dump(repo_issues,f)
	# Done processing the repository with the name 'i'
	print(str(dataset_links[i])+' done')
	# Initialising the variable with empty dictionary for processing the other repository
	repo_issues = {}
