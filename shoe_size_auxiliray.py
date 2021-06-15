##shoe size charts:
#the tables are written from the nike shoe conversion site,
#make changes here if there are problems with size conversions
kids_us = [2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,1,1.5]
kids_eu = [17,19,18.5,19,19.5,20,21,21.5,22,22.5,23,24,24,25.5,26,26.5,27,27.5,28,28.5,29.5,30,31,31.5,32,33]
kids_uk = [1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,1]

men_us = [3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
men_uk = [3,3.5,4,4.5,5,5.5,6,6,6.5,7,7.5,8,8.5,0,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15]
men_eu = [35.5,36,36.5,37.5,38,38.5,39,40,40.5,41,42,42.5,43,44,44.5,45,45.5,46,47,47.5,48,48.5,49,49.5,50,50.5]

women_us = [4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5]
women_uk = [1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,0,9.5,10]
women_eu = [34.5,35,35.5,36,36.5,37.5,38,38.5,39,40,40.5,41,42,42.5,43,44,44.5,45]

def size_auxilliray(size):
    '''gets the size as string and returns the number'''
    number = 0
    for i in size:
        if i.isdigit():
            number = number * 10 + int(i)
        elif i == '.':
            number = number + 0.5
            return number
    return number



def calculate_size(size,type):
    if type == 'Kids':
        number = size_auxilliray(size)
        if 'EU' in size:
            try:
                index = kids_eu.index(number)
                us_size = 'US ' + str(kids_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        if 'UK' in size:
            try:
                index = kids_uk.index(number)
                us_size = 'US ' + str(kids_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        else:
            return size
    elif type == 'Mens':
        number = size_auxilliray(size)
        if 'EU' in size:
            try:
                index = men_eu.index(number)
                us_size = 'US ' + str(men_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        if 'UK' in size:
            try:
                index = men_uk.index(number)
                us_size = 'US ' + str(men_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        else:
            return size
    elif type == 'Womens':
        number = size_auxilliray(size)
        if 'EU' in size:
            try:
                index = women_eu.index(number)
                us_size = 'US ' + str(women_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        if 'UK' in size:
            try:
                index = women_uk.index(number)
                us_size = 'US ' + str(women_us[index])
                return us_size
            except ValueError as ve:
                print('Size not in charts!')
                return None
        else:
            return size
    else:
        print('INVALID SHOE SIZE!')