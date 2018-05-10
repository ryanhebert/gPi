import threading
import time
import RPi.GPIO as GPIO
from crontab import CronTab

#### __init__
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
####

class h2oController:

	def __init__(self, zoneCount):
		self.zoneCount = zoneCount
		self.zones = []
		self.schedules = []
		self.defaultDuration = 1
		self.abort = False

		pins = [18,16,22,15,11,13,21,19]
		GPIO.setup(pins, GPIO.OUT, initial=GPIO.HIGH)

		for i, pin in enumerate(pins):
			if i < zoneCount:
				self.zones.append(h2oZone(i+1,pin))

		## Test
		#for i, pin in enumerate(pins):
		#	GPIO.output(pin, GPIO.HIGH)
		#	time.sleep(1)

		#for i, pin in enumerate(pins):
		#	GPIO.output(pin, GPIO.LOW)
		#	time.sleep(1)



	def create_schedule(self, scheduledZones, name="default"):
		retVal = h2oSchedule(scheduledZones, name)
		self.schedules.append(retVal)
		return retVal


	def stopZones(self):
		for zone in self.zones:
			GPIO.output(zone.pin, GPIO.HIGH)

			if not GPIO.input(zone.pin):
				return False
		return True


	def startZone(self, zone, duration):

		if zone in self.zones:
			if self.stopZones():
				startTime = time.time()
				print("starting zone " + str(zone.pin))
				GPIO.output(zone.pin, GPIO.LOW)
				while True:
					now = time.time()
					timer = duration * 60 - int(now - startTime)
					print ("%02d" % (timer/60/60) + ":" + "%02d" % (timer/60) + ":" + "%02d" % (timer%60))
					if self.abort == True:
						self.abort = False
						print("zone aborted")
						break
					elif  timer > 0:
						time.sleep(1)
					else:
						GPIO.output(zone.pin, GPIO.HIGH)
						print("zone finished")
						break
				return True
			else:
				print("error stopping zones")
				return False
		else:
			print("zone doesn't exist")
			return False

	def startSchedule(self, schedule):

		print schedule

		for item in schedule.scheduledZones:
			#print item['zone']
			#print item['duration']
			self.startZone(item['zone'], item['duration'])



class h2oZone:

	def __init__(self, number, pin, name=None):

		self.number = number
		self.pin = pin
		
		if name == None:
			self.name = 'Zone-'+str(number)
		else:
			self.name = name

	def set_name(self, name):
		self.name = str(name)


class h2oSchedule: ## need to finish

	def __init__(self, scheduledZones, name="default", days=[1,2,3,4,5,6,7], timeInHours=24):

		self.name = name
		self.scheduledZones = scheduledZones ## scheduledZone = {"zone": zone1, "duration": 5}
		self.cron = CronTab(user=True)


	def set(self):

		job = self.cron.new(command='print("API runSchedule()")')
		job.dow.on(days)
		job.hour.on(timeInHours)

		if job.is_valid():
			self.cron.write()

		if self.cron.render():
			return True

	def forget(self):
		self.cron.delete()
