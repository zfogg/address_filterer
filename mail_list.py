import csv
import os
from glob import glob

THIS_FILE = os.path.abspath(__file__)
THIS_DIR = os.path.split(THIS_FILE)[0]
PARENT_DIR = os.path.split(THIS_DIR)[0]

def main(files):

	csv_data = []
	keys = ()
	for file in files:
		print "\tTarget: %s\n" % file.split('\\')[-1]
		data = [line for line in csv.reader( open(file) )]
		keys = data.pop(0)
		print keys
		csv_data += data
	raw_input()
	total_to_parse = len(csv_data)
	
	print "Validating addresses . . ."
	valid_keys = ('zip', 'city')
	print "Validation keys: %s" % str(valid_keys)
	dicts = [dict for dict in csv_to_dictionaries(csv_data, keys) if valid_dict(dict, valid_keys)]
	total_filtered = total_to_parse - len(dicts)
	print "%d valid addresses = %d total - %d invalid" % (
		total_to_parse - total_filtered, total_to_parse, total_filtered
	)
	
	print "\n"
	
	print "Filtering duplicates . . ."
	unique_keys = ('address1', 'zip')
	print "Duplication signature: %s" % str(unique_keys)
	results = f5_filter( [tuple(x.items()) for x in dicts], address_signature(unique_keys) )
	duplicates_found = total_to_parse - total_filtered - len(results)
	print "%d addresses = %d valid - %d duplicates" % (
		len(results), total_to_parse - total_filtered, duplicates_found
	)

def csv_to_dictionaries(data, keys):
	for line in data:
		data_dictionary = {}
		for i in range( len(keys) ):
			data_dictionary[ keys[i] ] = clean_text(line[i], keys[i])
		yield data_dictionary
		
def valid_dict(dict, valid_keys):
	for k in valid_keys:
		if not dict[k]: return False
	country = dict['country']
	if country != 'US' and country != 'USA' and country != '':
		return False
	if not dict['zip'].isdigit(): return False
	
	return True

def address_signature(unique_keys):
	def f(address):
		signature = []
		for element in address:
			for uk in unique_keys:
				if uk in element: signature.append(element)
		return tuple(signature)
	return f
	
def f5_filter(seq, idfun=lambda x: x):
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result
		
def clean_text(text, key):
	text = text.replace('.', '').upper().strip(" ")
	
	if key == 'address1':
		if text.endswith(' ST'):
			text = text[:-2] + 'STREET'
		elif text.endswith(' RD'):
			text = text[:-2] + "ROAD"
		elif text.endswith(' AV') or text.endswith(" AVE"):
			text = ' '.join(text.split(' ')[:-1]) + " AVENUE"
		elif text.endswith(' PL'):
			text = text[:-2] + "PLACE"

	if key == 'zip':
		text = text.split('-')[0]

	return text
		
def log_csv_tuples(csv_tuples):
	i = 0
	for tup in csv_tuples:
		print "\n%d" % i
		log_tuple(tup)
		i += 1
	
def log_tuple(tup):
	for k, v in tup: print "\t%s : %s" % (k, v)
	
if __name__ == "__main__":
	data_path = PARENT_DIR + "\\data\\"
	files = glob( os.path.join(data_path, '*.csv') )
	
	#file = PARENT_DIR + "\\data\\" + "quickbooks_all.csv"
	main(files)
	#else: print "No such file."