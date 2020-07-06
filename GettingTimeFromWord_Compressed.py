import re

subtitle_content = []
subtitle_time_window = []

def approx(time1, time2, adjust = 500):
	time1 = re.split(",", time1)
	dec1 = int(time1[1])
	hour1 = int(re.split(":", time1[0])[0])
	min1 = int(re.split(":", time1[0])[1])
	sec1 = int(re.split(":", time1[0])[2])
	time2 = re.split(",", time2)
	dec2 = int(time2[1])
	hour2 = int(re.split(":", time2[0])[0])
	min2 = int(re.split(":", time2[0])[1])
	sec2 = int(re.split(":", time2[0])[2])
	if(dec1 <= 996):
		if((hour1 == hour2) and (min1 == min2) and (sec1 == sec2) and (dec2 - dec1 <= adjust)):
			return True
		return False
	elif(sec1 <= 58):
		if(((hour1 == hour2) and (min1 == min2) and (sec1 == sec2) and (dec2 - dec1 > 0))
			or
			((hour1 == hour2) and (min1 == min2) and (sec1 == sec2 - 1) and (dec2 - dec1 <= -(1000 - adjust)))):
			return True
		return False
	elif(min1 <= 58):
		if(((hour1 == hour2) and (min1 == min2) and (sec1 == sec2) and (dec2 - dec1 > 0))
			or
			((hour1 == hour2) and (min1 == min2 - 1) and (sec2 == 0) and (dec2 - dec1 <= -(1000 - adjust)))):
			return True
		return False
	else:
		if(((hour1 == hour2) and (min1 == min2) and (sec1 == sec2) and (dec2 - dec1 > 0))
			or
			((hour1 == hour2 - 1) and (min2 == 0) and (sec2 == 0) and (dec2 - dec1 <= -(1000 - adjust)))):
			return True
		return False

def compressor(list_time, list_content):
	if(len(list_time) >= 2):
		result1 = []
		result2 = []
		old_b = list_time[0][0]
		old_e = list_time[0][1]
		old_c = list_content[0]
		for i in range(1, len(list_time)):
			new_b = list_time[i][0]
			new_e = list_time[i][1]
			new_c = list_content[i]
			if(not approx(old_e, new_b)):
				result1.append([old_b, old_e])
				result2.append(old_c)
				old_b = new_b
				old_c = ""
			old_e = new_e
			old_c += new_c
			if(i == len(list_time) - 1):
				result1.append([old_b, old_e])
				result2.append(old_c)
		return result1, result2
	return list_time, list_content

def get_subtitle(subtitles):
	list1 = []
	list2 = []
	for index, subtitle in enumerate(subtitles):
		subtitle = subtitle.split("\n")
		list1.append(subtitle[1])
		if(len(subtitle) == 3):
			list2.append(subtitle[2].upper())
		else:
			list2.append(subtitle[2].upper() + "\n" + subtitle[3].upper()) 
	for i in range(len(list1)):
		list1[i] = list1[i].split(" --> ")
	return list1, list2

def get_time(word, time_list, subtitle_list):
	window_list = []
	content_list = []
	for index, subtitle in enumerate(subtitle_list):
		if(re.search(".*{}.*".format(word), subtitle)):
			window_list.append(time_list[index])
			content_list.append(subtitle_list[index])
	return window_list, content_list

def get_word():
	return(input("What word to search: "))

def reading_file(filename = None, code = "UTF-8"):
	if(filename == None):
		filename = input("In which file: ")
	with open(filename, "r", encoding = code) as f:
		data = f.read()
	data = data.split("\n\n")
	return data

subtitles = reading_file(None, "ISO-8859-15")
subtitle_time_window, subtitle_content =  get_subtitle(subtitles)
word = get_word().upper()
time_windows, corresponding_content = get_time(word, subtitle_time_window, subtitle_content)
compressed_time_windows, compressed_content = compressor(time_windows, corresponding_content)

print("{} has been found {} times in {} scenes".format(word, len(corresponding_content), len(compressed_content)))

final_content = []
for content in compressed_content:
	content = content.split("\n")
	temp = []
	for elt in content:
		elt = elt.split("\t")
		elt = elt[0]
		temp.append(elt)
	final_content.append(temp)

with open("Display.txt", "w") as f:
	for time_window, content in zip(compressed_time_windows, final_content):
		f.write("From {} to {}\n".format(time_window[0], time_window[1]))
		for line in content:
			f.write(line + "\n")
		f.write("\n")
# if(len(compressed_time_windows) == 0):
# 	print("{} has not been found anywhere... Sorry!".format(word))
# elif(len(compressed_time_windows) == 1):
# 	print("{} has been found at this time window : {}, with this subtitle : {}".format(word, compressed_time_windows[0], compressed_content[0]))
# else:
# 	print("{} has been found at these time windows : {}, with these contents : {}".format(word, compressed_time_windows, compressed_content))