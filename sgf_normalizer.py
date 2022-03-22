#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import os
import sys

class fred:
    '''wczytywanie pliku'''
    def __init__(self, content):
        self.content = content
        self.idx_lst = list()   #/* indexy węzłów
        self.header = {}
        self.head_lst = list()  #/* indexy nagłówka
        self.body = {}
        self.body_lst = list()  #/* indexy treści

        self._idx_collector()
        self.new_fn = ''
        #/*self.new_path = os.path.join(os.getcwd(),'GOTOWE/')
        self.new_path = os.path.join('GO/SGF', 'OGS')

    def _idx_collector(self):
        '''czyta self.content uzupełnia listy indexów'''
        node = 0 #/* numer węzła
        head = 0
        BW = ['b', 'B', 'w', 'W']
        for idx in range(len(self.content)):
            try:
                if self.content[idx] == ';':
                    if self.content[idx-1] == '(':
                        if head == 0:
                            self.idx_lst.append(idx-1)
                            self.head_lst.append(idx+1)
                            head = len((self.head_lst))
                        else:
                            node += 1
                            self.idx_lst.append(idx-1)
                    elif head == 1:
                        if self.content[idx+1] in BW and self.content[idx+2] == '[':
                            self.head_lst.append(idx)
                            head = len((self.head_lst))
            except:
                pass
        if head:
            self.body_lst.append(self.head_lst[1])
            self.body_lst.append(len(self.content)-1)


    def old_head_parser(self):
        '''buduje słownik nagłówka pliku sgf'''
        #/* błędny jest podział po '\n'!
        #/* pewniejszy jest podział po ']' z pominięciem '\\]'
        sgfh = self.content[self.head_lst[0]:self.head_lst[1]].split('\n')
        for ln in sgfh:
            ln = ln.strip()
            idx = ln.find('[')
            if idx > 0:
            #/* tu znajduje ostatni ']' co jest błędem przy argumentach podanych w jednej linii!
            #/* konieczne podzielenie linii wg występujących znaków ']'
            #/* a następnie połączenie, jeśli przed ']' występowały '\\'
                #self.header[ln[:idx]] = ln[idx+1:ln.rfind(']')]

                #/* Tu ze zmianami:
                self.header[ln[:idx]] = ln[idx+1:ln.find(']')]


    def head_parser(self):
        '''poprawiony parser nagłówka'''
        segments_lst = list()
        sgfh = self.content[self.head_lst[0]:self.head_lst[1]]
        #print sgfh
        #print '+'*10
        cutidx = 0
        dkey = ''
        for idc in range(len(sgfh)):
            if sgfh[idc] == ']' and not (sgfh[idc-1] == "\\"):
                segments_lst.append(sgfh[cutidx:idc])
                cutidx = idc+1

        for itm in range(len(segments_lst)):
            #print segments_lst[itm]
            cutidx = segments_lst[itm].find('[')
            dkey = filter(lambda x: x.isupper(), segments_lst[itm][:cutidx])
            self.header[dkey] = segments_lst[itm][cutidx+1:]
            #print '%s -> %s' % (dkey, self.header[dkey])


    def get_info(self):
        '''drukuje informacje na temat pliku SGF'''
        for itm in self.header.keys():
            print('%s -> %s' % (itm, self.header.get(itm, '-')))


    def new_file_name(self):
        '''buduje ścieżkę i nową nazwę pliku'''
        plansza = '%sx%s' % (self.header['SZ'],self.header['SZ'])
        self.new_path = os.path.join(self.new_path, plansza)
        if os.path.isdir(self.new_path):
            pass
        else:
            os.makedirs(self.new_path, 0o766)

        tmp_fn = self.header.get('PB', 'nodata').strip().replace(' ', '_')
        tmp_fn += '-' + self.header.get('PW', 'nodata').strip().replace(' ', '_')
        tmp_fn += '-' + self.header.get('DT', 'nodata').strip().replace('-', '')
        tmp_path = os.path.join(self.new_path, tmp_fn+'.sgf')
        idx = 1
        while os.path.isfile(tmp_path):
            print('istnieje')
            print('  ->' + tmp_path)
            tmp_path = os.path.join(self.new_path, tmp_fn+'_'+str(idx)+'.sgf')
            idx += 1
        return tmp_path

if __name__ == '__main__':
    if len(sys.argv)>1:
        for i in range(1,len(sys.argv)):
            #print sys.argv[i]
            # sprawdź czy istnieje sys.args[i]
            with open(sys.argv[i], 'r') as fp:
                print(sys.argv[i])
                test_data = fp.read()
                fp.close()
            #/* nowy sktalogowany plik:
            sgf = fred(test_data)
            sgf.head_parser()
            with open(sgf.new_file_name(), 'w+') as fout:
                fout.write(test_data)
                fout.close()
