


import os
import json
import pandas as pd
import re

from stanza_utils import *

book_corp_path = r'C:\BOOKS_gpt4\Vol1/'
book_text_path = book_corp_path+'book_text/'

files = os.listdir(book_text_path)
paragraphs_path_list = [os.path.join(book_text_path, file) for file in files]

book_code_list = [  file[len('df_paragraphs_'):-len('.tsv')] for file in files]



print(files)
print(paragraphs_path_list)

print(book_code_list)



file_path_for_json = book_corp_path +'file_path_dic.json'
file_path_rev_json = book_corp_path +'file_path_rev_dic.json'
with open(file_path_for_json, 'r') as file:
        file_path_dic = json.load(file)
with open(file_path_rev_json, 'r') as file:
        file_path_dic_rev = json.load(file)

print(f"file_path_dic  . #books: {len(file_path_dic)} {len(file_path_dic_rev)}")




























for f_index, paragraphs_file in enumerate(paragraphs_path_list):
    book_code = re.search(r'_(fp_[\w\d]+|\d+)\.tsv$', paragraphs_file)  .group(1)
    book_name = file_path_dic_rev[book_code]["book_name"]


    book_dic_info = file_path_dic[book_name]
    word_table_date = book_dic_info.get('word_table_date', None)
    if word_table_date is not None:
      continue



    df_paragraphs = pd.read_csv(paragraphs_file, sep='\t')
    print(f'-------\n{f_index:<5} {book_name}   {book_code}={book_code_list[f_index]}   #paragraphs={len(df_paragraphs):<10}  {paragraphs_file}')
    df_book_token_coref_stanza, df_coref_chain = get_stanza_rezults(df_paragraphs)

    df_book_token_coref_stanza.to_csv(book_corp_path+'/tmp/stanza/df_book_token_coref_stanza_'+book_code+'.tsv', sep='\t', index=False)
    df_coref_chain.to_csv(book_corp_path+'/tmp/stanza/df_coref_chain_'+book_code+'.tsv', sep='\t', index=False)

    #break










