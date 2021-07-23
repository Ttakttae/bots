import pickle

player_list = []
player_Info = {}
with open("player_Info", 'wb') as fw:
    pickle.dump(player_list, fw)
    pickle.dump(player_Info, fw)
    