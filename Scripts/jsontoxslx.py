import json
import xlsxwriter
import os

total = 0

#Path of the folder where json files with the metadata of the issues are present 
folder_path = "C:/Users/muvva/Desktop/BTP/BTP_Dataset/Scraping_Files/newdataset/C/JSON"
for file in os.listdir(folder_path):
        if file.endswith('.json'):
                # Opens the json files with the metadata
                f = open(file)	#Github links of the data set is present in this file
                dataset_file = f.read()
                # Loads the metadata from the josn file
                repo_issues = json.loads(dataset_file)
                for i in repo_issues['open_issues']:
                        repo_issues['open_issues'][i]['fixed_by'] = ''
                        repo_issues['open_issues'][i]['pull_request_summary'] = ''
                        repo_issues['open_issues'][i]['pull_request_description'] = ''
                        repo_issues['open_issues'][i]['pull_request_status'] = ''
                        repo_issues['open_issues'][i]['issue_fixed_time'] = ''
                        repo_issues['open_issues'][i]['files_changed'] = []
                # Gets the name of the repository (json file name)
                workbook = xlsxwriter.Workbook(file[:-5]+'.xlsx')
                # Used for storing the data in xlsx file
                worksheet = workbook.add_worksheet()
                cvb=0 # S. No of the data element

                # Columns of the xlsx file
                data=[["Sr. No","Issue_URL","Issue_ID","Issue_Summary","Issue_Description","Issue_Status","fixed_by","PullRequest_Summary","PullRequest_Description","PullRequest_Status","Issue_Fixed_Time","Files_Changed"]]

                # Appends the open issues metadata
                for i in repo_issues["open_issues"]:
                        cvb+=1
                        data.append([str(cvb),repo_issues["open_issues"][i]["issue_url"],repo_issues["open_issues"][i]["issue_id"],repo_issues["open_issues"][i]["issue_summary"],repo_issues["open_issues"][i]["issue_description"],repo_issues["open_issues"][i]["issue_status"],repo_issues["open_issues"][i]["fixed_by"],repo_issues["open_issues"][i]["pull_request_summary"],repo_issues["open_issues"][i]["pull_request_description"],repo_issues["open_issues"][i]["pull_request_status"],repo_issues["open_issues"][i]["issue_fixed_time"],str(repo_issues["open_issues"][i]["files_changed"])])
                # Appends the closed issues metadata
                for i in repo_issues["closed_issues"]:
                        cvb+=1
                        data.append([str(cvb),repo_issues["closed_issues"][i]["issue_url"],repo_issues["closed_issues"][i]["issue_id"],repo_issues["closed_issues"][i]["issue_summary"],repo_issues["closed_issues"][i]["issue_description"],repo_issues["closed_issues"][i]["issue_status"],repo_issues["closed_issues"][i]["fixed_by"],repo_issues["closed_issues"][i]["pull_request_summary"],repo_issues["closed_issues"][i]["pull_request_description"],repo_issues["closed_issues"][i]["pull_request_status"],repo_issues["closed_issues"][i]["issue_fixed_time"],str(repo_issues["closed_issues"][i]["files_changed"])])
                # Number of issues closed by pull requests
                temp_total = len([i for i in repo_issues['closed_issues'] if repo_issues['closed_issues'][i]['pull_request_status']=='Merged'])
                # Total number of issues closed by pull requests
                total += temp_total
                print(file,temp_total)
                # Store the data in xlsx file
                for i in range(0,len(data)):
                        worksheet.write(i,0,data[i][0])
                        worksheet.write(i,1,data[i][1])
                        worksheet.write(i,2,data[i][2])
                        worksheet.write(i,3,data[i][3])
                        worksheet.write(i,4,data[i][4])
                        worksheet.write(i,5,data[i][5])
                        worksheet.write(i,6,data[i][6])
                        worksheet.write(i,7,data[i][7])
                        worksheet.write(i,8,data[i][8])
                        worksheet.write(i,9,data[i][9])
                        worksheet.write(i,10,data[i][10])
                        worksheet.write(i,11,data[i][11])

                workbook.close()
print(total)
