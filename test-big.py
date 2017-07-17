import fileinput

counter = 0
with fileinput.input(files=('2.out', )) as f:
    for line in f:
        counter += 1
	
print("total lines: %s" % str(counter))
