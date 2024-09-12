import os
currentPath = os.getcwd()

MANGA_DIR = os.path.join(currentPath, 'manga')

#################### RUN THIS FILE TO CHECK IF YOUR MANGA IDS ARE CORRECTLY MANAGED ####################

def getAllIds():
    allDirs = os.listdir(MANGA_DIR)
    allIds = []
    for dir in allDirs:
        print(dir, end=' ')
        idFile = os.path.join(MANGA_DIR, dir, 'id.txt')
        with open(idFile, 'r') as fid:
            mangaId = fid.read()
            allIds.append(int(mangaId))
            print("id:", mangaId)
            fid.close()
    print(allIds)
    return allIds


allid = getAllIds()

allid.sort()
highestValue = allid[len(allid)-1]

for num in range(len(allid)):
    if num <= 0:
        continue
    if allid[num]!= num + 1:
        print(f"There are a total of {len(allid)} manga, although the highest value is {highestValue}")
        print(allid)
        input(f"Missing manga with ID: {num+1}")
        quit()


        
    

input("No Invalid ID's found")