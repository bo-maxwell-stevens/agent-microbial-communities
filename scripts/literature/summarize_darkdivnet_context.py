#!/usr/bin/env python3
import json
from pathlib import Path
import pandas as pd

base=Path('.')
meta=pd.read_csv(base/'data'/'Final_data_with_diversity_prefixed.csv')
amf=pd.read_csv(base/'data'/'AMF_OTU_table_final.tsv', sep='\t', usecols=[0])
bac=pd.read_csv(base/'data'/'BAC_OTU_table_final.tsv', sep='\t', usecols=[0])
euk=pd.read_csv(base/'data'/'EUK_OTU_table_final.tsv', sep='\t', usecols=[0])
its=pd.read_csv(base/'data'/'ITS_OTU_table_final.tsv', sep='\t', usecols=[0])

meta_id='canonical' if 'canonical' in meta.columns else meta.columns[0]
sets={
    'META': set(meta[meta_id].astype(str).str.strip()),
    'AMF': set(amf.iloc[:,0].astype(str).str.strip()),
    'BAC': set(bac.iloc[:,0].astype(str).str.strip()),
    'EUK': set(euk.iloc[:,0].astype(str).str.strip()),
    'ITS': set(its.iloc[:,0].astype(str).str.strip()),
}
keys=['META','AMF','BAC','EUK','ITS']
pairwise=[]
for i,a in enumerate(keys):
    for b in keys[i+1:]:
        pairwise.append({'a':a,'b':b,'overlap_n':len(sets[a]&sets[b])})

union=set().union(*sets.values())
all5=set.intersection(*sets.values())

out={
    'meta_id_column': meta_id,
    'set_sizes': {k:len(v) for k,v in sets.items()},
    'pairwise_overlap': pairwise,
    'union_n': len(union),
    'all5_n': len(all5),
    'missing_from_union': {k:len(union-v) for k,v in sets.items()},
    'darkdivnet_core_vars_present': [v for v in ['alpha','gamma','dark','compl','pool','compl.perc','beta','beta.perc'] if v in meta.columns],
    'darkdivnet_core_vars_missing': [v for v in ['alpha','gamma','dark','compl','pool','compl.perc','beta','beta.perc'] if v not in meta.columns],
}

out_dir=base/'results'/'literature_search_records'
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir/'dataset_context_darkdivnet.json').write_text(json.dumps(out, indent=2))
print(json.dumps({'out':str(out_dir/'dataset_context_darkdivnet.json'), 'all5_n':out['all5_n'], 'union_n':out['union_n']}))
