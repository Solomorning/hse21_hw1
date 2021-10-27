def ArrayRoller(f):
    Array = []
    summ, max, k = 0, 0, -1
    min = 10000000
    for i in f:
        if i[0] == '>':
            y = i.find('len')
            x = int(i[(y + 3):y+i[y:].find('_')])
            summ += x
            Array.append(x)
            if (x<min):
                min = x
            if (x>max):
                max = x
                z = i
    print('Total=',summ,'\nLongest=',max,'\nShortest=',min, z)
    i = 0
    c50 = n50 = Array[0]
    while c50 < summ/2:
        i += 1
        n50 = Array[i]
        c50 += Array[i]
    print('N50=',n50)
    return Array

def GapFinder(x, file, name):
    x.sort(reverse = True)
    gaps = 0
    n = 0
    q = False
    file.close()
    file = open(getcwd() + '\\venv\Outputs\Poil_scaffold.fa', 'r')
    for i in file:
        if q:
            while 'N' in i:
                if i[0] != 'N':
                    gaps += 1
                i = i[i.find('N'):]
                j = 'N'
                while j == 'N':
                    n += 1
                    i = i[1:]
                    j = i[0]
            if '>' in i:
                q = False
        if str(x[0]) in i:
            q = True

    print('Gaps=',gaps,'n=',n)


from os import getcwd
file = open(getcwd() + '\\venv\Outputs\Poil_contig.fa', 'r')
ArrayRoller(file)
file.close()
file = open(getcwd() + '\\venv\Outputs\Poil_scaffold.fa', 'r')
GapFinder(ArrayRoller(file), file, getcwd() + '\\venv\Outputs\Poil_scaffold.fa')
file.close()