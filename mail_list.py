import csv
import os

THIS_FILE = os.path.abspath(__file__)
THIS_DIR = os.path.split(THIS_FILE)[0]
PARENT_DIR = os.path.split(THIS_DIR)[0]

def main(target_file):
	print "\nValidating addresses in: " + target_file.split('\\')[-1]
	
	csv_data = [line for line in csv.reader( open(target_file) )]
	keys = csv_data.pop(0)
	total_to_parse = len(csv_data)
	print "Parsing %d total addresses" % total_to_parse
	raw_input("Ready?")
	
	valid_keys = ('zip', 'city')
	dicts = [dict for dict in csv_to_dictionaries(csv_data, keys) if valid_dict(dict, valid_keys)]
	total_filtered = total_to_parse - len(dicts)
	print "Valid addresses: " + str(len(dicts))
	print "Filtered out %d invalid addresses." % total_filtered
	
	unique_keys = ('address1', 'zip')
	
	results = f5_filter([tuple(x.items()) for x in dicts], address_id_filter)
	log_csv_tuples(results)

def csv_to_dictionaries(data, keys):
	for line in data:
		data_dictionary = {}
		for i in range( len(keys) ):
			try: data_dictionary[ keys[i] ] = clean_text(line[i], keys[i])
			except: data_dictionary[ keys[i] ] = ''
		yield data_dictionary
		
def valid_dict(dict, valid_keys):
	for k in valid_keys:
		if not dict[k]: return False
		
	country = dict['country']
	if country != 'US' and country != 'USA' and country != '':
		return False
	
	if not dict['zip'].isdigit(): return False
	
	return True
	
def address_id_filter(x):
    keys = []
    for k in x:
        if 'zip' in k: keys.append(k)
        if 'address1' in k: keys.append(k)
    return tuple(keys)
	
def f5_filter(seq, idfun):
	# order preserving 
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result
	
def duplicate_filter(data, datalist, unique_keys):
	for x in datalist:
		if not unique_dict(data, x, unique_keys):
			#if x is not data: datalist.remove(x)
			datalist = duplicate_filter(data, [y for y in datalist if y is not x or y is data], unique_keys)
	return datalist
	
def unique_dict(d1, d2, unique_keys):
	for key in unique_keys:
		if d1[key] != d2[key]: return True
	
	#print "\nDuplicate found:"
	#log_dict(d1)
	return False
	
def unique_pairs(data):
	i = len(data) - 1
	while i:
		j = i
		while j:
			j -= 1
			yield (i, j)
		i -= 1
		
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
	
def log_csv_dicts(csv_dicts):
	i = 0
	for dict in csv_dicts:
		print "\n%d" % i
		log_dict(dict)
		i += 1
		
def log_csv_tuples(csv_tuples):
	i = 0
	for tup in csv_tuples:
		print "\n%d" % i
		log_tuple(tup)
		i += 1
		
def log_dict(dict):
	for k, v in dict.items(): print "\t%s : %s" % (k, v)
	
def log_tuple(tup):
	for k, v in tup: print "\t%s : %s" % (k, v)
	
if __name__ == "__main__":
	file = PARENT_DIR + "\\data\\" + "quickbooks_all.csv"
	if os.path.exists(file): main(file)
	else: print "No such file."