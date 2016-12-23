
import requests
import json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

flickr_key = '98ce5738477c46cdb09822c212d6c844'
if not flickr_key:
    flickr_key = raw_input("Enter your flickr API key, or paste it in the .py file to avoid this prompt in the future: \n>>")

def flickrREST(baseurl = 'https://api.flickr.com/services/rest/',
    method = 'flickr.photos.search',
    api_key = flickr_key,
    format = 'json',
    extra_params={}):
    d = {}
    d['method'] = method
    d['api_key'] = api_key
    d['format'] = format
    for k in extra_params:
        d[k] = extra_params[k]
    return requests.get(baseurl, params = d)

def fix_flickr_resp(response_string):
    return response_string[len("jsonFlickrApi("):-1]

wordinput = raw_input("Insert word here without pressing space")

search = flickrREST(extra_params = {'tags' : wordinput, 'tag_mode': 'all', 'per_page' : 250, })
tag_dict = json.loads(search.text[14:-1])

photoID = []
photos = tag_dict['photos']['photo']
for photo in photos:
    photoID.append(photo['id'])
    
info_d = {}

for x in photoID:
    flickrx = flickrREST(method = 'flickr.photos.getInfo', extra_params = {'photo_id' : x})
    flickry = fix_flickr_resp(flickrx.text)
    flickry = json.loads(flickry)
    dock = flickry['photo']['tags3']['tag']
    for i in dock:
        if i['_content'] not in info_d:
            info_d[i['_content']] = 1
        else:
            info_d[i['_content']] += 1


tag_list = sorted(info_d, key = lambda x: info_d[x], reverse = True)
flickr_words = tag_list

#http://words.bighugelabs.com/api/2/3f6ae50ada8ac1fb1937c80eddb1fcf1/ocean/json
#Params for the request
word = wordinput
format= '/json'
api_key = '/3f6ae50ada8ac1fb1937c80eddb1fcf1/'
apitype = 'api'
version = '/2'

def getfromthesaurus(baseurl = 'http://words.bighugelabs.com/'):
    t_response = requests.get(baseurl + apitype + version + api_key + word + format)
    t_data = json.loads(t_response.text)
    return t_data
t_dict = getfromthesaurus()



wordtype = raw_input("Enter the type of word, type 'noun' for a noun, 'verb' for a verb, 'adjective' for an adjective")


def extract_words(data = t_dict):
    t_list = data[wordtype]["syn"]
    return t_list
t_words1 = extract_words()

def get_rid_of_spaces(l):
    better_words = [x.replace(" ", "") for x in l]
    return better_words
t_words = get_rid_of_spaces(t_words1)

def get_top5(lst):
    return lst[0:5]
top_five_flickr = str(sorted(get_top5(flickr_words), key= len))
top_five_synonyms = str(sorted(get_top5(t_words), key = len))



class Percentage():
    def __init__(self, flickr_list, synonyms_list):
        self.flickr_keys = flickr_list
        self.synonyms = synonyms_list
        self.top5_synonyms = synonyms_list[0:5]
        self.top5_flickr_keys = flickr_list[0:5]
   
    def Overall_Prediction_Score(self):
        ops = 0
        max_score = float(len(self.synonyms))
        for a_word in self.flickr_keys:
            if a_word in self.synonyms:
                ops = ops + 1
        percent_score = (ops/max_score) * 100
        try:
            return percent_score
        except:
            print "There is something wrong with this function"

    def Top5_Prediction_Score(self):
        ops = 0
        max_score = 5.0
        for a_word in self.top5_flickr_keys:
            if a_word in self.top5_synonyms:
                ops = ops + 1
        percent_score = (ops/max_score) * 100
        try:
            return percent_score
        except:
            print "There is something wrong with this function"

Percentages = Percentage(flickr_words, t_words)
Top5_Percentages = Percentages.Top5_Prediction_Score()
Overall_Percentages = Percentages.Overall_Prediction_Score()

Amount_of_synonyms = str(len(t_words))

try:
    print "The top five Flickr keys most commonly found with" + " " + wordinput + " " + "are" + " " + str(top_five_flickr)
    print "-------------------------------------------------------------"
    print "There are" + " " + Amount_of_synonyms + " " + "synonyms for" + " " + wordinput
    print "The top five most common synonyms of" + " " + wordinput + " " + "are" + " " + str(top_five_synonyms)
    print "-------------------------------------------------------------"
except:
    print "There is something wrong with either the get_top5 function or the extract_words function"



print "-------------------------------------------------------------"
print "The percentage of the top five Flickr keys most commonly found with" + " " + wordinput + " " + "on Flickr that are also in the top five synonyms for" + " " + wordinput + " " + "is" + " " + str(Top5_Percentages) + "%"
print "-------------------------------------------------------------"
print "The percentage of the all of the top Flickr keys most commonly found with" + " " + wordinput + " " + "that are also synonyms for " + " " + wordinput + " " "is" + " " + str(Overall_Percentages) + "%"
print "-------------------------------------------------------------"
print "My personal reccomendation on using Flickr to predict synonyms for this word? It's:" 

if Overall_Percentages < 20:
    print "Flickr seemed to a terrible predictor for synonyms for this word"
if 20 <= Overall_Percentages < 40:
    print "Flickr is definitely not a great way to predict synonyms for this word"
if 40 <= Overall_Percentages < 60:
    print "Flickr really isn't too bad at predicting synonyms for this word"
if 60 <= Overall_Percentages < 80:
    print "I'm not saying Flickr is Thesaurus.com, but it's not a bad substitute for this word"
if 80 <= Overall_Percentages < 100:
    print "Why use Thesaurus.com? Flickr gives the same results and has cool pictures"

print "-------------------------------------------------------------"
print "A file named Flickr_Prediction.csv has been made showing these results"



word_stats = (str(top_five_flickr), str(top_five_synonyms), Overall_Percentages, Top5_Percentages)
outfile = open('Flickr_Prediction.csv', 'w')
outfile.write('Top 5 Flickr Keys, Top 5 Synonyms, Overall Predictor Percentage, Top 5 Predictor Percentage' + '\n')
outfile.write('"%s","%s", "%d", "%d" \n' % word_stats)
outfile.close()





