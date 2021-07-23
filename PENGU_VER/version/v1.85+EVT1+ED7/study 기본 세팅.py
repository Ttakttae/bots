import pickle


with open("study.txt","rb") as fr: #읽기
    study = pickle.load(fr)
del study['공지']
del study['버전']
del study['신']
with open("global_chet.txt","wb") as fw: #쓰기
    pickle.dump(study, fw)
print(study)