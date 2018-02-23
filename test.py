#/usr/local/bin/python3

def son():
    text = input('speak:')
    if text=='exit':
        return
    else:
        print('B{}'.format(text))

son()