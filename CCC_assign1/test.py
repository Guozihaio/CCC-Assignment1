# Test.json
# This file is to read over the json file, and to output the result
# Created by zihaog1 931278, 2022-3-25 16:35:52
import json
import copy
from collections import Counter
import mmap
#from mpi4py import MPI

# open json file
with open("smallTwitter.json", "r+b") as big_f:
  mm =  mmap.mmap(big_f.fileno(), 0, access = mmap.ACCESS_READ)
  for line in iter(mm.readline, b""):
    print(type(line))
with open("smallTwitter.json", encoding = 'utf-8') as small_f:
    small_set = json.load(small_f)
with open("tinyTwitter.json", encoding = 'utf-8') as tiny_f:
    tiny_set = json.load(tiny_f)

with open("sydGrid.json", 'r', encoding = 'utf-8') as sydgrid_f:
    syd_grid = json.load(sydgrid_f)
grid_feature = syd_grid["features"]
# To justfy a coordinate whether in the grid or not
def in_area(coordinates):
    for k,v in AREA.items():
        if v[0][0] <= coordinates[0] <= v[2][0] and v[1][1] <= coordinates[1] <= v[0][1]:
            return k
# Create grid
D4 = copy.deepcopy(grid_feature[-1]["geometry"]["coordinates"][0])
C4 = copy.deepcopy(grid_feature[0]["geometry"]["coordinates"][0])
B4 = copy.deepcopy(grid_feature[1]["geometry"]["coordinates"][0])
A4 = copy.deepcopy(grid_feature[2]["geometry"]["coordinates"][0])
D3 = copy.deepcopy(grid_feature[3]["geometry"]["coordinates"][0])
C3 = copy.deepcopy(grid_feature[4]["geometry"]["coordinates"][0])
B3 = copy.deepcopy(grid_feature[5]["geometry"]["coordinates"][0])
A3 = copy.deepcopy(grid_feature[6]["geometry"]["coordinates"][0])
D2 = copy.deepcopy(grid_feature[7]["geometry"]["coordinates"][0])
C2 = copy.deepcopy(grid_feature[8]["geometry"]["coordinates"][0])
B2 = copy.deepcopy(grid_feature[9]["geometry"]["coordinates"][0])
A2 = copy.deepcopy(grid_feature[10]["geometry"]["coordinates"][0])
D1 = copy.deepcopy(grid_feature[11]["geometry"]["coordinates"][0])
C1 = copy.deepcopy(grid_feature[12]["geometry"]["coordinates"][0])
B1 = copy.deepcopy(grid_feature[13]["geometry"]["coordinates"][0])
A1 = copy.deepcopy(grid_feature[14]["geometry"]["coordinates"][0])

# Dictionary
AREA = {"A1": A1, "A2": A2, "A3": A3, "A4": A4, 
        "B1": B1, "B2": B2, "B3": B3, "B4": B4,
        "C1": C1, "C2": C2, "C3": C3, "C4": C4,
        "D1": D1, "D2": D2, "D3": D3, "D4": D4}

lang_dict = {"A1": [], "A2": [], "A3": [], "A4": [], 
             "B1": [], "B2": [], "B3": [], "B4": [],
             "C1": [], "C2": [], "C3": [], "C4": [],
             "D1": [], "D2": [], "D3": [], "D4": []}

ref_dict = {"en": "English (default)", "ar": "Arabic", "bn": "Bengali", "cs": "Czech", "da": "Danish", "de": "German", "el": "Greek", 
            "es": "Spanish", "fa": "Persian", "fi": "Finnish", "fil": "Filipino", "fr": "French", 
            "he": "Hebrew", "hi": "Hindi", "hu": "Hungarian", "id": "Indonesian", "it": "Italian", "ja":"Japanese", "ko":"Korean", 
            "msa": "Malay", "nl": "Dutch", "no": "Norwegian", "pl": "Polish", "pt": "Portuguese", 
            "ro": "Romanian", "ru": "Russian", "sv":"Swedish", "th":"Thai", "tr":"Turkish", "uk":"Ukrainian", "ur": "Urdu",
            "vi": "Vietnamese", "zh-cn": "Chinese", "zh-tw": "Chinese"}

lang_count = {"en": 0, "ar": 0, "bn": 0, "cs": 0, "da": 0, "de": 0, "el": 0, 
            "es": 0, "fa": 0, "fi": 0, "fil": 0, "fr": 0, 
            "he": 0, "hi": 0, "hu": 0, "id": 0, "it": 0, "ja":0, "ko":0, 
            "msa": 0, "nl": 0, "no": 0, "pl": 0, "pt": 0, 
            "ro": 0, "ru": 0, "sv":0, "th":0, "tr":0, "uk":0, "ur": 0,
            "vi": 0, "zh-cn": 0, "zh-tw": 0}

# data processing
tiny_rows = tiny_set['rows']
small_rows = small_set['rows']

lang_dict_2 = {"A1": [], "A2": [], "A3": [], "A4": [], 
               "B1": [], "B2": [], "B3": [], "B4": [],
               "C1": [], "C2": [], "C3": [], "C4": [],
               "D1": [], "D2": [], "D3": [], "D4": []}
new_lang_dict2 = copy.deepcopy(lang_dict_2)
for i in range(len(small_rows)):
    if small_rows[i]["doc"]["coordinates"] != None:
        #print(small_rows[i]["doc"]["id"])
        lang_dict_2[in_area(small_rows[i]["doc"]["coordinates"]["coordinates"])].append(small_rows[i]["doc"]["lang"])
    for k,v in lang_dict_2.items():
        c1 = Counter(v)
        new_lang_dict2[k] = dict(c1)
        
# output the result
print("Cell    #Total Tweets    #Number of Languages Used    #Top 10 Languages & #Tweets")
for area, lang_check in new_lang_dict2.items():
    top_lang = {}
    out_dict = {"num_lang": 0, "total_tweets": 0}
    for k, v in lang_check.items():
        top_lang[ref_dict[k]] = v
        out_dict["num_lang"]+=1
        out_dict["total_tweets"]+=v
    sort_lang = sorted(top_lang.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
    sort_lang = sort_lang[0:10]
    print(area, '    \t', out_dict["total_tweets"], "         \t",out_dict["num_lang"], "                     \t",sort_lang)