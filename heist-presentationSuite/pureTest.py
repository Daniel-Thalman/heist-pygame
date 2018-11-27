from renforcement import *

def something(seed, n):
	seed = str(seed)
	n = int(n)
	stats = playPure(seed, n, 4)
	highScoreF = open("highscore.txt", "a")
	highScoreF.write(str(stats['max']) + "\n")
	highScoreF.close()
	return stats

print(something(0, 64))
