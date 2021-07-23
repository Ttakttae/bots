import pickle

player_Info = {}
with open("player_Info", 'wb') as fw:
    pickle.dump(player_Info, fw)