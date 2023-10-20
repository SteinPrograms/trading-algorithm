import sched, time

schedule = sched.scheduler(time.monotonic, time.sleep)

def fetch():
    print("Seems to be working")
    schedule.enter(1,1,fetch)
    schedule.run()

fetch()
while True:
    pass