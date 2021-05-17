import random
def main():
	f = open("example.txt", "w")
	for i in range (0,200):
		x = random.randint(1,5)
		if x ==1:
			f.write("'ensolarado',")
		elif x==2:
			f.write("'garoa',")
		elif x==3:
			f.write("'chuvoso',")
		elif x==4:
			f.write("'neblina',")
		elif x==5:
			f.write("'neve',")
		
		x = random.randint(1,2)
		if x ==1:
			f.write("'dia',")
		elif x==2:
			f.write("'noite',")
		x = random.randint(1,3)
		if x ==1:
			f.write("'grande',")
		elif x==2:
			f.write("'media',")
		elif x==3:
			f.write("'pequena',")
		x = random.randint(1,3)
		if x ==1:
			f.write("'grande',")
		elif x==2:
			f.write("'media',")
		elif x==3:
			f.write("'pequena',")
		x = random.randint(1,3)
		if x ==1:
			f.write("'grande',")
		elif x==2:
			f.write("'media',")
		elif x==3:
			f.write("'pequena',")
		x = random.randint(1,2)
		if x ==1:
			f.write("'sim',")
		elif x==2:
			f.write("'nao',")
		x = random.randint(1,2)
		if x ==1:
			f.write("'sim',")
		elif x==2:
			f.write("'nao',")
		x = random.randint(1,3)
		if x ==1:
			f.write("'alta',")
		elif x==2:
			f.write("'media',")
		elif x==3:
			f.write("'baixa',")
		x = random.randint(1,3)
		if x ==1:
			f.write("'alta',")
		elif x==2:
			f.write("'media',")
		elif x==3:
			f.write("'baixa',")
		f.write("'indiferente'")
		f.write("\n")
	f.close()

main()

