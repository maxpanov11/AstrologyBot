#Функции, в которой исправляются ошибки с пмощью расстояния Левенштейна
def mistakes_corrector(word):        
    signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
    dist = []
    for sign in signs:
        if abs(len(sign)-len(word)) <= 2:
            leven = [[0] * (len(word)+1) for i in range(len(sign)+1)]
            for i in range(1, (len(word)+1)):
                leven[0][i] = i
            for j in range(1, (len(sign)+1)):
                leven[j][0] = j
            for i in range(1, len(sign)+1):
                for j in range(1, len(word)+1):
                    leven[i][j] = min(leven[i-1][j]+1, leven[i][j-1]+1, leven[i-1][j-1] + (word[j-1]!=sign[i-1]))
            if leven[-1][-1] == 1:
                return sign
            else:
                dist.append([leven[-1][-1], sign])
    if min(dist)[0] <= 2:
        return min(dist)[1]
    else:
        return 0

       
