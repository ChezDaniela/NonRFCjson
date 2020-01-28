import os.path
import csv, json, sys
import shutil
import errno
import time
import xlwt
from os.path import join
 

def JSONDictionary(dictionary_object,index,new_header,headers,values,new_headers,new_values):
    k=0
    temp_list_headers = []
    temp_list_values = []
    while k < len(dictionary_object):
        if isinstance(list(dictionary_object.values())[k],dict):
            new_header_level = str(new_header) + '_' + str(list(dictionary_object.keys())[k])
            JSONDictionary(list(dictionary_object.values())[k],k,new_header_level,headers,values,new_headers,new_values)
        elif isinstance(list(dictionary_object.values())[k],list):
            new_header_level = str(new_header) + '_' + str(list(dictionary_object.keys())[k])
            JSONList(list(dictionary_object.values())[k],k,new_header_level,headers,values,new_headers,new_values)
        else:
            header_object = str(new_header) + '_' + str(list(dictionary_object.keys())[k])
            temp_list_headers.append(header_object)
            temp_list_values.append(list(dictionary_object.values())[k])
        k = k + 1
    if len(temp_list_headers) > 0:
        new_headers.extend(temp_list_headers)
        new_values.extend(temp_list_values)
    return new_headers
    return new_values

  

def JSONList(list_object,index,new_header,headers,values,new_headers,new_values):
    k=0
    temp_list_headers = []
    temp_list_values = []
    while k < len(list_object):
        if isinstance(list_object[k],dict):
            new_header = str(new_header)
            JSONDictionary(list_object[k],k,new_header,headers,values,new_headers,new_values)
        elif isinstance(list_object[k],list):
            new_header = str(new_header)
            JSONList(list_object[k],k,new_header,headers,values,new_headers,new_values)
        else:
            header_object = str(new_header) 
            temp_list_headers.append(header_object)
            temp_list_values.append(list_object[k].values())
        k = k + 1
    if len(temp_list_headers) > 0:
        new_headers.extend(temp_list_headers)
        new_values.extend(temp_list_values)
    return new_headers
    return new_values


def Parse_csv(fileInput,csvOutput,csv_fileException):
    #check if you pass the input file and output file
    if fileInput is not None and csvOutput is not None:
        try:
            inputFile = open(fileInput)
            try:
                data = json.load(inputFile)
            except ValueError:
                print('Decoding JSON has failed')
                return
                # sys.exit(1)
            inputFile.close()
        except IOError:
            print ("Error reading file:", fileInput)
    
    
    headers = list(data.keys())
    values = list(data.values())
    new_headers = []
    new_values = []
    v = 0
    while v < len(data.values()):
        if isinstance((values[v]),dict):
            new_header = str(headers[v])
            JSONDictionary(values[v],v,new_header,headers,values,new_headers,new_values)
        elif isinstance((values[v]),list):
            new_header = str(headers[v])
            JSONList(values[v],v,new_header,headers,values,new_headers,new_values)
        else:
            new_headers.append(headers[v])
            new_values.append(values[v])
        v = v + 1
     
    if os.path.isfile(csvOutput):
        with open(csvOutput, newline='') as f:
            reader = csv.reader(f)
            if next(reader) == new_headers:
                csvFile = open(csvOutput, 'a', newline='')
                output = csv.writer(csvFile)
                output.writerow(new_values)
                csvFile.close()
            else:
                if os.path.isfile(csv_fileException):          
                    csv_exceptionFile = open(csv_fileException, 'a', newline='')
                    output = csv.writer(csv_exceptionFile)
                    output.writerow(new_headers)
                    output.writerow(new_values)
                    csv_exceptionFile.close()
                else:         
                    csv_exceptionFile = open(csv_fileException, 'w', newline='')
                    output = csv.writer(csv_exceptionFile)
                    output.writerow(new_headers)
                    output.writerow(new_values)
                    csv_exceptionFile.close()            
    else:
        csvFile = open(csvOutput, 'w', newline='')
        output = csv.writer(csvFile)
        output.writerow(new_headers)
        output.writerow(new_values)
        csvFile.close()





def main():

    choice ='0'
    while (choice == '0'):
        print("MENU")
        print("Usage: python JSON_tool_v7.py")
        print("1: process all JSON files in the current directory and move them to subdir <Parsed>")
        print("2: exit")
        choice = input ("Please make a choice: ")

        if choice == "2":
            print("Exiting: ...")
            break
        elif choice == "1":
            try:
                destination_dir = "Processed"
                if os.path.isdir(destination_dir):
                    pass
                else:
                    try:
                        os.makedirs(destination_dir)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                        pass

                
                duplicates_dir = "Already_processed"
                if os.path.isdir(duplicates_dir):
                    pass
                else:
                    try:
                        os.makedirs(duplicates_dir)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                        pass
            
                for (dirname, subdirs, files) in os.walk('./'):
                    for filename in files:
                        if filename.endswith('.json'):
                            processedPath=str(destination_dir)+'/'+filename
                            duplicatesPath=str(duplicates_dir)+'/'+filename
                            if os.path.exists(duplicatesPath):
                                os.remove(filename) 
                                break
                            if os.path.exists(processedPath):
                                shutil.move(filename,duplicates_dir) 
                                break
                            cwd = os.getcwd()
                            # print(cwd)
                            milli_sec = int(round(time.time() * 1000))
                            milli_sec = str(milli_sec)[0:7]
                            print(milli_sec)
                            csvOutput = 'Data' + str(milli_sec) + '.csv'
                            csv_fileException = 'Exception.csv'
                            Parse_csv(filename,csvOutput,csv_fileException)
                            shutil.move(filename,destination_dir)
                            time.sleep(3)
                    break
            except FileNotFoundError:
                print("Error file and/or path.")
            break
        else:
            choice = '0'


if __name__ == '__main__':
    main()