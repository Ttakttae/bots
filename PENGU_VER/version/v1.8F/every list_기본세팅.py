import pickle
# list_a = []
# with open("lolling.txt","wb") as fw: #쓰기
#     pickle.dump(list_a, fw)

with open("lolling.txt","rb") as fr: #읽기
    lolling_list = pickle.load(fr)
print(lolling_list)
print(len(lolling_list))
del lolling_list[14]
del lolling_list[13]
del lolling_list[12]
del lolling_list[11]
del lolling_list[10]
print(lolling_list)
with open("lolling.txt","wb") as fw: #쓰기
    pickle.dump(lolling_list, fw)