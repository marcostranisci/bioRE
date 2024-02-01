import json
import pandas as pd

class Experiments:
    def __init__(self) -> None:
        pass

    def collect_gold(self,path):
        ents = list()
        rels = list()
        for item in open(path):
            
            jsn = json.loads(item)
            _id = jsn['doc_id']
            for ent in jsn['entities']:
                ents.append({'doc_id':_id,'person':' '.join(jsn['words'][ent[0]:ent[1]])})
            for triple in jsn['triplets']:
                rels.append({'doc_id':_id,'s':triple['subject']['name'],'p':triple['relation']['name'],'o':triple['object']['name']})
        return ents,rels
    
    def collect_preds(self,path):
        ents = list()
        rels = list()
        for item in open(path):
            
            jsn = json.loads(item)
            _id = jsn['doc_id']
            for ent in jsn['predicted_entities']:
                ents.append({'doc_id':_id,'person':' '.join(jsn['words'][ent[0]:ent[1]])})
            for triple in jsn['predicted_relations']:
                rels.append({'doc_id':_id,'s':' '.join(jsn['words'][triple['subject']['start']:triple['subject']['end']]),'p':triple['relation']['name'],'o':' '.join(jsn['words'][triple['object']['start']:triple['object']['end']])})
        return ents,rels
    
    def compare_rels(self,df_1,df_2):
        '''df_1 = df_1.groupby('doc_id').triple.apply(list).reset_index()

        df_2 = df_2.groupby('doc_id').triple.apply(list).reset_index()
        
        for i,row in df_1.iterrows():
            for item in row.triple:
                if item not in df_2.loc[i,'triple']:
                    print(item)'''
        df_2 = df_2.merge(df_1,how='right',on=['doc_id','s','p','o'])

        return df_2
    def augment(self,df_1,df_2,feat='female'):

        df_2 = df_2[['label','person','gender']].drop_duplicates()
        df_2.columns = ['person','label','gender']
        group = df_2[df_2.gender==feat]
        a = df_1.merge(group,left_on='s',right_on='person')
        b = df_1.merge(group,left_on='o',right_on='person')
        a = pd.concat([a,b]).drop_duplicates()

        return a


if __name__ == '__main__':
    exp = Experiments()

    gold_ents,gold_rels = exp.collect_gold('../test.pretrained-biore.hierarchy.jsonl')
    pred_ents,pred_rels = exp.collect_preds('../test.pretrained-biore.hierarchy.jsonl')

    gold_rels = pd.DataFrame(gold_rels)
    pred_rels = pd.DataFrame(pred_rels)
    #pred_rels['triple'] = pred_rels['s']+ ' '+pred_rels['p']+ ' '+pred_rels['o']
    #gold_rels['triple'] = gold_rels['s']+ ' '+gold_rels['p']+ ' '+gold_rels['o']
    pred_rels['pred'] = 1
    gold_rels['gold'] = 1
    comp = exp.compare_rels(gold_rels,pred_rels)


    comp = comp[comp.pred.isna()]
    df = pd.read_csv('../output/crossre_augmented_gender.csv')

    x = exp.augment(comp,df)
    print('false_w',x.p.value_counts())

    
        
