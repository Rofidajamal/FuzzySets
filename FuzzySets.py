
class variable:
    def __init__(self):
        self.fuzzysets = fuzzySet ()
        self.range = None
        self.crisp = None
        self.name = None

    def setName(self, n):
        self.name = n

    def getName(self):
        return self.name

    def setCrisp(self, c):
        self.crisp = c

    def getCrisp(self):
        return self.crisp

    def setRange(self, r):
        self.range = r

    def getRange(self):
        return self.range

    def setFuzzySet(self, l1):
        self.fuzzysets = l1

    def getFuzzySet(self):
        return self.fuzzysets

    def fuzzification(self, ):
        crisp = variable.getCrisp (self)
        for j in self.fuzzysets:
            if (crisp < j.x_coordinates[0] or crisp > j.x_coordinates[-1]):  # value outside set
                j.set_member (0)
                # print(member)
            elif (crisp > j.x_coordinates[0] or crisp < j.x_coordinates[-1]):  # value inside set
                for x in range (0, len (j.x_coordinates)):
                    if (crisp == j.x_coordinates[x]):
                        # j.gety()
                        j.set_member (j.y_coordinates[x])
                    else:
                        for x in range (0, len (j.x_coordinates) - 1):
                            if (crisp >= j.x_coordinates[x] and crisp <= j.x_coordinates[x + 1]):
                                m = (j.y_coordinates[x + 1] - j.y_coordinates[x]) / (
                                            j.x_coordinates[x + 1] - j.x_coordinates[x])
                                c = j.y_coordinates[x] - m * j.x_coordinates[x]
                                j.set_member (m * crisp + c)


class fuzzySet:
    def __init__(self):
        self.name = None
        self.type = None
        self.x_coordinates = None
        self.y_coordinates = None
        self.member = None

    def setName(self, n):
        self.name = n

    def getName(self):
        return self.name

    def setType(self, t):
        self.type = t

    def getType(self):
        return self.type

    def setx(self, x):
        self.x_coordinates = x

    def getx(self):
        return self.x_coordinates

    def sety(self):
        if (self.getType () == "TRI"):
            self.y_coordinates = [0, 1, 0]
        elif (self.getType () == "TRAP"):
            self.y_coordinates = [0, 1, 1, 0]

    def gety(self):
        return self.y_coordinates

    def set_member(self, m):
        self.member = m

    def get_member(self):
        return self.member




def inference(var, sets, mem, line):
    f = 0
    list_line = line.split ()
    if var[0].getName () == list_line[0]:
        index1 = next ((i for i, obj in enumerate (sets) if obj.getName () == list_line[1]), -1)
        index2 = next ((i for i, obj in enumerate (sets) if obj.getName () == list_line[4]), -1)
        if list_line[2] == "and":
            f = (min (mem[index1], mem[index2]))
        elif list_line[2] == "and_not":
            f = (min (mem[index1], 1 - mem[index2]))
        elif list_line[2] == "or_not":
            f = (max (mem[index1], 1 - mem[index2]))
        else:
            f = (max (mem[index1], mem[index2]))


    elif var[1].getName () == list_line[0]:
        index1 = next ((i for i, obj in enumerate (sets) if obj.getName () == list_line[1]), -1)
        index2 = next ((i for i, obj in enumerate (sets) if obj.getName () == list_line[4]), -1)
        if list_line[2] == "and":
            f = (min (mem[index1], mem[index2]))
        elif list_line[2] == "and_not":
            f = (min (mem[index1], 1 - mem[index2]))
        elif list_line[2] == "or_not":
            f = (max (mem[index1], 1 - mem[index2]))
        else:
            f = (max (mem[index1], mem[index2]))
    return f


import numpy as np


def Defuzzification(membership_output,
                    output_position_list):  # membership_output came from inference , #output_position_list numbers will user enter
    fuzzy_output = 0  # final output
    Centroid = 0  # z* =∑𝝁(𝒛̅).̅𝒛∑𝝁(𝒛̅) equation of calc centrioied
    arr_position = np.array (membership_output)

    Centroid += (sum (output_position_list)) / len (output_position_list)
    for i in range (0, len (arr_position)):
        z = arr_position[i]  # to multiply the membership with the cetroied
        fuzzy_output += Centroid * z

    return fuzzy_output


