import csv
import ipdb
import  os
import re
import jellyfish


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print BASE_DIR

CSV_DIR = os.path.join(BASE_DIR, "774_summary.csv")
LGA_DIR = os.path.join(BASE_DIR, "lgas.csv")

ptrn = re.compile("\s|-|\/|\'")

with open(CSV_DIR, 'r') as f:
    
    myreader = csv.DictReader(f)
    csv_file = []

    for row in myreader:
        state = re.sub(ptrn, "_", row['State'].lower().strip())
        lga = re.sub(ptrn, "_", row['LGA'].lower().strip())
        row['unique_lga'] = state + "_" + lga
        csv_file.append(row)

with open(LGA_DIR, 'r') as f:
    myreader = csv.DictReader(f)
    lgas = [row for row in myreader]



true_name = [row['unique_lga'] for row in lgas]

log = open(os.path.join(BASE_DIR, "matching.log"), "wa")

output_file = open(os.path.join(BASE_DIR, "output.csv"),"wa")
fieldname = csv_file[0].keys()
csvwriter = csv.DictWriter(output_file, delimiter=',', fieldnames=fieldname)
csvwriter.writeheader()

counter = 1
for row in csv_file:
    
    old_name = row['unique_lga']
    score = [jellyfish.jaro_winkler(old_name, tn) for tn in true_name]
    
    max_score = max(score)
    candidate = true_name[score.index(max_score)]
    
    if max_score >= 0.912:
        row['unique_lga'] = candidate
    else:
        log.write('Row_num:%s score:%.3f  Old:%s |===> New:%s \n'
            % (counter, max_score, old_name, candidate))
    counter = counter + 1 
    csvwriter.writerow(row)

log.close()
output_file.close()
#ipdb.set_trace()

