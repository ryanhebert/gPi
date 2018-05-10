# MAIN
import h2o
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


def main():
  
	controller = h2o.h2oController(7)

	for zone in controller.zones:
		controller.startZone(zone,1)


if __name__== "__main__":
  main()






def test():
  
	test = h2o.h2oController(7)
	#test.startZone(test.zones[0], 3)

	## Create Schedule
	scheduledZones = []
	for zone in test.zones:
		scheduledZones.append({"zone": zone, "duration": test.defaultDuration})

	s = test.create_schedule(scheduledZones, "schedule-1")
	test.startSchedule(s)