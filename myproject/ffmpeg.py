def filter_inicio(time):
	if int(time[9]) < 5:
		if int(time[7]) == 0:
			if int(time[6]) == 0:
				if int(time[4]) == 0:
					if int(time[3]) == 0:
						if int(time[1]) == 0:
							return '00:00:00.000'
						else:
							newtime = time[:1] + str(int(time[1]) - 1) + ':59:59'+ '.'+ str((int(time[9]) - 5)%10) + time[10:]
							return newtime
					else:
						newtime = time[:3] + str(int(time[3]) - 1) + '9:59'+ '.'+ str((int(time[9]) - 5)%10) + time[10:]
						return newtime
				else:
					newtime = time[:4] + str(int(time[4]) - 1) + ':59'+ '.'+ str((int(time[9]) - 5)%10) + time[10:]
					return newtime
			else:
				newtime = time[:6] + str(int(time[6]) - 1) + '9'+ '.'+ str((int(time[9]) - 5)%10) + time[10:]
				return newtime
		else:
			newtime = time[:7] + str(int(time[7]) - 1) + '.'+ str((int(time[9]) - 5)%10) + time[10:]
			return newtime
	else:
		newtime = time[:9] + str(int(time[9]) - 5) + time[10:]
		return newtime

def filter_fim(time):
	if int(time[9]) >= 5:
		if int(time[7]) == 9:
			if int(time[6]) == 5:
				if int(time[4]) == 9:
					if int(time[3]) == 5:
						newtime = time[:1] + str(int(time[1]) + 1) + ':00:00'+ '.'+ str((int(time[9]) + 5)%10) + time[10:]
						return newtime
					else:
						newtime = time[:3] + str(int(time[3]) + 1) + '0:00'+ '.'+ str((int(time[9]) + 5)%10) + time[10:]
						return newtime
				else:
					newtime = time[:4] + str(int(time[4]) + 1) + ':00'+ '.'+ str((int(time[9]) + 5)%10) + time[10:]
					return newtime
			else:
				newtime = time[:6] + str(int(time[6]) + 1) + '0'+ '.'+ str((int(time[9]) + 5)%10) + time[10:]
				return newtime
		else:
			newtime = time[:7] + str(int(time[7]) + 1) + '.'+ str((int(time[9]) + 5)%10) + time[10:]
			return newtime
	else:
		newtime = time[:9] + str(int(time[9]) + 5) + time[10:]
		return newtime


def add_in_database():
	lines = open('Legenda.srt', 'r', encoding="utf8").readlines()
	resultado = []
	i = 0
	while(i+6 < len(lines)):		
		
		string = 'Sentence.objects.create(sentence=u"'+ lines[i+2].rstrip().replace(' ', '==')+'", pinyin = "' + lines[i+4].rstrip()+'", equivalence = "' + lines[i+3].rstrip().replace('"',"'")
		resultado.append(string)
		i=i+6

	#resultado = f7(resultado)

	for i in range(0,len(resultado)):
		resultado[i] = resultado[i] + '", number = '+str(i)+")\n"

	open("database.txt", 'w', encoding="utf8").writelines(resultado)

#def f7(seq):
 #   seen = set()
  #  seen_add = seen.add
   # return [x for x in seq if not (x in seen or seen_add(x))]

def convert_srt():
	counter = 1
	size = 0
	lines = open('Legenda.srt', 'r', encoding="utf8").readlines()

	resultado = ['chcp 65001\n']
	i = 0
	while(i+6 < len(lines)):
		tempos = lines[i+1].split(" ")
		inicio = tempos[0].replace(',','.')
		fim = tempos[2].rstrip().replace(',','.')
		
		string = "ffmpeg -i Dragão.Wu-Xia.2014.720p.BluRay.x264.S4FILMES.mp4 -ss "+ filter_inicio(inicio) + " -to "+ filter_fim(fim) + " " + lines[i+2].rstrip().replace(' ', '==') + ".mp4\n"
		resultado.append(string)
		i=i+6

		
	resultado.append('"')
	name = 'output.bat'
	open(name, 'w', encoding="utf8").writelines(resultado)
	

	

#add_in_database()
convert_srt()

