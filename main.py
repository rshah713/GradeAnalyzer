#!/usr/bin/env python
# coding: utf-8

"""
Save HTML file of specific Genesis class
    - format: https://parents.ewrsd.k12.nj.us/genesis/parents?tab1=studentdata&tab2=gradebook&tab3...
Program built to parse and extract existing grades and values to predict assignment

Use sliders to predict grade
    - target grade slider: will reveal next assignment weight to achieve
    - next weight slider: points needed on next assignment to end with target_grade slider
    
"""

import os
from bs4 import BeautifulSoup

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


######################## HTML PARSER ########################
PTS_ACHIEVED = 0
TTL_POINTS = 0
CURRENT_GRADE = 0


def read_file(file):
    global html
    html_f = open(file, 'r')
    html = html_f.read()
    html = os.linesep.join([s for s in html.splitlines() if s])
    html_f.close()


def process_data():
    global PTS_ACHIEVED, TTL_POINTS, CURRENT_GRADE
    parsed_html = BeautifulSoup(html)
    html_body = parsed_html.body.find_all('td', attrs={'class':'cellLeft', 'align':'right'})
    classname = parsed_html.body.find_all('option', attrs={'selected':True})[2].text
    
    total = [] # 2d list where each element is [10, 10, '100.0%'] (see 'res' key below )
    for i in html_body:
        res = i.text.split('\n')
        res = [name for name in res if name.strip()]
        for ind in range(len(res)):
            res[ind] = res[ind].strip()
        
        res[0] = float(res[0])
        res[1] = int(res[1].split(' ')[1])
        total.append(res)
        
    # res: ['7', '/ 10', '70.0%'] where 
    # res[0] -> points achieved
    # res[1] -> total points
    # res[2] -> grade in percent
    
    PTS_ACHIEVED = 0
    TTL_POINTS = 0
    for row in total:
        PTS_ACHIEVED += row[0]
        TTL_POINTS += row[1]

    CURRENT_GRADE = PTS_ACHIEVED / TTL_POINTS * 100
    
######################## DATA ANALYSIS ########################

def points_needed(target_grade, next_assignment_weight):
    """ given a target final grade and weight of next assignment
    calculate the grade needed on the next assignment"""
    points_needed = (target_grade/100 * (TTL_POINTS+next_assignment_weight)) - PTS_ACHIEVED
    return points_needed

def weight_needed(target_grade):
    """assuming you receive 100 on the next grade,
    how many points u need to hit target grade"""
    
    # IM A GENIUS FOR FIGURING THIS FORMULA OUT
    # weight_needed = ((final grade * total weight) - (100 * achieved points)) / (100 - final grade)
    weight_needed = (target_grade * TTL_POINTS) - (100 * PTS_ACHIEVED)
    weight_needed /= abs(100 - target_grade)
    return weight_needed

def maintain_current_grade(w):
    return points_needed(CURRENT_GRADE, w)


pts_needed = points_needed(90, 40)
maintain = maintain_current_grade(30)
weight = weight_needed(93)

print("Need a {}/{} (a {:.2f}%) to end with an {}".format(pts_needed, 40, pts_needed*100/40, 90))
print("Need a 100% on a {:.2f}pt assignment to end with a {}".format(weight, 93))
print("Need a {}/{} (a {:.2f}%) to maintain current grade".format(maintain, 30, maintain*100/30))

######################## KIVY GUI ########################

kv = Builder.load_file("GradeAnalyzer.kv")

class Main(Widget):
    target = 0
    weight = 0
    txtinpt = ObjectProperty(None)
    
    def target_grade(self, *args):
        self.target = round(args[1], 2)
        self.targetlabel.text = "Target Grade: " + self.get_target()
        weight = weight_needed(self.target)
        self.weightneeded.text = "{:.2f}pt assignment to reach {}%".format(weight, self.target)
        
    def read_data(self, filename):
        read_file(filename)
        process_data()
        
    def get_target(self):
        return str(self.target)
        
    def next_weight(self, *args):
        self.weight = args[1]
        self.weightlabel.text = "Next Assignment Weight: " + self.get_weight()
        pts_needed = points_needed(self.target, self.weight)
        self.pointsneeded.text = "Need a {:.2f}/{} (a {:.2f}%) to end with an {}".format(pts_needed, self.weight, pts_needed*100/self.weight, self.target)
        
    def get_weight(self):
        return str(int(self.weight))
        
    
class GradeAnalyzerApp(App):
    def build(self):
        return Main()

GradeAnalyzerApp().run()
