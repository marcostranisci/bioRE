import json,argparse,yaml,glob
import pandas as pd


parser = argparse.ArgumentParser()

parser.add_argument('-f','--filename')

args = parser.parse_args()

with open(args.filename) as f:
    prm = yaml.load(f,Loader=yaml.FullLoader)

class AnnotationHandler:

    def __init__(self):
        pass

    def convert_rebel(self,a_jsonl):
        all_rels = list()
        for doc in open(a_jsonl):
            jsn = json.loads(doc)
            people = list()
            links = list()
            for item in jsn['gold_entities']:
                if item[-1] == 'PER':
                    print(item)
                    people.append(item[-2])
     
            for triple in jsn['gold_triplets']:
     
                links.append((triple['subject']['uri'],triple['relation']['name'],triple['relation']['name_orig'],triple['object']['uri']))
            for person in people:
                for link in links:
                    if link[0]==person or link[-1]==person:
                        all_rels.append({'person':person,'relation':link[1],'orig_relation':link[2]})
        

        return all_rels

    def convert_crossre(self,folder):
        all_rels = list()
        for file in glob.glob(folder):
            for doc in open(file):
                jsn = json.loads(doc)
                people = list()
                if len(jsn['relations'])>0:
                    for item in jsn['ner']:
                        if item[-1] == 'person':
                            people.append((item[0],item[1]))
                    for el in jsn['relations']:
                        for per in people:
                            if per[0]==el[0] or per[0] == el[2]:
                                all_rels.append({'person':' '.join(jsn['sentence'][per[0]:per[1]+1]),'relation':el[4]})
        return all_rels
    
    def link_crossre(self,folder):
        all_ents = list()
        for file in glob.glob(folder):
            for doc in open(file):
                jsn = json.loads(doc)
                for item in jsn['gold_entities']:
                    try:
                        all_ents.append({'person':item[2],'label':item[3]})
                    except: continue
        return all_ents
    
    def augment_entity(self,relations,feature):
        rels = pd.read_csv(relations)
        feats = pd.read_csv(feature)
        rels = rels.merge(feats,on='person')

        return rels

if __name__ == "__main__":
    handler = AnnotationHandler()
    reb = handler.link_crossre(prm['original']['crossre_linked'])

    df = pd.DataFrame(reb)
    df.to_csv('../output/all_linked_crossre.csv',index=False)
    print(len(reb),reb[:10])
    
    