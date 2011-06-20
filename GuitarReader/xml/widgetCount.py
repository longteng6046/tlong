import sys



file1 = open(sys.argv[1])
file2 = open(sys.argv[2])


list1 = []
list2 = []

for line in file1.readlines():
    if "<Value>w" in line:
        line = line.strip()[7:-8]
        list1.append(line)

for line in file2.readlines():
    if "<Value>w" in line:
        line = line.strip()[7:-8]
        list2.append(line)

list1 = list(set(list1))
list2 = list(set(list2))


for item in list1:
    if item in list2:
        list1.remove(item)
        list2.remove(item)
        print 'pop1'
for item in list2:
    if item in list1:
        list1.remove(item)
        list2.remove(item)
        print 'pop2'


        

list1.sort()
list2.sort()

print len(list1)
print len(list2)

# for i in range(0, len(list1)):
    # if list1[i] != list2[i]:
        # print "idx:", i, 'list1:', list1[i], 'list2:', list2[i]

file1.close()        
file2.close()        
