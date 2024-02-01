import json
import pandas as pd
from random import shuffle


class Sampler:
    def __init__(self):
        pass 

    def find_threshold(self,path):
        df = pd.read_csv(path)
        print(df[df.gender=='female'].relation.value_counts())
        max_values = {row[0]:row[1] for row in df[df.gender=='female'].relation.value_counts().reset_index().to_numpy()}
        women =  {x.person:1 for _,x in df[df.gender=='female'].drop_duplicates(subset=['person']).iterrows()}
        men = {x.person:1 for _,x in df[df.gender=='male'].drop_duplicates(subset=['person']).iterrows()}

        return max_values,women,men
    
    def collect_minority(self,path,d_1,d_2):
        minority = list()
        majority = list()

        for doc in open(path):
            jsn = json.loads(doc)
            
            men = int()
            women = int()
            for item in jsn['gold_entities']:
                if item[-1] == 'PER':
                    if item[-2] in d_1:
                        women+=d_1[item[-2]]
                    elif item[-2] in d_2:
                        men+=d_2[item[-2]]
            
            if men==0 and women!=0:
                minority.append(jsn)
            elif men!=0 and women!=0:
                minority.append(jsn)
            elif men!=0 and women ==0:
                majority.append(jsn)
            men = int()
            women = int()
            
        return minority,majority

    def collect_majority(self,path,d_1,max_val,list_1,list_2):
        new_man = list()
        threshold = max_val['contributes']
        maj_val = {x:0 for x in max_val}
        for item in maj_val:
            maj_val[item] = 0
        
        for item in list_1:
            if maj_val['position held']<=max_val['position held']:
                men = list()
                for per in item['gold_entities']:
                    if per[-1] == 'PER' and per[-2] in d_1:
                        men.append(per[-2])
                
                for triple in item['gold_triplets']:

                    if triple['subject']['uri'] in men or triple['object']['uri'] in men:
                        maj_val[triple['relation']['name']]+=1
            else:break
        
        shuffle(list_2)
        for item in list_2:
            if maj_val['geographical']<=threshold:
                
                
                men = list()
                for per in item['gold_entities']:
                    if per[-1] == 'PER' and per[-2] in d_1:
                        men.append(per[-2])
                warn = [x['relation']['name'] for x in item['gold_triplets'] if x['relation']['name']=='position held']
                if len(warn)==0:
                    new_man.append(item)
                    for triple in item['gold_triplets']:
                        

                        if triple['subject']['uri'] in men or triple['object']['uri'] in men:
                    
                            maj_val[triple['relation']['name']]+=1
                else:continue
            else: break
        
        return maj_val,new_man
    


