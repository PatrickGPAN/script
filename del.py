import time

date=time.strftime("%Y%m%d")

print "###START TO AlTER THE HOLDDETAILS FOR XXX###"

with open("details"+date+".txt","w") as f:
    for line in f:
        if 'XXX' not in line:
            f.write(line + '\n')
    f.truncate()

print "###Completed###"
