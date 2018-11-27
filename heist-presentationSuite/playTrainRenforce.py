from renforcement import *
import compileModel as CM

def something(limit, chance, seed):
	n = 1024
	seed = str(seed)
	CM.compile()
	stats = playTrain(seed, n, limit, chance, 8)
	highScoreF = open("highscore.txt", "a")
	highScoreF.write(str(stats['max']) + "\n")
	highScoreF.close()
	return stats

print(something(100, 0.2, 0))
