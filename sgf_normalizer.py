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

    def head_parser(self):
        sgfh = self.content[self.head_lst[0]:self.head_lst[1]]
        cutidx = 0
        for idc in range(len(sgfh)):
            if sgfh[idc] == ']' and not (sgfh[idc-1] == "\\"):
                sgfh_slice = sgfh[cutidx:idc]
                sgfh_key, sgfh_value = sgfh_slice.split('[')
                self.header[sgfh_key.strip()] = sgfh_value.strip()
                cutidx = idc+1

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
            #/* nowy skatalogowany plik:
            sgf = fred(test_data)
            sgf.head_parser()
            with open(sgf.new_file_name(), 'w+') as fout:
                fout.write(test_data)
                fout.close()
