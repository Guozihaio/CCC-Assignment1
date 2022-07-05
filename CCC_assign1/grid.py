import json
import copy
with open("sydGrid.json", 'r', encoding = 'utf-8') as sydgrid_f:
    syd_grid = json.load(sydgrid_f)
grid_feature = syd_grid["features"]

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

AREA = {"A1": A1, "A2": A2, "A3": A3, "A4": A4, 
        "B1": B1, "B2": B2, "B3": B3, "B4": B4,
        "C1": C1, "C2": C2, "C3": C3, "C4": C4,
        "D1": D1, "D2": D2, "D3": D3, "D4": D4}

# To justfy a coordinate whether in the grid or not
def in_area(coordinates):
    for k,v in AREA.items():
      if v[0][0] <= coordinates[0] <= v[2][0] and v[1][1] <= coordinates[1] <= v[0][1]:
          return k