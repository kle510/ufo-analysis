def writetoF(content, i):
    name = "data/ufo_data_"+str(i)+".json"
    outF = open(name, 'w')
    outF.write(content)
    outF.close()


if __name__ == "__main__":
    filename = "ufo_awesome_with_airport_shooting_hospital_twitter.json"
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            i = i + 1
            writetoF(line, i)
            if i == 200:
                break
