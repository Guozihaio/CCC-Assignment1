import json
from typing import Tuple

class grid:
    def __init__(self,json_data="/COMP90024/ASSIGNMENT 1/sydGrid-2.json"):
        lan_dict = {"en": 0, "ar": 0, "bn": 0, "cs": 0, "da": 0, "de": 0, "el": 0, 
            "es": 0, "fa": 0, "fi": 0, "fil": 0, "fr": 0, 
            "he": 0, "hi": 0, "hu": 0, "id": 0, "it": 0, "ja":0, "ko":0, 
            "msa": 0, "nl": 0, "no": 0, "pl": 0, "pt": 0, 
            "ro": 0, "ru": 0, "sv":0, "th":0, "tr":0, "uk":0, "ur": 0,
            "vi": 0, "zh-cn": 0, "zh-tw": 0}
        id_dict={"23":"C4", "22": "B4", "21":"A4", "20":"D3", 
                 "19":"C3", "18": "B3", "17":"A3", "16":"D2", 
                 "15":"C2", "14": "B2", "13":"A2", "12":"D1",
                 "11":"C1", "10": "B1", "9" :"A1", "24":"D4"}
        self.json_data = json_data
        self.id = self.json_data["properties"]['id']
        self.lefttop = self.json_data['geometry']['coordinates'][0][0]
        self.leftbottom = self.json_data['geometry']['coordinates'][0][1]
        self.rightbottom = self.json_data['geometry']['coordinates'][0][2]
        self.righttop = self.json_data['geometry']['coordinates'][0][3]
        self.lan_dict = lan_dict
    #To check whether is a vaild language, if not, detect it
    def check_if_language_exist(self,lan):
        if lan in self.lan_dict:
            self.lan_dict[lan] = self.lan_dict[lan] + 1
        else:
            self.lan_dict[lan] = 1
    #To check whether a coordinate locates at a grid
    def check_if_coordinates_in_grid(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        if self.lefttop[0]<x<=self.righttop[0] and self.rightbottom[1]<=y<self.righttop[1]:
            return self.id
        else:
            return None
           
class twitter:
    def __init__(self,json_data = None):
        self.json_data = json_data
        self.lang = self.json_data["doc"]["lang"]
        self.coordinates = self.json_data["doc"]["coordinates"]["coordinates"]
        
class Grid_info:
    def create_grids(self,json_path="/COMP90024/ASSIGNMENT 1/sydGrid-2.json"):
        f1 = open(json_path, 'r', encoding = 'utf-8')
        syd_grid = json.load(f1)
        grid_list  = []
        for item in syd_grid['features']:
            grid_list.append(grid(item))
        return grid_list
