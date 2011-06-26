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

list1_n = []
list2_n = []

for item in list1:
    if item not in list2:
        list1_n.append(item)
for item in list2:
    if item not in list1:
        list2_n.append(item)


        

list1_n.sort()
list2_n.sort()



print "list1:"
for item in list1_n:
    print item

print "list2:"
for item in list2_n:
    print item
print "length_1:", len(list1_n)
print "length_2:", len(list2_n)

file1.close()        
file2.close()        
