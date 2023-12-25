#Перевод даты в знак гороскопа
def date_to_sign(word):
    signs = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы']
    dates = [[20, 10, 11], [20, 11, 12], [20, 12, 1], [20, 1, 2], [20, 2, 3], [21, 3, 4],
             [22, 4, 5], [23, 5, 6], [23, 6, 7], [23, 7, 8], [22, 8, 9], [21, 9, 10]]
    separators = ['.', ',', ':', '/', ';', ' ']
    if len(word) < 3 or len(word) > 5:
        return -1
    elif word[1] not in separators and word[2] not in separators:
        return 0
    elif word[1] in separators and word[0] >= '1' and word[0] <= '9':
        if len(word) == 3:
            if word[2] >= '1' and word[2] <= '9':
                month = int(word[2])
                day = int(word[0])
            else:
                return 1
        elif len(word) == 4:
            if word[2] == '0' and word[3] >= '1' and word[3] <= '9':
                month = int(word[3])
                day = int(word[0])
            elif word[2] == '1' and word[3] >= '0' and word[3] <= '2':
                month = int(word[2:4])
                day = int(word[0])
            else:
                return 1          
        else:
            return -1
    elif word[2] in separators and len(word) >= 4:
        if word[0] == '0' and word[1] >= '1' and word[1] <= '9':
            day = int(word[1])
        elif word[0] >= '1' and word[0] <= '3' and word[1] >= '0' and word[1] <= '9':
            day = int(word[0:2])
            if day > 31:
                return 2    
        else:
            return 2
        if len(word) == 5:
            if word[3] == '0' and word[4] >= '1' and word[4] <= '9':
                month = int(word[4])
            elif word[3] == '1' and word[4] >= '0' and word[4] <= '2':
                month = int(word[3:5])
            else:
                return 1
        else:
            if word[3] >= '1' and word[3] <= '9':
                month = int(word[3])
            else:
                return 1
    else:
        return -1
    sign=signs[(day<=dates[month-1][0])*dates[month-1][1]+(day>dates[month-1][0])*dates[month-1][2]-1]
    return sign 
