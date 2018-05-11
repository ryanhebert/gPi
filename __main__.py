# MAIN
import threading
import time
import h2o
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

controller = h2o.h2oController(7)


class simpleStart(Resource):

	def __init__(self):
		self.thread = threading.Thread(target=self.run, name="simpleStart", args=())
		self.thread.event = threading.Event()

	def post(self):
		
		self.thread.start()
		#self.thread.event.set()
		
		return 'Success', 201

	def run(self):
		controller.simpleMode()
		#while not self.thread.event.is_set():
			#controller.simpleMode()


class stopZones(Resource):

	def post(self):
		controller.stopZones()
		return 'Success', 201

class stopZone(Resource):

	def post(self):
		controller.stopZone()
		return 'Success', 201

class toggleSimpleStart(Resource):

	def __init__(self):
		self.thread = threading.Thread(target=self.run, name="simpleStart", args=())
		self.thread.event = threading.Event()

	def post(self):
		
		self.thread.start()
		#self.thread.event.set()
		
		return 'Success', 201

	def run(self):
		if controller.getRunning():
			controller.stopZones()
		else:
			controller.simpleMode()
		#while not self.thread.event.is_set():
			#controller.simpleMode()

class getRunning(Resource):

	def get(self):
		return controller.getRunning(), 201


api.add_resource(simpleStart, '/simpleStart')
api.add_resource(stopZones, '/stopZones')
api.add_resource(stopZone, '/stopZone')
api.add_resource(toggleSimpleStart, '/toggleSimpleStart')
api.add_resource(getRunning, '/getRunning')

if __name__== "__main__":
	app.run(debug=True)



def test():

	test = h2o.h2oController(7)
	#test.startZone(test.zones[0], 3)

	## Create Schedule
	scheduledZones = []
	for zone in test.zones:
		scheduledZones.append({"zone": zone, "duration": test.defaultDuration})

	s = test.create_schedule(scheduledZones, "schedule-1")
	test.startSchedule(s)