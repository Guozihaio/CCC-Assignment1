# newmain.py
# This file is to data processing and parallel reading
# Created at 2022-3-30 18:20:06

#import mmap
from multi import *
import copy
from collections import Counter
import sys
from mpi4py import MPI

''' MPI related states '''
# the communicator
comm = MPI.COMM_WORLD
# number of processes / size of the communicator
num_process = comm.Get_size()
# rank of the current process
rank = comm.Get_rank()
# on which node is the current process running
nodeName = MPI.Get_processor_name()
# load the information of the grid
json_path = sys.argv[1]
# load the information of the twitter dataset
twitter_path = sys.argv[2]
# num of lines to send in one time
batch_size = int(sys.argv[3])

# id of each grid
id_dict={"23":"C4", "22": "B4", "21":"A4", "20":"D3", 
             "19":"C3", "18": "B3", "17":"A3", "16":"D2", 
             "15":"C2", "14": "B2", "13":"A2", "12":"D1",
             "11":"C1", "10": "B1", "9" :"A1", "24":"D4"}

# reference dictionary, to match the language code to the language string
ref_dict = {"en": "English (default)", "ar": "Arabic", "bn": "Bengali", "cs": "Czech", "da": "Danish", "de": "German",  "el": "Greek", "es": "Spanish", "fa": "Persian", "fi": "Finnish", "fil": "Filipino", "fr": "French", 
            "he": "Hebrew", "hi": "Hindi", "hu": "Hungarian", "in": "Indonesian", "it": "Italian", "ja":"Japanese", "ko":"Korean", 
            "msa": "Malay", "nl": "Dutch", "no": "Norwegian", "pl": "Polish", "pt": "Portuguese", 
            "ro": "Romanian", "ru": "Russian", "sv":"Swedish", "th":"Thai", "tr":"Turkish", "uk":"Ukrainian", "ur": "Urdu",
            "vi": "Vietnamese", "zh": "Chinese", "zh-tw": "Chinese", "und": "Undetermined", "tl": "Tagalog", "ca": "Catalan", "ht": "Haitian", "et": "Estonian", "cy": "Welsh", "lt": "Lithuanian"}

# counter for each node    
lang_dict_t = {"A1": [], "A2": [], "A3": [], "A4": [], 
               "B1": [], "B2": [], "B3": [], "B4": [],
               "C1": [], "C2": [], "C3": [], "C4": [],
               "D1": [], "D2": [], "D3": [], "D4": []}
# all dict to use for count number of languages has been used               
new_lang_dict_t = copy.deepcopy(lang_dict_t)
merge_lang_dict = copy.deepcopy(lang_dict_t)
read_list = []

'''
To read a chuck of tweets
'''
def read_process():
    tweets = None
    for i in range(batch_size):
        line = big_f.readline()
        try: 
          if line == ']}\n': break
          else: tweets = line[0:-2]
          if tweets == "EOF": break
          if tweets[-1] == ",": # remove ","
            tweets = tweets[0:-1] 
          if line[-2] == "]": # remove ']'
            tweets = tweets[0:-2]
          if tweets[-1] == "]": break
        except:
          print("Here is Wrong")
          print(line)
        if tweets == "": break
        if tweets == "]}\n": break 
        read_list.append(tweets)

'''
To process one tweat
'''
def line_processing(listoflines):
  for line in listoflines:
      '''
      if line.startswith('{"id'):
          if line.endswith('},\r\n'):
              data = json.loads(line[:-3])
          else:
              data = json.loads(line[:-4])
      #print(parse) 
      '''
      data = json.loads(line)
      # only consider the tweat has the information of coordinates
      if data["doc"]["coordinates"] != None:
        for grids in grid_list:
            #print(grids)
            id = grids.check_if_coordinates_in_grid(data["doc"]["coordinates"]["coordinates"])
            if id is None: 
                continue
            place_name = id_dict[str(id)]
            language_used = data["doc"]["lang"]
            lang_dict_t[place_name].append(language_used)
            #print("My rank is", i, "I am doing my job")

'''
To merge all the results from slave nodes
'''     
def merge_all_dict():
  for i in recv_obj:
    for k,v in i.items():
      merge_lang_dict[k].extend(v)

#load Grid
f1 = open(json_path, 'r', encoding = 'utf-8')
syd_grid = json.load(f1)
grid_list  = []
for item in syd_grid['features']: grid_list.append(grid(item))

############################ read json begin ###################################

# open the twitter file for processing
with open(twitter_path, mode="r", encoding="utf-8", newline="\r\n") as big_f:
    # the first line of the twitter data is to record the num of lins, not important, skip
    big_f.readline()
    # initial position of the buffer reader
    position = big_f.tell()
    # each iteration first reads a chuck of lines
    while True:
        # each process reads a chuck, in ascending rank order
        for i in range(0, num_process):
            if rank == i: # my turn to read
                # move my handler to the position that last reader finsihed reading
                big_f.seek(position)
                read_process()
                # if EOF is reached, end the job
                if len(read_list) < batch_size: position = "EOF"
                # otherwise update to the latest position
                else: position = big_f.tell()
            # inform to other rank, the position of the file after the reading process 
            position = comm.bcast(position, root=i)
            if position == "EOF": break
        # process that batch
        if len(read_list) > 0: 
            line_processing(read_list)
            read_list = [] 
        # no more data to read and process
        if position == "EOF": break
############################ read json end ###################################

# Finshied the data processing, rank 0 to gather all information         
recv_obj = comm.gather(lang_dict_t , root=0)

# rank 0 to receive all the information, and output the result
if rank == 0:            
    merge_all_dict()
    for k,v in merge_lang_dict.items():
        c1 = Counter(v)
        new_lang_dict_t[k] = dict(c1)
    #print(recv_obj)
    print(new_lang_dict_t)    
    # output the result
    print("Cell    #Total Tweets    #Number of Languages Used    #Top 10 Languages & #Tweets")
    for area, lang_check in new_lang_dict_t.items():
        top_lang = {}
        out_dict = {"num_lang": 0, "total_tweets": 0}
        for k, v in lang_check.items():
            top_lang[ref_dict[k]] = v
            out_dict["num_lang"]+=1 
            out_dict["total_tweets"]+=v
        sort_lang = sorted(top_lang.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
        sort_lang = sort_lang[0:10]
        print(area, '    \t', out_dict["total_tweets"], "         \t",out_dict["num_lang"], "                     \t",sort_lang)
        #print(num_process)

            
            
            
            

            
            




        



    
    
    
    
