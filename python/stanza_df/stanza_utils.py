

import os
import json
import pandas as pd
import re



import stanza
#import peft
#import transformers

'''
stanza.download('en')
nlp = stanza.Pipeline('en') # initialize English neural pipeline
doc = nlp("Barack Obama was born in Hawaii.") # run annotation over a sentence
print(doc)
'''

#pipe = stanza.Pipeline("en", processors="tokenize,coref")

#A = pipe("John Bauer works at Stanford.  He has been there 4 years")
#print(A)



pipe = stanza.Pipeline("en", processors="tokenize,pos,constituency,lemma,depparse,ner,coref")  # the constituency parser does not return words and token objects, only labels.



def get_list_of_NP_indices(sentence):
  sent_word_list = [ word.text  for word in sentence.words]
  zeros_list = [0] * len(sentence.words)  # Each NP node in the tree has a unique number. Embedded nodes can be identified by looking at the sequence of numbers. For example: 2,2,1,1,1,3,1 means that node 1 includes both 2 and 3 because its number is lower than the previous nodes. 0 means that the word does not belong to any NP node
  zeros_list2= [0] * len(sentence.words)
  zeros_list_VP= [0] * len(sentence.words)
  zeros_list_PP= [0] * len(sentence.words)
  zeros_list_ADJP= [0] * len(sentence.words)
  zeros_list_ADVP= [0] * len(sentence.words)

  NP_node_nr = 0
  word_nr = -1

  def traverse_tree(node, list_of_NP_phrases, list_of_NP_phrases2,list_of_VP_phrases,list_of_PP_phrases,list_of_ADJP_phrases,list_of_ADVP_phrases):
      nonlocal NP_node_nr, word_nr
      #word = None
      if node.is_leaf():
          #word = node.label
          word_nr += 1
      if node.label=='NP':
        NP_node_nr += 1
        word_list_NP = [ d  for d in  node.leaf_labels()]
        word_nr_1 = word_nr + 1
        word_nr_2 = word_nr + len(word_list_NP)
        #print(f'{NP_node_nr} {node.label} {word_nr_1}-{word_nr_2}       {word_list_NP}       node.depth()={node.depth()}')  # {" ".join(d  for d in  node.leaf_labels())}
        if node.depth() in [2,3]:
          list_of_NP_phrases.append((word_list_NP,word_nr_1,word_nr_2,NP_node_nr))
        if node.depth()>3:
          list_of_NP_phrases2.append((word_list_NP,word_nr_1,word_nr_2,NP_node_nr))

      if node.label=='VP':
        NP_node_nr += 1
        word_list_NP = [ d  for d in  node.leaf_labels()]
        word_nr_1 = word_nr + 1
        word_nr_2 = word_nr + len(word_list_NP)
        #print(f'{NP_node_nr} {node.label} {word_nr_1}-{word_nr_2}       {word_list_NP}       node.depth()={node.depth()}')  # {" ".join(d  for d in  node.leaf_labels())}
        list_of_VP_phrases.append((word_list_NP,word_nr_1,word_nr_2,NP_node_nr))

      if node.label=='PP':
        NP_node_nr += 1
        word_list_NP = [ d  for d in  node.leaf_labels()]
        word_nr_1 = word_nr + 1
        word_nr_2 = word_nr + len(word_list_NP)
        #print(f'{NP_node_nr} {node.label} {word_nr_1}-{word_nr_2}       {word_list_NP}       node.depth()={node.depth()}')  # {" ".join(d  for d in  node.leaf_labels())}
        list_of_PP_phrases.append((word_list_NP,word_nr_1,word_nr_2,NP_node_nr))

      if node.label=='ADJP' and len(node.leaf_labels())>1: #      node.label not in ['NP','VP','PP'] node.depth()>1    SBAR
        NP_node_nr += 1
        word_list_NP = [ d  for d in  node.leaf_labels()]
        word_nr_1 = word_nr + 1
        word_nr_2 = word_nr + len(word_list_NP)
        #print(f'{NP_node_nr} {node.label} {word_nr_1}-{word_nr_2}       {word_list_NP}       node.depth()={node.depth()}')  # {" ".join(d  for d in  node.leaf_labels())}
        list_of_ADJP_phrases.append((word_list_NP,word_nr_1,word_nr_2,NP_node_nr))

      if node.label=='ADVP' and len(node.leaf_labels())>1: #      node.label not in ['NP','VP','PP'] node.depth()>1    SBAR
        NP_node_nr += 1
        word_list_NP = [ d  for d in  node.leaf_labels()]
        word_nr_1 = word_nr + 1
        word_nr_2 = word_nr + len(word_list_NP)
        #print(f'{NP_node_nr} {node.label} {word_nr_1}-{word_nr_2}       {word_list_NP}       node.depth()={node.depth()}')  # {" ".join(d  for d in  node.leaf_labels())}
        list_of_ADVP_phrases.append((word_list_NP,word_nr_1,word_nr_2,NP_node_nr))


      for child in node.children:
          traverse_tree(child,list_of_NP_phrases, list_of_NP_phrases2,list_of_VP_phrases,list_of_PP_phrases,list_of_ADJP_phrases,list_of_ADVP_phrases)

      return list_of_NP_phrases, list_of_NP_phrases2,list_of_VP_phrases,list_of_PP_phrases,list_of_ADJP_phrases,list_of_ADVP_phrases


  def find_match_indices(sent_word_list, word_list_NP):
      indices = []
      for i in range(len(sent_word_list) - len(word_list_NP) + 1):
          if sent_word_list[i:i+len(word_list_NP)] == word_list_NP:
              indices.append((i, i+len(word_list_NP)-1))
      return indices



  list_of_NP_phrases, list_of_NP_phrases2,list_of_VP_phrases,list_of_PP_phrases,list_of_ADJP_phrases,list_of_ADVP_phrases = traverse_tree(sentence.constituency,[],[],[],[],[],[])
  #print(list_of_NP_phrases)


  for phrase_NP_tup in list_of_NP_phrases:
    #phrase_NP = phrase_NP_tup[0]
    word_nr_1 = phrase_NP_tup[1]
    word_nr_2 = phrase_NP_tup[2]
    NP_node_nr = phrase_NP_tup[3]
    for i in range(word_nr_1, word_nr_2+1 ):
      zeros_list[i] = NP_node_nr
    #print(f'                                       ----  {word_nr_1}  {word_nr_2} {NP_node_nr} {phrase_NP}')

  for phrase_NP_tup in list_of_NP_phrases2:
    #phrase_NP = phrase_NP_tup[0]
    word_nr_1 = phrase_NP_tup[1]
    word_nr_2 = phrase_NP_tup[2]
    NP_node_nr = phrase_NP_tup[3]
    for i in range(word_nr_1, word_nr_2+1 ):
      zeros_list2[i] = NP_node_nr

  for phrase_tup in list_of_VP_phrases:
    word_nr_1 = phrase_tup[1]
    word_nr_2 = phrase_tup[2]
    node_nr = phrase_tup[3]
    for i in range(word_nr_1, word_nr_2+1 ):
      zeros_list_VP[i] = node_nr

  for phrase_tup in list_of_PP_phrases:
    word_nr_1 = phrase_tup[1]
    word_nr_2 = phrase_tup[2]
    node_nr = phrase_tup[3]
    for i in range(word_nr_1, word_nr_2+1 ):
      zeros_list_PP[i] = node_nr

  for phrase_tup in list_of_ADJP_phrases:
    word_nr_1 = phrase_tup[1]
    word_nr_2 = phrase_tup[2]
    node_nr = phrase_tup[3]
    for i in range(word_nr_1, word_nr_2+1 ):
      zeros_list_ADJP[i] = node_nr

  for phrase_tup in list_of_ADVP_phrases:
    word_nr_1 = phrase_tup[1]
    word_nr_2 = phrase_tup[2]
    node_nr = phrase_tup[3]
    for i in range(word_nr_1, word_nr_2+1 ):
      zeros_list_ADVP[i] = node_nr



  return zeros_list, zeros_list2 ,zeros_list_VP, zeros_list_PP,zeros_list_ADJP,zeros_list_ADVP




