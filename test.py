arr = '28125'
length = len(arr)
len_str = str(arr).zfill(10)
print length
i = 0
while i < 10:
	print len_str[i:]
	i = i + 1

