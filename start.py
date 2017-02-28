from datetime import date, timedelta, datetime
from threading import Thread
import tinder_api as api
import messages

match_info = {}
my_locations = []
headers = {'sdsd'}

def get_match_info():
	matches = api.get_updates()['matches']
	name_dict = {}
	for match in matches[:len(matches) - 2]:
		try:
			PERSON = match['person']
			name = PERSON['name']
			person_id = PERSON['_id'] # for looking up profile
			match_id = match['id'] # for sending messages
			person_json = api.get_person(person_id)
			ping_time = PERSON['ping_time']
			message_count = match['message_count']
			photos = get_photos_by_person_id(person_json)
			bio = PERSON['bio']
			gender = PERSON['gender']
			distance = person_json['results']['distance_mi']
			name_dict[person_id] = {
			"name": name,
			"ping_time": ping_time,
			"match_id": match_id,
			"message_count": message_count,
			"photos": photos,
			"bio": bio,
			"gender": gender,
			"distance": distance
			}
		except:
			continue
	return name_dict

def get_my_locations(file):
    f = file.read(file)
    global my_locations
    i = 0
    for row in f:
        if i == 3:
            break
        content = readrow(row)
        if content[1] == 1:
            row ++
        else:
            location = content[0]
            my_locations.append(location)
            f.updaterow[1] == 1
            i ++


def select_msg(match,offer_id):
    message_count = match['message_count']
    if message_count <= 2:
        msg = greeting.random()
    if message_count > 2:
        msg = messages.offer_message[offer_id]
    return msg



get_my_locations('locations.csv') # получаем 3 случайных локации из файла и записываем в список my_locations
for location in my_locations:
    try:
        lat = location.split(":")[0]
        lon = location.split(":")[1]
        api.get_ping(lat,lon)
        matches = get_match_info()
        for match in matches:
            try:
                match_id = matches[i]['match_id']
                offer_id = 1
                text = select_msg(match_id,offer_id)
                api.send_msg(match_id, text)
            except:
                continue
        rec = api.get_recommendations()
        i = 0
        for user in rec:
            try:
                if i%3=0:
                    api.dislike(user["person_id"])
                else:
                    api.like(user["person_id"])
                i ++
            except:
                continue
    except:
        break



# matchthread.join()

# Upon starting the program i should start a separate thread that basically begins get_matches
# so that all the data is stored locally after about a minute but behind the scenes.


# It is probably a good idea to
# go through each match and create a dict from
# name -> match_id
# and then create another thing that will list each matches name
