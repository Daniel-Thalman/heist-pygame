from renforcement import *

n = 128
limit = 40
chance = 0.5
seed = str(input())
for i in range(1, 9):
	stats = playTrain(seed, n, limit, chance)
	limit = stats["median"]
	chance *= 0.8
	print(stats, "\nCycles Completed: %d" % (i))
