class Calculator:
    def varCalc(self, string, substitute):
        beggining = ""
        end = ""
        i = 0
        finished = False
        while not finished:
            finished = True
            for i in range(len(string)):
                if string[i] == "x":
                    finished = False
                    break
            if not finished:
                string = string[0:i] + self.convertNumber(substitute) + string[(i+1):len(string)]
        return self.calc(string)
        
    def calc(self, string):
        #This section runs through the equation simplifying it iteratively
        #and adhering to the order of operation.
        string = self.simpPar(string)
        string = self.simpExp(string)
        string = self.simpMulAndDiv(string)
        string = self.simpAddAndSub(string)
        #Turns the output string containing the simplified equation
        #into a number.
        return self.convertString( string )

    #Turns an input number into a string
    def convertString(self, string):
        try:
            returnValue = float(string)
        except ValueError:
            returnValue = int(string)
        return returnValue

    #Turns an input number into a string
    def convertNumber(self, string):
        try:
            returnValue = str(string)
        except ValueError:
            returnValue = None
        return returnValue

    #Tests to see if the string is a digit
    def isDigit(self, string):
        try:
            int(string)
            toReturn = True
        except:
            try:
                float(string)
                toReturn = True
            except:
                toReturn = False
        return toReturn

    #Finds all parentheses and simplifies their contents
    def simpPar(self, string):
        i = 0
        simplified = False
        #Iterates through the function until every parentheses
        #is simplified.
        while not simplified:
            #If this value stays true, the equation is simplified.
            simplified = True
            for i in range(len(string)):
                if string[i] == "(":
                    simplified = False
                    break
            if not simplified:
                index= [i,i]
                beggining = ""
                ending = ""
                middle = ""
                #Finds the closing parentheses
                while not index[0] > (len(string) - 2):
                    index[1] += 1
                    if string[index[1]] == ")":
                        break
                beggining = string[0:index[0]]
                ending = string[(index[1] + 1):len(string)]
                #Creates another instance of the calc function
                #treating the parentheses contents like the original
                #equation.
                middle = self.convertNumber(self.calc(string[(index[0] + 1):index[1]]) )
                #Concatenates the beggining, simplified expression, and ending.
                string = beggining + middle + ending
        #Returns a new equation devoid of parentheses
        #and with the expressions inside fully simplified
        return string

    #This simplifies all the exponential sections
    #of the equation.
    def simpExp(self, string):
        i = 0
        simplified = False
        while not simplified:
            simplified = True
            for i in range(len(string)):
                if string[i] == "^":
                    simplified = False
                    break
            if not simplified:
                index = [i,i,i]
                beggining = ""
                ending = ""
                middle = ""
                while not index[0] < 1:
                    index[0]-=1
                    if string == "":
                        break
                    elif (not self.isDigit(string[index[0]]) ) and (not string[index[0]] == "."):
                        break
                if index[0] > 0:
                    index[0]+=1
                while not index[2] > (len(string) - 2):
                    index[2]+=1
                    if (not self.isDigit(string[index[2]]) ) and (not string[index[0]] == "."):
                        break
                if index[2] < (len(string) - 1):
                    index[2]-=1
                beggining = string[0:(index[0])]
                ending = string[(index[2]+1):len(string)]
                middle = self.convertNumber(self.calcExponent( self.convertString(string[index[0]:index[1]]) , self.convertString(string[(index[1]+1):(index[2] + 1)]) ) )
                string = beggining + middle + ending
        return string

    def simpMulAndDiv(self, string):
        i = 0
        simplified = False
        while not simplified:
            simplified = True
            for i in range(len(string)):
                if string[i] == "*" or string[i] == "/":
                    simplified = False
                    break
            if not simplified:
                index = [i,i,i]
                beggining = ""
                ending = ""
                middle = ""
                firstString = ""
                secondString = ""
                while not index[0] < 1:
                    index[0]-=1
                    if string == "":
                        break
                    elif ( not self.isDigit(string[index[0]]) ) and (not string[index[0]] == "."):
                        break
                if index[0] > 0:
                    index[0]+=1
                while not index[2] > (len(string) - 2):
                    index[2]+=1
                    if ( not self.isDigit(string[index[2]]) ) and (not string[index[0]] == "."):
                        break
                if index[2] < (len(string) - 1):
                    index[2]-=1
                beggining = string[0:(index[0])]
                ending = string[(index[2]+1):len(string)]
                if string[index[1]] == "*":
                    middle = self.convertNumber(self.convertString(string[index[0]:index[1]]) * self.convertString(string[(index[1]+1):(index[2] + 1)]) )
                elif string[index[1]] == "/":
                    middle = self.convertNumber(self.convertString(string[index[0]:index[1]]) / self.convertString(string[(index[1]+1):(index[2] + 1)]) )
                string = beggining + middle + ending
        return string

    def simpAddAndSub(self, string):
        string += "+0"
        calcParts = ["",""]
        operation = ""
        place = 0
        for i in string:
            if self.isDigit(i) and (not i == "."):
                calcParts[place] += i
            else:
                if place == 0:
                    operation = i
                    place = 1
                else:
                    if operation == "+":
                        calcParts[0] = self.convertNumber( self.convertString(calcParts[0]) + self.convertString(calcParts[1]) )
                    else:
                        calcParts[0] = self.convertNumber( self.convertString(calcParts[0]) - self.convertString(calcParts[1]) )
                    calcParts[1] = ""
        return calcParts[0]

    def calcExponent(self, a, b):
        total = a
        for i in range(int(b) - 1):
            total *= a
        return total
        

myCalc = Calculator()
proceed = True
while proceed:
    value = raw_input("> ")
    print myCalc.calc(value)
