from asset.core.classifier import classifier
from asset.database_manage.dressRepo import insert_dress
from asset.database_manage.topRepo import insert_tops
from asset.database_manage.bottomRepo import insert_bottoms
from asset.database_manage.shoesRepo import insert_shoes

def DressManager(dress_path, model, user_id=0):
    data = classifier('dress', image_path=dress_path, model=model) 
    ret_data={'result':[]}
    for k in data:
        ret=[]
        dress={'type': None, 'color': None, 'pattern': None, 'material': None, 'fit': None, 'season': None, 'preference': None, 'style': None, 'image': None, 'features': None, 'category': None, 'uid': user_id}
        unique={'drid':None}
        try:
            for i,j in k.items():                
                if i not in dress:
                    unique[i]=j
                else:
                    dress[i]=j
            dress['image']=dress_path
            id= insert_dress(dress)
            # print(id)
            ret_data['result']+=[[dress]+[unique]]
            if id!=-1:
                unique['drid']=id
                if dress['category']=='top':
                    insert_tops(unique)
                if dress['category']=='bottom':
                    insert_bottoms(unique)
                if dress['category']=='shoes':
                    insert_shoes(unique)

        except Exception as e:
            print(e)
    return ret_data