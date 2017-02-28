import json
import requests
import config

headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/4.7.1 (iPhone; iOS 9.2; Scale/2.00)",
}

"""
Known endpoints:
	tested:
		-- https://api.gotinder.com/auth
		-- https://api.gotinder.com/user/recs
		-- https://api.gotinder.com/user/matches/_id
		-- https://api.gotinder.com/user/_id
		-- https://api.gotinder.com/updates
		-- https://api.gotinder.com/profile
		-- https://api.gotinder.com/meta
		-- https://api.gotinder.com/user/ping
		-- https://api.gotinder.com/report/{_id}
		-- https://api.gotinder.com/{like|pass}/{_id}
	untested:
		https://api.gotinder.com/group/{like|pass}/{id}
		https://api.gotinder.com/passport/user/travel
"""

# def get_auth_token(fb_auth_token, fb_user_id):
# 	url = config.host + '/auth'
# 	req = requests.post(url,
#     	headers=headers,
#     	data=json.dumps({'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
#     	)
# 	try:
# 		tinder_auth_token = req.json()["token"]
# 		headers.update({"X-Auth-Token": tinder_auth_token})
# 		return tinder_auth_token
# 	except:
# 		return {"error": "could not authorize"}
#
# print("Getting your Auth Token...")
# tinder_auth_token = get_auth_token(config.fb_auth_token, config.fb_user_id)
# if "error" in tinder_auth_token:
# 	print("Something went wrong!")
# else:
# 	print("Success!")

def get_auth_token(csv):
	url = config.host + '/auth'
	for i in csv:
		row = readrow()
		if row[2] == 1:
			i ++
		else:
			fb_auth_token = row[0]
			fb_user_id = row[1]
			response = requests.post(url,
								headers=headers,
								data=json.dumps({'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
								)
			tinder_auth_token = response.json()["token"]
			headers.update({"X-Auth-Token": tinder_auth_token})
			return tinder_auth_token
			row.rewrite(row[2] = 1)
			break


get_auth_token('accesstokens.csv') # get first available token using accesstokens.csv, update headers , and mark it with 1 (which mean used)


# INPUT : None
# OUTPUT: A dict of the recommended users to swipe on
# I think recommended means the users who have already 'liked' you
# r.json()["results"][index]["name"] == the person at index's name
def get_recommendations():
	try:
		r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
		return r.json()
	except:
		return {"error": "could not retrieve recommendations"}

		##### COULD DO LIKE IF "ERROR" IN r.json() then print this else do this.


# INPUT: last_activity_date -> the date from which you want to see updates
#							-> defaults to "" which means from the beginning of time
# 		should be of the form ______________________
# OUTPUT: A dict of all updates since given activity date
# NOTES: You can do this to get messages sent, all matches...
def get_updates(last_activity_date=""):
	r = requests.post('https://api.gotinder.com/updates',
		headers=headers,
		data=json.dumps({"last_activity_date": last_activity_date}))
	return r.json()

# Returns the following keys:
## ['squads_only', 'squads_discoverable', 'instagram', 
## 'gender', 'bio', 'birth_date', 'name', 'interested_in', 
## 'location', 'gender_filter', 'age_filter_min', 'photos', 
## 'ping_time', 'squad_ads_shown', 'discoverable', 'facebook_id', 
## 'pos', 'can_create_squad', 'age_filter_max', 'schools', 
## 'pos_info', 'jobs', 'blend', 'distance_filter', '_id', 
## 'create_date']
def get_self():
	url = config.host + '/profile'
	r = requests.get(url, headers=headers)
	return r.json()


# 18 >= age_filter_min <= 46
# 22 >- age_filter_max <= 55
# age_filter_min <= age_filter_max - 4
# gender 0 = looking for males, gender 1 = looking for females
# 1 <= distance_filter >= 100 in miles
def change_preferences(age_filter_min, age_filter_max, gender, distance_filter):
	url = config.host + '/profile'
	preferences = {"age_filter_min": age_filter_min,
		 "gender": gender,
		 "age_filter_max": age_filter_max, 
		 "distance_filter": distance_filter}
	r = requests.post(url, headers=headers, data=json.dumps(preferences))
	return r.json()

# Returns metadata containing the following keys:
## ['globals', 'client_resources', 'versions', 'purchases', 
## 'status', 'groups', 'products', 'rating', 'tutorials', 
## 'travel', 'notifications', 'user']
def get_meta():
	url = config.host + '/meta'
	r = requests.get(url, headers=headers)
	return r.json()

def get_ping(lat, lon):
	headers.update({"X-Auth-Token": tinder_auth_token})
	url = config.host + '/user/ping'
	r = requests.post(url, headers=headers, data={"lat": lat, "lon": lon})
	return r.json()

# Input: person_id --> the tinder_id of a user not yourself
# Output: The person_id's corresponding profile information
#		bio, pictures, gender, birthdate...

# NEED A FUNCTION TO GET THAT PERSON'S ID FROM THE UPDATES CALL
def get_person(person_id):
	url = config.host + '/user/%s' % person_id
	r = requests.get(url, headers=headers)
	return r.json()

# INPUT: match_id : string -> 
#	this is different than the person's person_id
#	the match_id is typically an id for the chat
# 	usually, match_id = person1_id ^ person2_id
# 	get_updates["matches"][0]["_id"] is the match_id for match 0, the index
# INPUT: msg : string -> 
#	Desired message to be sent
# OUTPUT: Success or Failure msg
def send_msg(match_id, msg):
	url = config.host + '/user/matches/%s' % match_id
	r = requests.post(url, headers=headers, data=json.dumps({"message": msg}))
	return r.json()

def superlike(person_id):
	url = config.host + '/like/%s/super' % person_id
	r = requests.get(url, headers=headers)
	return r.json()	

def like(person_id):
	url = config.host + '/like/%s' % person_id
	r = requests.get(url, headers=headers)
	return r.json()

def dislike(person_id):
	url = config.host + '/pass/%s' % person_id
	r = requests.get(url, headers=headers)
	return r.json()

# Cause must be one of the given options
# I WILL CHECK THESE LATER
def report(person_id, cause):
	url = config.host + '/report/%s' % person_id
	r = requests.post(url, headers=headers, data={"cause": cause})
	return r.json()






