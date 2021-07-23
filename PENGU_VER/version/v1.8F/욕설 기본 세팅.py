import pickle
list_a = {}
with open("bad_list.txt","wb") as fw: #쓰기
    pickle.dump(list_a, fw)