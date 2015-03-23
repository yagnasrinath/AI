__author__ = 'krishna'

import support
import Queue

class CSP:
    def __init__(self, inp_file):
        self.inp_file = inp_file
        self.li_tables = self.extract_vals(inp_file)
        print "len of tables", len(self.li_tables)
        self.courses = self.build_courses()
        self.tas = self.build_tas()
        self.taCourseDict = {}
        self.courseTaDict = {}
        self.taNeighbours = {}
        self.buildCourseTaDict()
        self.buildTaCourseDict()
        self.buildTaNeighbours()
        self.result_co = {}
        self.result_ta = {}
        print self.courses
        print self.tas
        self.counter = 0

    def extract_vals(self, inp_file):
        fin = open(inp_file, 'r')
        tbl_tbl = []
        tbl = {}
        for line in fin:
            if(line.strip() == ''):
                tbl_tbl.append(tbl)
                tbl = {}
                continue
            self.process_line(line, tbl)
        tbl_tbl.append(tbl)
        fin.close()
        return tbl_tbl

    def process_line(self, line, tbl):
        row = line.split(',')
        #Should contain more than 1 elements
        if len(row) > 1:
            tbl[row[0].strip()] = [x.strip() for x in row[1:]]
        return

    def build_courses(self):
        gl_class = self.li_tables[0]
        rec_tbl = self.li_tables[1]
        cou_details = self.li_tables[2]
        cour_req = self.li_tables[3]
        courses_list = {}
        for key in gl_class:
            cou_obj = support.Course(key)
            for i in range(0, len(gl_class[key])/2):
                cou_obj.timings.append((gl_class[key][2*i], gl_class[key][2*i+1]))
            if rec_tbl.has_key(key):
                rec_entry = rec_tbl[key]
                cou_obj.recitation = [rec_entry[0], rec_entry[1]]
            cou_obj.noTAs = self.count_no_tas(int(cou_details[key][0]))
            cou_obj.requirements = cour_req[key]
            cou_obj.attendLectures = True if cou_details[key] == 'yes' else False
            courses_list[key] = cou_obj
        return courses_list

    def buildTaCourseDict(self):
        for ta in self.tas.keys():
            self.taCourseDict[ta]=[ c for c in self.courses.keys() if self.tas[ta].getTAscore(self.courses[c]) > 0.0 ]

    def buildCourseTaDict(self):
        for c in self.courses.keys():
            self.courseTaDict[c]=[ ta for ta in self.tas.keys() if self.tas[ta].getTAscore(self.courses[c]) > 0.0 ]

    def buildTaNeighbours(self):
        for ta in self.taCourseDict.keys():
            self.taNeighbours[ta] = [t for t in self.taCourseDict.keys() if ta != t and self.isNeighbour(self.taCourseDict[ta],self.taCourseDict[t])]

    def isNeighbour(self,ta1Courses, ta2Courses):
        for c1 in ta1Courses:
            if c1 in ta2Courses:
                return True
        return False

    def updateTaCourseDict(self):
        for ta in self.result_ta.keys():
            self.taCourseDict[ta]=[]
            if self.result_ta[ta][0] == float(0.0):
                self.taCourseDict[ta]= []
            else:
                for co in self.result_co.keys():
                    if self.result_co[co][0]> 0.0 and self.tas[ta].getTAscore(self.courses[co]) > 0.0:
                        self.taCourseDict[ta].append(co)


    def updateCourseTaDict(self):
        for co in self.result_co.keys():
            self.courseTaDict[co]=[]
            if self.result_co[co][0] == float(0.0):
                self.courseTaDict[co]= []
            else:
                for ta in self.result_ta.keys():
                    if self.result_ta[ta][0] > 0.0 and self.tas[ta].getTAscore(self.courses[co]) > 0.0:
                        self.courseTaDict[co].append(ta)

    def updateTaNeighbours(self):
        for ta in self.taCourseDict.keys():
            self.taNeighbours[ta] = [t for t in self.taCourseDict.keys() if ta != t and self.isNeighbour(self.taCourseDict[ta],self.taCourseDict[t])]

    def arc_cons(self):
        self.updateTaCourseDict()
        self.updateCourseTaDict()
        self.updateTaNeighbours()
        '''
        print "-------------ta=>courses---------------------"
        print self.taCourseDict
        print "-------------courses=>ta---------------------"
        print self.courseTaDict
        print "-------------ta=>ta---------------------"
        print self.taNeighbours
        print "----------------------------------------"
        '''
        q = Queue.Queue(maxsize=0)
        for ta in self.taNeighbours.keys():
            q.put(ta)
        while not q.empty():
            ta = q.get()
            for nb in self.taNeighbours[ta]:
                if self.rm_incons(ta, nb):
                    print "TA", ta
                    if len(self.taCourseDict) == 0 and self.result_ta[ta][0] > float(0):
                        return False
                    q.put(ta)
        return True

    def rm_incons(self, ta, nb):
        ta_co = self.taCourseDict[ta]
        nb_co = self.taCourseDict[nb]
        if len(ta_co) == 1:
            if ta_co[0] in nb_co:
                self.taCourseDict[ta] = []
                return True
        elif len(nb_co) == 1:
            if nb_co[0] in ta_co:
                self.taCourseDict[ta].remove(nb_co[0])
                return  True
        else :
            return False

    def count_no_tas(self, no_studs):
        if no_studs >= 60:
            return float(2.0)
        elif no_studs >= 40:
            return float(1.5)
        elif no_studs >= 25:
            return float(0.5)
        else:
            return float(0)

    def build_tas(self):
        resp = self.li_tables[4]
        skills = self.li_tables[5]
        tas_list = {}
        for key in skills:
            ta_obj = support.TA(key)
            for i in range(0, len(resp[key])/2):
                ta_obj.timings.append((resp[key][2*i], resp[key][2*i+1]))
            ta_obj.skills = skills[key]
            tas_list[key] = ta_obj
        return tas_list

    def solve_csp(self, type = 0):
        for key in self.courses.keys():
            self.result_co[key] = [float(self.courses[key].getNoTAs())]
        for key in self.tas.keys():
            self.result_ta[key] = [float(1)]
        self.type = type
        if self.__solve_csp():
            self.reduce_TAS()
            self.reduce_courses()
            for ta in sorted(self.result_ta.keys()):
                print ta, self.result_ta[ta]
            for co in sorted(self.result_co.keys()):
                print co, self.result_co[co]
            print "No of Nodes explored", self.counter
        else:
            print "No Sol Found!"
        return

    def __solve_csp(self):
        self.counter += 1
        #if(self.counter % 50 == 0):
        #   print "Courses ", self.result_co
        if self.base_cond():
            return True

        for course in self.courses.keys():
            if self.result_co[course][0] == float(0):
                continue
            for ta in self.build_ta_heap(self.courses[course]):
                if self.result_ta[ta][0] == float(0):
                    continue
                self.result_co[course][0] -= 0.5
                self.result_co[course].append([ta, 0.5])
                self.result_ta[ta][0] -= 0.5
                self.result_ta[ta].append([course, 0.5])
                if self.type == 1:
                    fcflag = self.do_fc()
                elif self.type == 2:
                    fcflag = self.arc_cons() and self.do_fc()
                else:
                    fcflag = True

                if fcflag and self.__solve_csp():
                    return True
                else:
                    self.result_co[course][0] += 0.5
                    self.result_co[course].pop()
                    self.result_ta[ta][0] += 0.5
                    self.result_ta[ta].pop()

        return False

    def base_cond(self):

        #for each course in courses
        cflag = 0
        for course in self.courses.keys():
            if self.result_co[course][0] != float(0):
                cflag = 1
        flag = 0
        for ta in self.tas.keys():
            if self.result_ta[ta][0] != float(0):
                flag = 1
        if flag == 0 or cflag == 0:
           return True

        return False

    def do_fc(self):
        if self.base_cond():
            return True
        for ta in self.result_ta.keys():
            if self.result_ta[ta][0] != float(0):
                flag = True
                for course in self.result_co.keys():
                    if self.result_co[course][0] != float(0):
                        if self.tas[ta].getTAscore(self.courses[course]) > float(0):
                            flag = False
                            break
                if flag == True:
                    return False
        return True

    def build_ta_heap(self, cou_obj):
        taq = Queue.PriorityQueue(maxsize=0)
        for ta in self.tas.keys():
            pri = self.tas[ta].getTAscore(cou_obj)
            taq.put((pri, ta))
        while not taq.empty():
            yield taq.get()[1]
    def reduce_TAS(self):
        for ta in self.result_ta.keys():
            li = self.result_ta[ta][1:]
            li_set = {}
            for l in li:
                li_set[l[0]] = l[1]
            li_res = []
            #print li_set
            for key in li_set:
                val = li_set[key]
                li_res.append([key, float(li.count([key, val]))/2])
            self.result_ta[ta] = li_res
    def reduce_courses(self):
        for co in self.result_co.keys():
            li = self.result_co[co][1:]
            li_set = {}
            for l in li:
                li_set[l[0]] = l[1]
            li_res = []
            #print li_set
            for key in li_set:
                val = li_set[key]
                li_res.append([key, float(li.count([key, val]))/2])
            self.result_co[co] = li_res

csp_obj = CSP('dataset')
#print csp_obj.taNeighbours
#print csp_obj.taCourseDict
#print csp_obj.courseTaDict
csp_obj.solve_csp(2)