print("Fuzzy Logic Toolbox")
print("===================")
print("1- Create a new fuzzy system")
print("2- Quit")
flag  =0
create = int (input ())
Inf_list = []
LINES = []
list_vOut = []
list_s = []
m =[]
while(True):
        if(create == 2):
            break
        else:
            list_o = []
            list_v = []
            file_or_not = 0
            file_or_not = int(input("if you want read form file Enter 1 "))

            if(file_or_not == 1):
                m =[]
                with open('input.txt', 'r') as fname:
                    inputs = fname.readlines()
                    cleanInput=[]
                    for x in inputs:
                        val = x.strip()
                        cleanInput.append(val)

                no_v = int(cleanInput[0])
                b = 1
                for k in range (0, no_v):
                    v1 = variable ()
                    v1.setName(cleanInput[b] )
                    b+=1
                    v1.setCrisp (int(cleanInput[b]))
                    list_v.append (v1)
                    b+=1

                no_f = int(cleanInput[b])
                for k in range (0, no_v):
                    for i in range (0, no_f):
                        b+=1
                        temp = fuzzySet ()
                        temp.setName (cleanInput[b])
                        #print(temp.getName())
                        b += 1
                        temp.setType (cleanInput[b])
                        #print (temp.getType ())
                        b+=1
                        temp_x = cleanInput[b].split ()
                        temp_x2 = [int (x) for x in temp_x[:]]
                        #print (temp_x2)
                        temp.setx (temp_x2)
                        temp.sety ()
                        list_o.append (temp)  # list of fuzzyset objects
                        # list of variables
                        list_v[k].setFuzzySet(list_o)
                    b+=1
                    no_f = int(cleanInput[b])



                for v in range (0, len (list_v)):
                    list_v[v].fuzzification ()
                    for set in list_v[v].getFuzzySet ():
                        m.append (set.member)
                import matplotlib.pyplot as plt
                for l in range(0,len(list_v)):
                    fuzzy = list_v[l].getFuzzySet()
                    for i in range (0,len(list_o)):
                        xplot = fuzzy[i].x_coordinates
                        yplot = fuzzy[i].y_coordinates
                        nameVar = list_v[l].getName()
                        nameFuzzy = fuzzy[i].getName()
                        name = "the plot in variable  " + nameVar
                        plt.plot(xplot,yplot)
                        plt.title(name)
                        plt.show()



                Inf_list = []
                LINES = []
                num = int(cleanInput[b])

                for i in range (0, num):
                    b += 1
                    line =cleanInput[b]
                    LINES.append (line)
                # need var list , sets list and mem list to be ready before enter the loop

                for i in range (0, len (list_v)):
                    for K in range (0, len (LINES)):
                        Inf_list.append (inference (list_v, list_v[i].getFuzzySet (), m, LINES[K]))


                # to take more than output variable
                list_s = []
                list_vOut = []
                b+=1
                no_v = int (cleanInput[b])

                for i in range (0, no_v):
                    b+=1
                    v1 = variable ()
                    v1_name = cleanInput[b]
                    v1.setName (v1_name)
                    list_vOut.append (v1)

                for k in range (0, no_v):
                    b+=1
                    no_f = int (cleanInput[b])
                    for i in range (0, no_f):
                        b+=1
                        temp = fuzzySet ()
                        temp.setName ( cleanInput[b])
                        b+=1
                        temp.setType ( cleanInput[b])
                        b+=1
                        temp_x =  cleanInput[b].split ()
                        temp_x2 = [int (x) for x in temp_x[:]]
                        temp.setx (temp_x2)
                        temp.sety ()
                        list_s.append (temp)  # list of fuzzyset objects
                        # list of variables
                    list_vOut[k].setFuzzySet(list_s)
                import matplotlib.pyplot as plt
                for l in range(0,len(list_vOut)):
                    fuzzy = list_v[l].getFuzzySet()
                    for i in range (0,len(list_s)):
                        xplot = fuzzy[i].x_coordinates
                        yplot = fuzzy[i].y_coordinates
                        nameVar = list_vOut[l].getName()
                        nameFuzzy = fuzzy[i].getName()
                        name = "the plot of out variable  " + nameVar
                        plt.plot(xplot,yplot)
                        plt.title(name)
                        plt.show()

                x = []
                y = []
                final_output =0
                for i in range (0, len (list_vOut)):
                    x = list_vOut[i].fuzzysets
                    for k in range (0, len (x)):
                        if (x[k].getName () == "normal"):
                            y = x[k].x_coordinates
                            final_output = Defuzzification (Inf_list, y)
                    out=f'the predicted of {list_vOut[i].getName ()} ',"is normal ( %2.1f )  " %final_output
                    print (out)
                    f = open('output.txt',"w")
                    f.write(str(out))
                    f.close()


                m = []
                list_vOut = []
                list_s = []
            else:
                while(True):
                    R = int(input("1- Add variables. \n2- add fuzzy sets \n3- Add rules. \n4- Run the simulation on crisp values."))
                    if(R == 1):
                        flag = 1
                        no_v = int(input("enter the number of variables"))

                        for k in range (0, no_v):
                            v1 = variable ()
                            v1_name = input ("enter variable name")
                            v1.setName (v1_name)
                            v1_crisp = int (input ("enter variable crisp values"))
                            v1.setCrisp (v1_crisp)
                            list_v.append (v1)
                    elif(R ==2):
                        if(flag != 1):
                            print("you should enter variables first")
                            break
                        flag =2

                        for k in range (0, len (list_v)):
                            no_f = int (input ("enter number of fuzzy sets"))
                            for i in range (0, no_f):
                                temp = fuzzySet ()
                                temp_name = input ("enter the name of the fuzzy set")
                                temp.setName (temp_name)
                                temp_type = input ("enter the type of the fuzzy set")
                                temp.setType (temp_type)
                                temp_x = input ("enter x coordinates").split ()
                                temp_x2 = [int (x) for x in temp_x[:]]
                                temp.setx (temp_x2)
                                temp.sety ()
                                list_o.append (temp)  # list of fuzzyset objects
                                # list of variables
                            list_v[k].setFuzzySet (list_o)

                        for v in range (0, len (list_v)):
                            list_v[v].fuzzification()
                            for set in list_v[v].getFuzzySet():
                                m.append (set.member)

                        import matplotlib.pyplot as plt

                        for l in range (0, len (list_v)):
                            fuzzy = list_v[l].getFuzzySet ()
                            for i in range (0, len (list_o)):
                                xplot = fuzzy[i].x_coordinates
                                yplot = fuzzy[i].y_coordinates
                                nameVar = list_v[l].getName ()
                                nameFuzzy = fuzzy[i].getName ()
                                name = "the plot in variable  " + nameVar
                                plt.plot (xplot, yplot)
                                plt.title (name)
                                plt.show ()

                    elif R == 3 :
                        if(flag != 2):
                            print("you should add Fuzzy sets first")
                            break
                        else:
                            flag = 3

                            # take input from user as for loop each line in one iteration and call inference function
                            # pass to it list of variable name var=[v1.name,v2.name] , list of sets name set=[set1.name,..],
                            # list of member ship for each set mem=[set1.member,set2.member, ...]

                            # number of fuzzy rules
                            Inf_list =[]
                            num = int (input ("enter the number of rules you will write "))
                            for i in range (0, num):
                                line = input ("enter one rule at a time")
                                LINES.append (line)
                            # need var list , sets list and mem list to be ready before enter the loop
                            for i in range (0, len (list_v)):
                                for K in range (0, len (LINES)):
                                    Inf_list.append (inference (list_v, list_v[i].getFuzzySet (), m, LINES[K]))



                    # to take more than output variable
                    elif R == 4:
                        if flag != 3:
                            print("you should enter rules first")
                            break
                        else:
                            no_v = int (input ("enter the number of output variables "))
                            for i in range (0, no_v):
                                v1 = variable ()
                                v1_name = input ("enter variable name")
                                v1.setName (v1_name)
                                list_vOut.append (v1)

                            for k in range (0, no_v):
                                no_f = int (input ("enter number of fuzzy sets for the output variable"))
                                for i in range (0, no_f):
                                    temp = fuzzySet ()
                                    temp_name = input ("enter the name of the fuzzy set")
                                    temp.setName (temp_name)
                                    temp_type = input ("enter the type of the fuzzy set")
                                    temp.setType (temp_type)
                                    temp_x = input ("enter x coordinates").split ()
                                    temp_x2 = [int (x) for x in temp_x[:]]
                                    temp.setx (temp_x2)
                                    temp.sety ()
                                    list_s.append (temp)  # list of fuzzyset objects
                                    # list of variables
                                list_vOut[k].setFuzzySet (list_s)

                                # calling of the function


                            x = []
                            y = []
                            final_output =0
                            for i in range (0, len (list_vOut)):
                                    x = list_vOut[i].fuzzysets
                                    for k in range (0, len (x)):
                                        if (x[k].getName () == "normal"):
                                            y = x[k].x_coordinates
                                            final_output = Defuzzification (Inf_list, y)
                            print (f'the predicted of {list_vOut[i].getName ()} ',"is normal ( %2.1f )  " %final_output)
                    else:
                        break
