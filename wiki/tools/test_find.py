
data = [
        {'id':1,'parent_id':0},
        {'id':2,'parent_id':1},
        {'id':5,'parent_id':1},
        {'id':3,'parent_id':0},
        {'id':4,'parent_id':3},
        {'id':6,'parent_id':3},
]

# 输出：[ {'id':1,'children':[{'id':2}....]}, ]

def chat(data):
    res = []
    for i in data:
        if i['parent_id']==0:
            dic={}
            dic['id']=i['id']
            dic['children']=[]
            res.append(dic)
    for i in data:
        for j in res:
            if i['parent_id']==j['id']:
                dic={}
                dic['id']=i['id']
                j['children'].append(dic)
    return res

print(chat(data))


def find_father(input_list):
    home = {}
    parent_list = []
    for data in input_list:
        if data['parent_id'] == 0:
            dic = {}
            dic['id'] = data['id']
            parent_list.append(dic)
        else:
            p_id = data['parent_id']
            if p_id not in home:
                home[p_id] = []
                home[p_id].append({'id':data['id']})
            else:
                home[p_id].append({'id': data['id']})

            # home.setdefault(p_id,[])
            # home[p_id].append({'id': data['id']})

    for f in parent_list:
        if f['id'] in home:
            f['children'] = home[f['id']]
    return parent_list

print(find_father(data))

