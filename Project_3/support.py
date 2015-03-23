__author__ = 'krishna'

#!/usr/bin/env python3
import sys

class TA:
    def __init__(self,name):
        self.name = name
        self.timings = []
        self.skills = []

    def getTimings(self):
        return self.timings
    def setTimings(self,timingList):
        self.timings = timingList
    def getSkills(self):
        return self.skills
    def setSkills(self,skillsList):
        self.skills = skillsList
    def isMatch(self, course):
        for requirement in course.getRequirements():
            if requirement not in self.skills:
                #print " TA", self.name ,"Req Not matched ", self.skills , "<->", course.getRequirements()
                return False
        for timing in course.getRecitation():
            if timing in self.timings:
                #print " TA", self.name ," Timings matched ",self.timings , "<->", course.getRecitation()
                return False
        if course.getAttendLectures():
            for timing in course.getTimings():
                if timing in self.timings:
                    #print " TA", self.name ," Timings matched ", self.timings, "<->", course.getTimings()
                    return False
        return True
    def getTAscore(self, course):
        count = 0
        for requirement in course.getRequirements():
            if requirement in self.skills:
                count += 1
        for timing in course.getRecitation():
            if timing in self.timings:
                count = float('-inf')
        if course.getAttendLectures():
            for timing in course.getTimings():
                if timing in self.timings:
                    count = float('-inf')
        return count

    def __repr__(self):
        return self.name+" "+ str(self.timings)+" "+str(self.skills)+str("\n")


class Course:
    def __init__(self,courseNo):
        self.courseNo = courseNo
        self.timings = []
        self.recitation = []
        self.noTAs = 0
        self.requirements = []
        self.attendLectures = False

    def getTimings(self):
        return self.timings
    def setTimings(self,timingList):
        self.timings = timingList
    def getRecitation(self):
        return self.recitation
    def setRecitation(self,recitationList):
        self.recitation = recitationList
    def setNoTAs(self,noTA):
        self.noTAs = noTA
    def getNoTAs(self):
        return self.noTAs
    def setRequirements(self,requirements):
        self.requirements = requirements
    def getRequirements(self):
        return self.requirements
    def setAttendLectures(self,attendLectures):
        self.attendLectures = attendLectures
    def getAttendLectures(self):
        return self.attendLectures
    def __repr__(self):
        return self.courseNo+" "+ str(self.timings)+" "+str(self.recitation)+" "+str(self.noTAs)+str("\n")+\
               str(self.requirements)+" "+str(self.attendLectures)+"\n"