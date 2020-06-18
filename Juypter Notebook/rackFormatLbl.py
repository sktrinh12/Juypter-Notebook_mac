import numpy as np

def format24wellRack(lst,type='ld'):
    '''
    different ways to format the sbs 24 well format rack and number the well positions.
    ld = left down
    ldz = left down zig-zag
    lu = left up 
    rl = right left 
    lr = left right 
    '''
    type_1 = type[:1]
    type_2 = type[1:]
    numberlbls = [i for i in range(1,21)]
    if type_1 == "l" and "r" not in type:
        set_1 = numberlbls[0:5] 
        set_2 = numberlbls[5:10] 
        set_3 = numberlbls[10:15] 
        set_4 = numberlbls[15:20] 
    elif "r" in type:
        set_1 = numberlbls[0:4] 
        set_2 = numberlbls[4:8] 
        set_3 = numberlbls[8:12] 
        set_4 = numberlbls[12:16] 
        set_5 = numberlbls[16:20]
    
    if type_2 == "d" and type_1 == "l":
        arr = np.column_stack((set_1,set_2,set_3,set_4))
    elif type_2 == "u" and type_1 == "l":
        arr = np.column_stack((set_1[::-1],set_2,set_3[::-1],set_4))
    elif type_2 == "dz" and type_1 == "l":
        arr = np.column_stack((set_1,set_2[::-1],set_3,set_4[::-1]))

    if type_1 == "l" and type_2 == "r":
        arr = np.concatenate(([set_1],[set_2],[set_3],[set_4],[set_5]))
    elif type_1 == "r" and type_2 == "l":
        arr = np.concatenate(([set_1[::-1]],[set_2],[set_3[::-1]],[set_4],[set_5[::-1]]))
    print(arr)
    return [x for _,x in sorted(zip(arr.flatten().tolist(),lst))]

# import random 
# ran_lst = [random.randint(1,20) for i in range(20)]
# format24wellRack(ran_lst,'ldz')

with open('/Users/spencertrinh/Documents/datafiles/chemical_data.tsv', 'r') as f:
    contents = f.readlines()
#format24wellRack(contents[1:21],'ldz')

tecanlst = format24wellRack([i for i in range(1,21)],'ld')

format24wellRack(tecanlst,'lr')
