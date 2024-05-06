import requests
import json
import os

my_list = []
pwd = os.getcwd()
with open(pwd + '\\dev_urls.txt') as f:
    print("start")
    lines = f.readlines() # list containing lines of file
    columns = [] # To store column names

    i = 1
    for line in lines:
        print(f'read line: {i}')
        line = line.strip() # remove leading/trailing white spaces
        # print(line)
        if line:
            if i == 1:
                i = i + 1
            elif i == 2:
                columns = [item.strip() for item in line.split()]
                print(columns)
                i = i + 1
            # elif i > 1000:
            #     break
            else:
                d = {} # dictionary to store file data (each line)
                data = [item.strip() for item in line.split()]
                for index, elem in enumerate(data):
                    # print(data[index])
                    d[columns[index]] = data[index]

                my_list.append(d) # append dictionary to list
                i = i + 1

# pretty printing list of dictionaries
# print(json.dumps(my_list, indent=4))

i = 1
for entry in my_list:
    if entry:
        if int(entry['imagenum']) > 3:
            continue
        if i > 150:
            break
        i = i + 1
        try:
            response = requests.get(entry['url'], stream=True)

            if not response.ok:
                print(response)
                continue

            with open(pwd + f"\\invalid\\{entry['first']}{entry['last']}{entry['imagenum']}.jpg", 'wb') as handle:
                for block in response.iter_content(1024):
                    if not block:
                        continue
                    handle.write(block)
        except:
            print("fail")

