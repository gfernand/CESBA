import http.client, urllib.parse
import json
global my_server_path

my_server_path = 'ewetasker.cluster.gsi.dit.upm.es'


'''
-->CREATERULE

REQUEST:

rule_title(String): Name of the new rule you want to create. Example: "My example rule".
rule_description(String): Decription of your rule. Example: "When users enters GSI (< 2 meters) then show a Notification saying 'Welcome!' "
rule_channel_one (String): Event channel. Example: "Presence Sensor"
rule_channel_two(String): Action channel. Example: "Notification"
rule_event_title(String): Event name. Example: "Presence Detected At Distance Less Than"
rule_action_title(String): Action name. Example: "Show"
rule_place(String): Place where rule is active. Example: "GSI".
rule_creator(String): Username. Example: "Peter".
rule(String): Rule string, which must contain all prefixes with the N3 rule description for EYE. 

Example:

      @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
      @prefix math: <http://www.w3.org/2000/10/swap/math#>.
      @prefix ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/#> .
      @prefix ewe-presence: <http://gsi.dit.upm.es/ontologies/ewe-presence/ns/#>
      @prefix ewe-notification: <http://gsi.dit.upm.es/ontologies/ewe-notification/ns/#>
      @prefix ov: <http://vocab.org/open/#> .

      {
      ?event rdf:type ewe-presence:PresenceDetectedAtDistance.
      ?event!ewe:sensorID string:equalIgnoringCase "A1B2C3" .
      ?event!ewe:distance math:lessThan 2 .
      }
      =>
      {
      ewe-notification:Notification rdf:type ewe-notification:Show;
      ov:message "Welcome!".
      }.


RESPONSE:
{
   "success":"1"
 }


'''

def createRule(rule_title_aux = None, rule_description_aux = None, rule_channel_one_aux = None, rule_channel_two_aux = None, 
	rule_event_title_aux = None, rule_action_title_aux = None, rule_place_aux = None, rule_creator_aux = None, distance_activate_rule_aux = None,
	rule_aux = None):

	beaconId = '1023'

	rule_title = 'Rule' if rule_title_aux is None else rule_title_aux
	rule_description = 'This is a rule' if rule_description_aux is None else rule_description_aux
	rule_channel_one = 'Presence Sensor' if rule_channel_one_aux is None else rule_channel_one_aux
	rule_channel_two = 'Notification' if rule_channel_two_aux is None else rule_channel_two_aux
	rule_event_title = 'Presence Detected At Distance Less Than' if rule_event_title_aux is None else rule_event_title_aux
	rule_action_title = 'Show' if rule_action_title_aux is None else rule_action_title_aux
	rule_place = 'Laboratory' if rule_place_aux is None else rule_place_aux
	rule_creator = 'public' if rule_creator_aux is None else rule_creator_aux
	distance_activate_rule = str(2 if distance_activate_rule_aux is None else distance_activate_rule_aux)
	exampleRule = '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . @prefix math: <http://www.w3.org/2000/10/swap/math#> . @prefix ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/#> . @prefix ewe-presence: <http://gsi.dit.upm.es/ontologies/ewe-presence/ns/#> . @prefix ewe-notification: <http://gsi.dit.upm.es/ontologies/ewe-notification/ns/#> . @prefix ov: <http://vocab.org/open/#> . @prefix string: <http://www.w3.org/2000/10/swap/string#> . { ?event rdf:type ewe-presence:PresenceDetectedAtDistance. ?event ewe:sensorID ?sensorID. ?sensorID string:equalIgnoringCase \'' + beaconId + '\'. ?event!ewe:distance math:lessThan ' + distance_activate_rule + '. } => { ewe-notification:Notification rdf:type ewe-notification:Show; ov:message "Welcome!". }.'
	rule = exampleRule if rule_aux is None else rule_aux
	command = 'createRule'

	params = urllib.parse.urlencode({'rule_title': rule_title, 'rule_description': rule_description, 'rule_channel_one': rule_channel_one,
	'rule_channel_two': rule_channel_two, 'rule_event_title': rule_event_title, 'rule_action_title': rule_action_title, 'rule_place': rule_place,
	'rule_creator': rule_creator, 'rule': rule, 'command': command})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(my_server_path)
	conn.request("POST", "/mobileConnectionHelper.php", params, headers)
	response = conn.getresponse()
	dataB = response.read()
	data = json.loads(str(dataB, 'utf-8'))
	conn.close()
	if data['success'] == '1': 
		return True
	else:
		return False


'''
-->GETCHANNELS

RESPONSE:
[{
         "title":"",
         "description":"",
         "events":[{
            "title":"",
            "prefix":"",
            "rule":"",
            "numParameters":""
         }],
         "actions":[{
            "title":"",
            "prefix":"",
            "rule":"",
            "numParameters":""
         }]
      }]

'''

def getChannels():

	params = urllib.parse.urlencode({'command': 'getChannels'})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(my_server_path)
	conn.request("POST", "/mobileConnectionHelper.php", params, headers)
	response = conn.getresponse()
	dataB = response.read()
	data = json.loads(str(dataB, 'utf-8'))
	conn.close()
	return data


'''
-->GETEVENTS

REQUEST:

inputEvent (String): You have to provide all the prefixes and the input event in N3 for EYE.

Example:

      @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
      @prefix math: <http://www.w3.org/2000/10/swap/math#>.
      @prefix ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/#> .
      @prefix ewe-presence: <http://gsi.dit.upm.es/ontologies/ewe-presence/ns/#> .

      ewe-presence:PresenceSensor rdf:type ewe-presence:PresenceDetectedAtDistance.
      ewe-presence:PresenceSensor ewe:sensorID "A1B2C3".
      ewe-presence:PresenceSensor ewe:distance 1.

user (String): User who sends the input. Example: "Peter"
command (String): "getChannels"

RESPONSE:

      {
         "success":1,
         "actions":
               [{
                  "channel":"",
                  "action":"",
                  "parameter":""
               }]
      }

'''

def getEvents(distance, user_aux = None):

	beaconId = '1023'

	user = 'public' if user_aux is None else user_aux
	inputEvent = '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . @prefix ewe-presence: <http://gsi.dit.upm.es/ontologies/ewe-connected-home-presence/ns/#> . @prefix ewe: <http://gsi.dit.upm.es/ontologies/ewe/ns/#> . @prefix ewe-presence: <http://gsi.dit.upm.es/ontologies/ewe-connected-home-presence/ns/#> . ewe-presence:PresenceSensor rdf:type ewe-presence:PresenceDetectedAtDistance. ewe-presence:PresenceSensor ewe:sensorID \"'+beaconId+'\". ewe-presence:PresenceSensor ewe:distance '+str(distance)+'.'
	
	params = urllib.parse.urlencode({'user': 'public', 'inputEvent': inputEvent, 'command': 'getChannels'})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(my_server_path)
	conn.request("POST", "/controller/eventsManager.php", params, headers)
	response = conn.getresponse()
	dataB = response.read()
	data = json.loads(str(dataB, 'utf-8'))
	conn.close()
	if data['success'] == 1:
		return data['actions']
	else:
		return False

#TEST

#get channels
#print (getChannels())

#Create a new rule
#print(createRule())

#get the event from the new rule before created
#print(getEvents('public'))