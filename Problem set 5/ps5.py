# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrases):
        #self.text = text
        self.phrases = phrases
    def is_phrase_in(self, text):
        s = text
        for p in string.punctuation:
            s = s.replace(p, " ")
        
        s = s.lower().split()
        phrases = self.phrases.lower().split()

        count = 0
        u = 0
        
        for phrase in phrases:
            if phrase in s:
                i = s.index(phrase)
                if i == 0 or i - u == 1 or u == 0:
                    if u > i:
                        break
                    else:
                        count += 1
                        u = i

        if count == len(phrases):
            return True   
        else:
            return False
# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, stroy):
        return self.is_phrase_in(stroy.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self,story):
        return self.is_phrase_in(story.get_description())
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time_aware = self.aware(time)
        self.time_naive = self.naive(time)
    def aware(self, time):
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        time = time.replace(tzinfo=pytz.timezone("EST"))
        return time
    def naive(self, time):
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        return time
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):  
  def evaluate(self, story):
    if story.get_pubdate().tzinfo != None:
        return self.time_aware > story.get_pubdate()
    elif self.time_naive != None:
        return self.time_naive > story.get_pubdate()

class AfterTrigger(TimeTrigger):
  def evaluate(self, story):
    if story.get_pubdate().tzinfo is not None:
        return self.time_aware < story.get_pubdate()
    else:
        return self.time_naive < story.get_pubdate()
    # return self.time_aware < story.get_pubdate() or self.time_naive < story.get_pubdate()


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, Trig):
        self.trig = Trig
    
    def evaluate(self, story):
        return not self.trig.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, Trig1, Trig2):
        self.trig1 = Trig1
        self.trig2 = Trig2
    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, Trig1, Trig2):
        self.trig1 = Trig1
        self.trig2 = Trig2
    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    new_stories_list = []

    for story in stories:
        for trigger in triggerlist:
            if story not in new_stories_list and trigger.evaluate(story):
                new_stories_list.append(story)

    return new_stories_list
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    # return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)


        

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    list_of_trigs = []
    trig_dict = {}
    func_trig_dict = {"TITLE": TitleTrigger, "DESCRIPTION": DescriptionTrigger, "AFTER": AfterTrigger, "BEFORE": AfterTrigger, "NOT": NotTrigger, "OR": OrTrigger, "AND": AndTrigger}
    for line in lines:
        line_split = line.split(',')
        print(line_split)
        if line_split[0] == 'ADD':
            for t in line_split[1:]:
                print(t)
                if trig_dict.get(t):
                    list_of_trigs.append(trig_dict[t])
                    print(list_of_trigs)
        else:
            trig_name = line_split[0]
            trig_func = line_split[1]
            trig = func_trig_dict[trig_func]
            print(trig)
            if trig_func == 'NOT':
                ti1 = line_split[2]
                trig_dict[trig_name] = trig(trig_dict[ti1])
                print(trig_dict)
            elif trig_func == 'OR' or trig_func == 'AND':
                ti1 = line_split[2]
                ti2 = line_split[3]
                trig_dict[trig_name] = trig(trig_dict[ti1], trig_dict[ti2])
                print(trig_dict)
            else:
                trig_dict[trig_name] = trig(line_split[2])
                print(trig_dict)
    return list_of_trigs
                
            
    

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("melania")
        # t2 = DescriptionTrigger("some")
        # t3 = DescriptionTrigger("apple")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

