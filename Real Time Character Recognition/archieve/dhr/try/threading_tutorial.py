import threading
import time

class my_thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "C Thread"
	def run(self):
		print "Starting " + self.name
		initialize_moods()
		print "Exiting " + self.name

def initialize_moods():
	# start C code here
	for i in range(1,11):
		print(i*100)
		time.sleep(2)
	# print something when C exits
	print("Exiting C")

c_thread = my_thread()
c_thread.start()

# running in main thread
for i in range(20):
	print(i)
	time.sleep(1)