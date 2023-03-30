from utils import has_repeated_word, contains_digits, contains_misspelled_word, word_a_b_common_word
import pandas as pd
import numpy as np
import torch

def get_unique_vocab():
    #extract our unique keyphrase vocabulary from the keybert output
    df = pd.read_csv('../data/raw/keyphrases-cosine_sim.csv',header=None)
    keywords = df.applymap(lambda x: x.split(',')[0][2:-1] if pd.notna(x) else x) #only take keyphrase, not the cosine similarity to plan
    unique_keyphrases = list(set(keywords.values.ravel().tolist()))
    unique_keyphrases = unique_keyphrases[1:]
    return unique_keyphrases
    
def create_stats_csv(unique_keyphrases, plan_index):
    #read in our keybert output and index rows by plan number
    df = pd.read_csv('../data/raw/keyphrases-cosine_sim.csv',header=None)
    keywords = df.drop(['plan#'],axis=1).applymap(lambda x: x.split(',')[0][2:-1] if pd.notna(x) else x)
    keywords['plan#'] = plan_index
    
    #create column for how many plans the keyphrase is a keyphrase in
    key_stats = pd.DataFrame({'keyphrase': unique})
    key_stats['keyphrase in _ plans'] =  [len(keywords[(keywords == x).any(axis=1)]['plan#'].value_counts()) for x in unique]
    key_stats = key_stats.sort_values(by='keyphrase in _ plans', ascending=False)
    #create some other useful columns for filtering later
    key_stats['has common word'] = key_stats['keyphrase'].apply(has_repeated_word) #flags keyphrases like reducing reduction
    key_stats['contains digits'] = key_stats['keyphrase'].apply(contains_digits)
    key_stats['misspelled'] = [contains_misspelled_word(text) for text in tqdm(key_stats['keyphrase'])]
    
    #filter for useful keyphrases and save csv
    clean_key_stats = key_stats[(key_stats['has common word'] == False) & (key_stats['contains digits']==False)& (key_stats['misspelled']==False)][['keyphrase','keyphrase in _ plans']]
    clean_key_stats.to_csv('../data/final/ml_keyphrases.csv',index=False)
    
    return clean_key_stats    
    

def create_pairwise_csv():
    #get unique keyphrases, this time without repeated words, digits, or mispellings
    df = pd.read_csv('../data/final/ml_keyphrases.csv',index=False)
    clean_unique_keyphrases = list(set(df.keyphrase.values.ravel().tolist()))
    
    #load word embeddings to get dictionary of only our unique keyphrase embeddings
    with open('../data/raw/split_plan_embeddings.pkl', "rb") as fIn:
        stored_vocab = pickle.load(fIn)
        vocab = stored_vocab.keys()
        vocab_embeddings = stored_vocab.values()
    
    keyword_embeddings = {k: stored_vocab[k] for k in clean_unique_keyphrases}
    
    #convert into tensor
    tensor_embeds = []
    for key in keyword_embeddings:
        value = keyword_embeddings[key]
        tensor_value = torch.from_numpy(value)
        tensor_embeds.append(tensor_value)
    
    tensor_embeds = torch.stack(tensor_embeds)
    
    #get cosine similarities
    cos_sim = util.cos_sim(tensor_embeds, tensor_embeds)
    
    #topk
    k = 100
    values, indices = torch.topk(cos_sim, k=k, dim=1, largest=True)
    x = indices.numpy()
    y = values.numpy()
    f = np.vectorize(lambda x : clean_unique_keyphrases[x])
    np_phrases = f(x)
    #create similar phrases and cosine similarity dataframes
    df1 = pd.DataFrame(np_phrases)
    df2 = pd.DataFrame(y)
    
    #convert them into desired format
    df1_melt = df1.melt(id_vars=['0'], value_vars=df1.columns[1:], var_name='nth similar', value_name='word_b')
    df2_melt = df2.melt(id_vars=['0'], value_vars=df2.columns[1:], var_name='nth similar', value_name='cosine_similarity')
    
    df1_melt['cosine similarity'] = df2_melt['cosine_similarity']
    #reorder so word_a shows 100 similar options before next word_a
    n = len(df1)
    new_index = [i + j for i in range(n) for j in range(0, len(df1_melt), n)]
    df_final = df1_melt.iloc[new_index]
    
    df_final = df_final.rename(columns= {'0':'word_a'})
    df_final['share_common_word'] = df_final.apply(word_a_b_common_word, axis=1)
    
    df_final.to_csv('../data/final/ml_keyphrases_pairwise.csv',index=False)
    
    return df_final


    