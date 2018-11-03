import statistics as stats
scorefile = open("scores%s.csv" % (input()))
lines = scorefile.readlines()
scores = []
for line in lines:
	scores += [int(line[:-1])]


print("min: %f\nmax: %f\nmedian: %f\nmean: %f\nstdev: %f" % (min(scores), max(scores), stats.median(scores), stats.mean(scores), stats.stdev(scores)))
scorefile.close()
