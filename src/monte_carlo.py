from scipy.stats import f_oneway
import pandas as pd
import numpy as np
import argparse,yaml
from collections import Counter

parser = argparse.ArgumentParser()

parser.add_argument('-f','--filename')

args = parser.parse_args()

with open(args.filename) as f:
    prm = yaml.load(f,Loader=yaml.FullLoader)

df = pd.read_csv(prm['input']['ny_ethn'])

relations = df.relation.drop_duplicates().to_list()
male = df[df.FormerColony==0]
m = list()
female = df[df.FormerColony==1]
for s in range(10):
    l = list()
    np.random.seed(s)
    a = np.random.randint(0,len(male.person.drop_duplicates()),100)
    b = np.random.randint(0,len(female.person.drop_duplicates()),100)


    for rel in relations:
        tot_m = list()
        for item in a:
            person = male.person.drop_duplicates().to_list()[item]
            rels = male[male.person==person].relation.to_list()
            counted = Counter(rels)
            if rel in counted:
                tot_m.append(counted[rel])
                
            else: tot_m.append(0)

        tot_f = list()
        for item in b:
            person = female.person.drop_duplicates().to_list()[item]
            rels = female[female.person==person].relation.to_list()
            counted = Counter(rels)
            if rel in counted:
                tot_f.append(counted[rel])
            else: tot_f.append(0)
            

        l.append((s,rel,f_oneway(tot_f,tot_m).pvalue,np.mean(tot_m),np.mean(tot_f)))
    print(l)
    m.extend(l)

pd.DataFrame(m,columns=['round','relation','p','w','t']).to_csv(prm['output']['report'],index=False)


'''tot_m = None
for item in a:
    person = male.person.drop_duplicates().to_list()[item]
    rels = male[male.person==person].relation.to_list()
    counted = Counter(rels)
    if tot_m is None:
        tot_m = counted
    else: tot_m = counted+tot_m

tot_f = None
for item in b:
    person = female.person.drop_duplicates().to_list()[item]
    rels = female[female.person==person].relation.to_list()
    counted = Counter(rels)
    if tot_f is None:
        tot_f = counted
    else: tot_f = counted+tot_f

print(tot_f,tot_m)
print(f_oneway([tot_f[x] for x in relations],[tot_m[x] for x in relations]))'''