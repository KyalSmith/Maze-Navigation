import json
import requests
import sys

def main():
    outputFileName =""
    try:
        outputFileName = sys.argv[1]
    except Exception as e:   
        outputFileName = "Output.csv"
        print(str(e))
        print("Set default filename for output file as: Output.csv")
    

    outputRequest = requests.get('http://platform1.greenseesaw.com/seesaw_api_test/_design/main/_view/allDocs',auth=('testAPI','testAPI'))

    initialjsonData = outputRequest.json()

    initialjsonData = str(initialjsonData).replace("\'", "\"")
    

    initialjsonData = json.loads(initialjsonData)



    csvData = JsonProcess(initialjsonData, '__')

    
    WriteToCSV(csvData,outputFileName)
    print("Finished Conversion!")



def JsonProcess(jsonDict,delim):
    p ={}
    val = {}
    internalDict=[]
    try:
        for v in jsonDict:

            if isinstance(jsonDict[v], list):
                for item in jsonDict[v]:

                    jsonDict[v] = item

                    if isinstance(jsonDict[v], dict):

                        recursiveDict = JsonProcess(jsonDict[v], delim)
                        for innerV in recursiveDict:

                            try:
                                val[v + delim + innerV].append(recursiveDict[innerV])
                            except KeyError:
                                val[v + delim + innerV] = [recursiveDict[innerV]]
                    else:
                        try:
                            val[v].append(jsonDict[v])
                        except KeyError:
                            val[v] = jsonDict[v]

            if isinstance(jsonDict[v], dict):

                internalDict = JsonProcess(jsonDict[v], delim)
                for innerV in internalDict:
                    try:
                        val[v + delim + innerV].append(internalDict[innerV])
                    except KeyError:
                        val[v + delim + innerV] = internalDict[innerV]




            else:
                try:
                    val[v].append(jsonDict[v])
                except KeyError:
                    val[v] = jsonDict[v]


    except e as Exception:
        print(str(e))
    return val


def WriteToCSV(Data,outputName):
    maxLen=0
    val_Length={}
    headers=[]
    buffer =""
    print(str(headers))

    for item in Data.keys():
        if isinstance(Data[item],list):
            val_Length[item] = len(Data[item])
            maxLen = max(maxLen,val_Length[item])
        elif Data[item] != None:
            val_Length[item] = 1
        elif Data[item] == None:
            val_Length[item] = None
    Output = open(outputName,'a')

    for item in Data.keys():
        headers.append(item)
    headers.sort()
    for head in headers:
        buffer+=head + ','
    buffer=buffer[0:len(buffer)-1] + "\n"
    Output.write(buffer)
    buffer = ""
    for x in range(0, maxLen - 1):
        for item in headers:
            try:
                if isinstance(Data[item], list):
                    buffer = buffer+ str(Data[item][x]) + ','
                else:
                    buffer = buffer + str(Data[item]) + ','
            except IndexError:
                buffer = buffer + ','
        buffer=buffer[0:len(buffer)-1]+"\n"
        Output.write(buffer)
        buffer=""


    

if __name__=="__main__":
    main()

