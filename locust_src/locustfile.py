import random
import json
from locust import HttpLocust, TaskSet, task, seq_task, TaskSequence
from test_case_id_utils import COUNTY_MAP, CASE_ID_LIST_DICT
from datetime import datetime


def read_commons():
	file_ptr = open('current.txt', 'r')
	data = file_ptr.readline()
	file_ptr.close()
	return data.split('_')


def get_courtcase(self):
	# key = random.randint(1,3)
	key = 3
	# getting state and county key
	state_key, county_key = COUNTY_MAP.get(key, None).split("-")
	# getting the case ID list
	case_id_list = CASE_ID_LIST_DICT.get(key, None)
	# selecting a random case id
	random_case_id = case_id_list[random.randint(0, (len(case_id_list) - 1))]
	# state_key, county_key, random_case_id = read_commons()
	# making request
	print("Requesting for case id {}".format(random_case_id))
	s = self.client.post("/codaxtr/rest/get_courtcase/", {"state": state_key, "county": county_key, "unicourt_unique_id": "test_account", "case_id": random_case_id})
	print("response received for case id {} at {}".format(random_case_id, datetime.now()))


def track_case(self):
	key = 3
	# getting state and county key
	state_key, county_key = COUNTY_MAP.get(key, None).split("-")
	# getting the case ID list
	case_id_list = CASE_ID_LIST_DICT.get(key, None)
	# selecting a random case id
	random_case_id = case_id_list[random.randint(0, (len(case_id_list) - 1))]
	# state_key, county_key, random_case_id = read_commons()
	# making request
	print("Requesting for case id {}".format(random_case_id))
	# making request
	d = self.client.post("/codaxtr/rest/track_cases/", data=json.dumps(
		{"priority": 1, "state": state_key, "county": county_key, "case_id_list": [int(random_case_id)],
		 "unicourt_unique_id": "unicourt", "webhook": {
			"DOCKET PROCESSING": {"ON-FAILURE": ["UNICOURTURL-ON-FAILURE"],
					      "ON-SUCCESS": ["UNICOURTURL-ON-SUCCESS"]},
			"REFRESH CASE BY CASE NUMBER": {"ON-FAILURE": ["UNICOURTURL-ON-FAILURE"],
							"ON-SUCCESS-NO-UPDATE": [
								"RESEARCHERURL-ON-SUCCESS-NO-UPDATE",
								"UNICOURTURL-ON-SUCCESS-NO-UPDATE"],
							"ON-SUCCESS-WITH-UPDATE": [
								"UNICOURT-ON-SUCCESS-WITH-UPDATE"]}}}),
			  headers={"Content-Type": "application/json"})
	print(d.text)

class MyTasks(TaskSequence):
	tasks = [track_case]

	# @seq_task(1)
	# def get_api_status(self):  # generating key
	# 	file_ptr = open('current.txt', 'w')
	# 	# generating key
	# 	key = 3
	# 	# getting state and county key
	# 	state_key, county_key = COUNTY_MAP.get(key, None).split("-")
	# 	# getting the case ID list
	# 	case_id_list = CASE_ID_LIST_DICT.get(key, None)
	# 	# selecting a random case id
	# 	random_case_id = case_id_list[random.randint(0, (len(case_id_list) - 1))]
	#
	# 	file_ptr.write("{}_{}_{}".format(state_key, county_key, random_case_id))
	# 	file_ptr.close()
	#
	# 	state_key, county_key = COUNTY_MAP.get(key, None).split("-")
	# 	self.client.post("/codaxtr/rest/get_api_status/",
	# 		      {"state": state_key, "county": county_key, "unicourt_unique_id": "test_account",
	# 		       "api_name": "track_case"})
	#
	# @seq_task(2)
	# def track_case(self):
	# 	# getting state and county key
	# 	state_key, county_key, random_case_id = read_commons()
	# 	# making request
	# 	d = self.client.post("/codaxtr/rest/track_cases/", data=json.dumps(
	# 		{"priority": 1, "state": state_key, "county": county_key, "case_id_list": [int(random_case_id)],
	# 		 "unicourt_unique_id": "unicourt", "webhook": {
	# 			"DOCKET PROCESSING": {"ON-FAILURE": ["UNICOURTURL-ON-FAILURE"],
	# 					      "ON-SUCCESS": ["UNICOURTURL-ON-SUCCESS"]},
	# 			"REFRESH CASE BY CASE NUMBER": {"ON-FAILURE": ["UNICOURTURL-ON-FAILURE"],
	# 							"ON-SUCCESS-NO-UPDATE": [
	# 								"RESEARCHERURL-ON-SUCCESS-NO-UPDATE",
	# 								"UNICOURTURL-ON-SUCCESS-NO-UPDATE"],
	# 							"ON-SUCCESS-WITH-UPDATE": [
	# 								"UNICOURT-ON-SUCCESS-WITH-UPDATE"]}}}),
	# 			  headers={"Content-Type": "application/json"})
	# 	print(d.text)

	# @seq_task(1)
	# def get_courtcase(self):
	# 	key = 3
	# 	# getting state and county key
	# 	state_key, county_key = COUNTY_MAP.get(key, None).split("-")
	# 	# getting the case ID list
	# 	case_id_list = CASE_ID_LIST_DICT.get(key, None)
	# 	# selecting a random case id
	# 	random_case_id = case_id_list[random.randint(0, (len(case_id_list) - 1))]
	# 	# state_key, county_key, random_case_id = read_commons()
	# 	# making request
	# 	self.client.post("/codaxtr/rest/get_courtcase/", {"state": state_key, "county": county_key, "unicourt_unique_id": "test_account", "case_id": random_case_id})
		# self.client.post("/codaxtr/rest/get_courtcase/", {"state": state_key, "county": county_key, "unicourt_unique_id": "test_account", "case_id": int(random_case_id)})


class Users(HttpLocust):
	task_set = MyTasks
	min_wait = 1
	max_wait = 300
