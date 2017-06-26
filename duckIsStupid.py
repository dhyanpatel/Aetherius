for x in range(11):
    print('')
    for y in range(11):
        if len(str(x*y)) == 1:
            print('  {}'.format(x * y), end = ' ')
        elif len(str(x*y))== 2:
            print(' {}'.format(x * y), end = ' ')
        elif len(str(x*y)) == 3:
            print(x*y, end = ' ')