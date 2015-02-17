def func(string,length):
	stringArray = []
	for i in string:
		stringArray += i 
	for j in range(0,length):
		if stringArray[j] == ' ':
			stringArray[j] = '%20'
	print(stringArray)


