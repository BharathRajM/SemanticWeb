# todo use description too
#import the CSV module for dealing with CSV files
import csv

#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
ifile = open('/home/veror/Desktop/Uni/Semantic Web Technology/Final Project/esco-files/v1.0.0_1/skills_en.csv', 'r')
reader = csv.reader(ifile)

#create a new variable called 'outfile' (could be any name), which we'll use to create a new file that we'll pass our TTL into.
outfile = open('esco_skill.ttl', 'w')

#get python to loop through each row in the CSV, and ignore the first row.
rownum = 0
for row in reader:
	if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
		pass
	else: # if it's not the first row, place the contents of the row into the 'c' variable, then create a 'd' variable with the stuff we want in the file.
		c = row
		split_alt = c[5].splitlines()
		split_hidden = c[6].splitlines()
		if len(split_alt) != 0:
			str_split_alt = split_alt[0] + '\"'
			for el in range(1, len(split_alt), 1):
				str_split_alt += ', \"' + split_alt[el] + '\"'
			d = '<' + c[1] + '> \n skos:prefLabel "' + c[4] + '" ;\n skos:altLabel "' + str_split_alt
		else:
			d = '<' + c[1] + '> \n skos:prefLabel "' + c[4] + '" ;\n skos:altLabel ""'
		if len(split_hidden) != 0:
			str_split_hidden = split_hidden[0] + '\"'
			for el in range(1, len(split_hidden), 1):
				str_split_hidden += ', \"' + split_hidden[el] + '\"'
			d += ' ;\n skos:hiddenLabel "' + str_split_hidden + ' .\n \n'
			#c[12] = c[12].replace("\n", "")
			#d += ' ;\n skos:hiddenLabel "' + str_split_hidden + ' ;\n dct:description "' + c[12] + '" .\n \n'
		else:
			d += ' ;\n skos:hiddenLabel ""' + ' .\n \n'
			#c[12] = c[12].replace("\n", "")
			#d += ' ;\n dct:description "' + c[12] + '" .\n \n'
		outfile.write(d)	# now write the d variable into the file
	rownum += 1 # advance the row number so we can loop through again with the next row

# finish off by closing the two files we created

outfile.close()
ifile.close()