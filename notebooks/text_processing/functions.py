import re

url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
nums = re.compile(r'[+-]?\d+(?:\.\d+)?')
friends = re.compile(r'@[A-Za-z0-9]+')
spaces = re.compile(' +')

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
"]+", flags=re.UNICODE)

def remove_first_space(x):
    if x[0] == " ":
        return x[1:]
    else:
        return x

def pre_process_text_df(data):
    data['text'] = data['text'].apply((lambda x: re.sub('RT','', x))) #remove retweets
    data['text'] = data['text'].apply(lambda x: x.lower()) #lower all letters
    data['text'] = data['text'].apply((lambda x: nums.sub("N", x))) # all numbers are designed by N
    data['text'] = data['text'].apply((lambda x: emoji_pattern.sub("EMOJI", x))) # all emojis are designed by EMPOJI
    data['text'] = data['text'].apply((lambda x: url.sub("LINK", x))) # all links are designed by LINK
    data['text'] = data['text'].apply((lambda x: friends.sub("PERSON", x))) # all @person are designed by PERSON
    data['text'] = data['text'].apply(lambda x: x.replace('\n', ' ')) #substitute \n for " " 
    data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]', '', x))) #remove punctiantion 
    data['text'] = data['text'].apply((lambda x: spaces.sub(" ", x))) #remove double spaces
    data['text'] = data['text'].apply(remove_first_space) #remove space in the first position
    
    
def simple_pre_process_text_df(data):
    data['text'] = data['text'].apply((lambda x: re.sub('RT','', x)))
    data['text'] = data['text'].apply(lambda x: x.lower())
    data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
    data['text'] = data['text'].apply(remove_first_space) #remove space in the first position
    data['text'] = data['text'].apply((lambda x: spaces.sub(" ", x))) #remove double spaces
    
def simple_pre_process_text(sentence):
    sentence = sentence.lower()
    sentence = re.sub('[^a-zA-z0-9\s]','', sentence)
    return sentence