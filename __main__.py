# MAIN
import h2o


def main():
  
	test = h2o.h2oController(7)
	#test.startZone(test.zones[0], 3)

	## Create Schedule
	scheduledZones = []
	for zone in test.zones:
		scheduledZones.append({"zone": zone, "duration": test.defaultDuration})

	s = test.create_schedule(scheduledZones, "schedule-1")
	test.startSchedule(s)


if __name__== "__main__":
  main()