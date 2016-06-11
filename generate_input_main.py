import glob
import os
with open('latex/main_input_generated.tex', 'w') as f:
    f.write('%!TEX root = crimson_throne_book_main.tex\n\n')
    print 'Hallo'
    for file in glob.glob('latex/downloaded/*.tex'):
        print file
        path = os.path.normpath(os.path.join(os.getcwd(), file))
        print path
        path_man = path.replace('downloaded', 'manual')
        print path_man
        if os.path.isfile(path_man):
            print 'manual exist'
            in_file = path_man.replace(os.getcwd(), '').replace('\\latex\\', '').replace('\\', '/')
            f.write('\t\\input{{{0}}}\n\n'.format(in_file))
        else:
            print 'use downloaded'
            in_file = path.replace(os.getcwd(), '').replace('\\latex\\', '').replace('\\', '/')
            f.write('\t\\input{{{0}}}\n\n'.format(in_file))
