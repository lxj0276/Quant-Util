import pandas as pd
from functools import reduce
from collections import OrderedDict
class features_dict(OrderedDict):
    def list_features(self):
        return self.keys()

    def to_DataFrame(self):
        dfs=[]
        for k,v in self.items():
            col=list(v.columns)
            idx=list(v.index)
            v_np=v.values
            df_list=[]
            for i in range(v_np.shape[0]):
                for j in range(v_np.shape[1]):
                    df_list.append([idx[i],col[j],v_np[i,j]])
            dfs.append(pd.DataFrame(df_list,columns=['datetime','instrument_id',k]))
        df=reduce(lambda x,y:x.merge(y,on=['datetime','instrument_id'],how='outer'),dfs)
        df = df.set_index('datetime')
        return df