def get_coref_for_chapter(coref_chunk_id, chapter, concatenated_text, paragraph_id):

  doc = pipe(concatenated_text)

  coref_chunk_id_list2 = []
  coref_chain_index_list = []
  coref_mention_sentence_list = []
  coref_mention_start_word_list = []
  coref_mention_end_word_list = []
  coref_mention_phrase_list = []


  for coref_chain in doc.coref:
    if len(coref_chain.mentions) == 1:
      continue
    #print(f"{coref_chain.index:<5} {len(coref_chain.mentions):>5}  {coref_chain.representative_index:>5}   {coref_chain.representative_text}")
    for coref_mention in coref_chain.mentions:
      #print(f"      {coref_mention.sentence:<5}   {coref_mention.start_word:>5}   {coref_mention.end_word}")
      coref_chunk_id_list2.append(coref_chunk_id)
      coref_chain_index_list.append(coref_chain.index)
      coref_mention_sentence_list.append(coref_mention.sentence)
      coref_mention_start_word_list.append(coref_mention.start_word+1)
      coref_mention_end_word_list.append(coref_mention.end_word)


      phrase_tmp = " ".join(d.text for d in  doc.sentences[coref_mention.sentence].words[coref_mention.start_word:coref_mention.end_word])
      coref_mention_phrase_list.append(phrase_tmp)



  paragraph_id_tmp = paragraph_id




  coref_chunk_id_list = []

  chapter_id_list = []
  paragraph_id_list = []
  sent_id_list = []
  word_id_list = []

  coref1_phrase_id_list = []

  token_text_list = []

  lemma_list = []
  upos_list = []
  xpos_list = []
  feats_list = []
  head_id_list = []
  head_word_list = []
  deprel_list = []
  ner_list = []
  is_quote_list = []

  coref_id_list_1 = []
  coref_id_list_2 = []
  coref_id_list_3 = []
  coref_id_list_4 = []

  coref1_is_start_list = []
  coref2_is_start_list = []
  coref3_is_start_list = []
  coref4_is_start_list = []

  coref1_is_end_list = []
  coref2_is_end_list = []
  coref3_is_end_list = []
  coref4_is_end_list = []

  NP_indices = []
  NP_indices2= []

  VP_indices = []
  PP_indices = []
  ADJP_indices = []
  ADVP_indices = []

  coref1_phrase_id = -1
  word_id_inbook = 0
  is_quote = 0

  for i, sent in enumerate(doc.sentences):
      #print(f"Sentence {i+1}")
      #if i !=1:
      #  continue


      NP_indices_tmp, NP_indices_tmp2  ,zeros_list_VP,zeros_list_PP,zeros_list_ADJP,zeros_list_ADVP     = get_list_of_NP_indices(sent)


      for word_id, word in enumerate(sent.words):  # sent.words token has words  sent.tokens

          NP_indice = NP_indices_tmp[word_id]
          NP_indice2= NP_indices_tmp2[word_id]

          if word.xpos[0] == 'N' and NP_indice == 0:
            NP_indice = word_id+1000 # to indicate that there is somthing wrong + 1000

          NP_indices.append(NP_indice)
          NP_indices2.append(NP_indice2)

          VP_indices.append(zeros_list_VP[word_id])
          PP_indices.append(zeros_list_PP[word_id])
          ADJP_indices.append(zeros_list_ADJP[word_id])
          ADVP_indices.append(zeros_list_ADVP[word_id])


          #word_id_inbook += 1

          #for coref_chain in word.coref_chains:
          #  print(f"  {word.text} ")
          #  print(f"      {coref_chain.chain.index}   {coref_chain.chain.representative_text}")

          coref_id_1 = -1
          coref_id_2 = -1
          coref_id_3 = -1
          coref_id_4 = -1


          coref1_is_start = False
          coref2_is_start = False
          coref3_is_start = False
          coref4_is_start = False

          coref1_is_end = False
          coref2_is_end = False
          coref3_is_end = False
          coref4_is_end = False

          if len(word.coref_chains)>0:
            coref_id_1 = word.coref_chains[0].chain.index
            coref1_is_start = word.coref_chains[0].is_start
            coref1_is_end = word.coref_chains[0].is_end
            if coref1_is_start or coref1_phrase_id == -1:
              coref1_phrase_id = word.id  #  word_id_inbook

          if len(word.coref_chains)>1:
            coref_id_2 = word.coref_chains[1].chain.index
            coref2_is_start = word.coref_chains[1].is_start
            coref2_is_end = word.coref_chains[1].is_end
          if len(word.coref_chains)>2:
            coref_id_3 = word.coref_chains[2].chain.index
            coref3_is_start = word.coref_chains[2].is_start
            coref3_is_end = word.coref_chains[2].is_end
          if len(word.coref_chains)>3:
            coref_id_4 = word.coref_chains[3].chain.index
            coref4_is_start = word.coref_chains[3].is_start
            coref4_is_end = word.coref_chains[3].is_end


          coref_chunk_id_list.append(coref_chunk_id)
          chapter_id_list.append(chapter)
          paragraph_id_list.append(paragraph_id_tmp)
          sent_id_list.append(i)
          word_id_list.append(word.id)  # word_id

          coref1_phrase_id_list.append(coref1_phrase_id)

          token_text_list.append(word.text)


          lemma_list.append(word.lemma)
          upos_list.append(word.upos)
          xpos_list.append(word.xpos)
          feats_list.append(word.feats)
          head_id_list.append(word.head)
          head_word_list.append( sent.words[word.head-1].text if word.head > 0 else "root" )
          deprel_list.append(word.deprel)

          if word.text=='“':
            is_quote = 1
          elif word.text=='”':
            is_quote = 0
          is_quote_list.append(is_quote)

          ner_str = word.parent.ner.split('-')[1] if '-' in word.parent.ner else ''
          ner_str = ner_str if ner_str != 'O' else ''
          #ner_list.append(word.parent.ner if word.parent.ner!='O' else '')
          ner_list.append(ner_str)


          misc = word.parent.to_dict()[0].get('misc')
          if misc is not None:
            #bb =  misc.endswith(r'\n\n')
            #print(f"{word.text:<20} {misc}  {misc.startswith('SpacesAfter=') }  {bb} ")
            if  misc.endswith(r"\n\n"):
              paragraph_id_tmp +=  + 1




          coref_id_list_1.append(coref_id_1)
          coref_id_list_2.append(coref_id_2)
          coref_id_list_3.append(coref_id_3)
          coref_id_list_4.append(coref_id_4)

          coref1_is_start_list.append(coref1_is_start)
          coref2_is_start_list.append(coref2_is_start)
          coref3_is_start_list.append(coref3_is_start)
          coref4_is_start_list.append(coref4_is_start)

          coref1_is_end_list.append(coref1_is_end)
          coref2_is_end_list.append(coref2_is_end)
          coref3_is_end_list.append(coref3_is_end)
          coref4_is_end_list.append(coref4_is_end)

          if coref1_is_end:
            coref1_phrase_id = -1

  #df_book_token_coref_stanza_tmp = pd.DataFrame({'coref_chunk_id': coref_chunk_id_list, 'coref1_phrase_id': coref1_phrase_id_list , 'chapter': chapter_id_list, 'paragraph_id': paragraph_id_list, 'sent_id': sent_id_list, 'word_id': word_id_list, 'token': token_text_list,          'lemma': lemma_list ,'pos': upos_list  ,'xpos': xpos_list,'head_id': head_id_list,'head_word': head_word_list,'deprel': deprel_list   , 'ner': ner_list,                      'coref_id_1': coref_id_list_1 , 'coref_id_2': coref_id_list_2, 'coref_id_3': coref_id_list_3, 'coref_id_4': coref_id_list_4 , 'coref1_is_start' : coref1_is_start_list ,  'coref1_is_end' : coref1_is_end_list , 'coref2_is_start' : coref2_is_start_list ,  'coref2_is_end' : coref2_is_end_list,  'coref3_is_start' : coref3_is_start_list ,  'coref3_is_end' : coref3_is_end_list , 'coref4_is_start' : coref4_is_start_list ,  'coref4_is_end' : coref4_is_end_list }  )
  df_book_token_coref_stanza_tmp = pd.DataFrame({'chapter': chapter_id_list, 'coref_chunk_id': coref_chunk_id_list,                                              'paragraph_id': paragraph_id_list, 'sent_id': sent_id_list, 'word_id': word_id_list, 'token': token_text_list,          'lemma': lemma_list ,'pos': upos_list  ,'xpos': xpos_list,'head_id': head_id_list,'head_word': head_word_list,'deprel': deprel_list   , 'ner': ner_list ,'is_NP': NP_indices , 'is_NP2': NP_indices2  , 'is_VP': VP_indices  , 'is_PP': PP_indices , 'is_ADJP': ADJP_indices , 'is_ADVP': ADVP_indices                 ,              'is_quote': is_quote_list                   }  )
  df_book_token_coref_stanza_tmp.loc[df_book_token_coref_stanza_tmp['token'] == '”', 'is_quote'] = 1

  df_coref_chain_tmp = pd.DataFrame({'coref_chunk_id': coref_chunk_id_list2, 'coref_chain_index': coref_chain_index_list , 'sentence_id': coref_mention_sentence_list, 'start_word_id': coref_mention_start_word_list, 'end_word_id': coref_mention_end_word_list  , 'phrase': coref_mention_phrase_list          }  )



  return df_book_token_coref_stanza_tmp , df_coref_chain_tmp




