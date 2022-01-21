file = open('html_vocab.txt', 'r', encoding='utf8')
outfile = open('try_output.py', 'w', encoding='utf8')
en = ''
ru = ''
refactor_dict = []
eng_words = []
for line in file:
    line = line.replace('<tr><td>', ' ')
    line = line.replace('</td><td>', ' ')
    line = line.replace('</td></tr>', ' ')
    a = int(line.split()[0])
    for i in line.split()[1:]:
        if i[0] != '(':
            if i[0] <= 'А':
                en += i + ' '
            else:
                ru += i + ' '
        else:
            if i[1] <= 'А':
                en += i + ' '
            else:
                ru += i + ' '
    refactor_dict.append(a)
    refactor_dict.append(en)
    refactor_dict.append(ru)
    eng_words.append(en)
    en = ''
    ru = ''
    print(refactor_dict, file=outfile, end=', \n \t \t')
    refactor_dict = []
print(eng_words, file=outfile)
'''
for num in range(5, len(eng_words), 5):
    print(eng_words[num - 5:num], file=outfile, end=', \n \t \t')
#print(eng_words[i-5:i] for i in range(5, len(eng_words), 5))
'''
outfile.close()
