from collections import defaultdict
new_dic= defaultdict(dict)
new_dic['BOS']['Richard']=234
new_dic['BOS']['Einstein']=200
new_dic['ATL']['David']=100
for dic in new_dic['BOS']:
    print(dic,new_dic['BOS'][dic])