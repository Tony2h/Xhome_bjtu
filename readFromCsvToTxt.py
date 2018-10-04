with open("playlist_style1.csv") as file:
	for line in file:
		line1=line.split('\n')
		str = line1[0].split(',')
		songname = str[0]+'\n'
		with open("songname.txt",'a') as f: 
    			f.write(songname)
		