def get_stanza_rezults(df_paragraphs):

    df_book_token_coref_stanza = None
    df_coref_chain = None

    concatenated_text = ''
    coref_chunk_id = 0

    df_book_token_coref_stanza = None
    df_coref_chain = None
    paragraph_id_tmp = -1
    for index, row in df_paragraphs.iterrows():
        chapter = row['chapter']
        paragraph = row['paragraph']

        if paragraph_id_tmp == -1:
          paragraph_id_tmp = index

        next_row_chapter = df_paragraphs.loc[index + 1, 'chapter'] if index < len(df_paragraphs) - 1 else None

        concatenated_text += paragraph + '\n\n'

        if len(concatenated_text.split())>1000 or next_row_chapter == None or next_row_chapter != chapter:
          print(f'\r    parag_index:{paragraph_id_tmp:>5}-{index:<5}   coref_chunk_id: {coref_chunk_id:<5}   chapter: {chapter:<5}    text_len: {len(concatenated_text):<5}  {concatenated_text[:20]}', end='')

          df_book_token_coref_stanza_tmp, df_coref_chain_tmp = get_coref_for_chapter(coref_chunk_id, chapter, concatenated_text, paragraph_id_tmp)
          concatenated_text = ''
          paragraph_id_tmp = -1
          coref_chunk_id += 1

          if df_book_token_coref_stanza is None:
            df_book_token_coref_stanza = df_book_token_coref_stanza_tmp
          else:
            df_book_token_coref_stanza = pd.concat([df_book_token_coref_stanza, df_book_token_coref_stanza_tmp], ignore_index=True)

          if df_coref_chain is None:
            df_coref_chain = df_coref_chain_tmp
          else:
            df_coref_chain = pd.concat([df_coref_chain, df_coref_chain_tmp], ignore_index=True)


          #if index>3:
          #  break

    return df_book_token_coref_stanza, df_coref_chain





def corect_stanza_lemma(df_book_token_coref_stanza):

    lemma_corec_dic = {
        'leaned-VERB':'lean'
    }

    for index, row in df_book_token_coref_stanza.iterrows():
        token = row['token']
        lemma	 = row['lemma']
        pos = row['pos']

        lemma2 = lemma_corec_dic.get(token+'-'+pos)
        if lemma2 is None:
          continue

        df_book_token_coref_stanza.loc[index, 'lemma'] = lemma2
        print(f"{token:<15}   {lemma:<15}    {lemma2:<15}")

        return df_book_token_coref_stanza
















'''
doc = pipe("Mr. Sherlock Holmes, who was usually very late in the mornings, save upon those not infrequent occasions when he was up all night, was seated at the breakfast table.")
sentence = doc.sentences[0]
NP_indices_tmp, list_of_NP_phrases2,zeros_list_VP,zeros_list_PP,zeros_list_ADJP,zeros_list_ADVP  = get_list_of_NP_indices(sentence)
print(NP_indices_tmp, list_of_NP_phrases2,zeros_list_VP,zeros_list_PP,zeros_list_ADJP,zeros_list_ADVP )
'''
