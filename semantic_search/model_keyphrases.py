from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
import csv
import pickle


def make_embeddings(split_corpus):
    # define the large language model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # increase the max sequence length
    model.max_seq_length = 512

    # input model into keyBERT and define the vectoriser
    kw_model = KeyBERT(model)
    my_vectorizer = KeyphraseCountVectorizer(
        pos_pattern="<J.*>?<N.*>{1,2}"
    )  # look for candidates, 0 or 1 adjectives followed by 1 or 2 nouns

    # extract vocab of potential key words, and embed documents and each word from the vocab
    vocab = my_vectorizer.fit(split_corpus).get_feature_names_out()
    # create dictionaries of document and word embeddings
    doc_embeddings, word_embeddings = kw_model.extract_embeddings(
        split_corpus, vectorizer=my_vectorizer
    )

    with open(r"data/raw/word_embeddings.pkl", "wb") as fOut:
        pickle.dump(
            {k: v for k, v in zip(vocab, word_embeddings)},
            fOut,
            protocol=pickle.HIGHEST_PROTOCOL,
        )

    # doc embeddings
    with open(r"data/raw/split_plan_embeddings.pkl", "wb") as fOut:
        pickle.dump(
            {"docs": split_corpus, "doc_embeddings": doc_embeddings},
            fOut,
            protocol=pickle.HIGHEST_PROTOCOL,
        )

    return doc_embeddings, word_embeddings


def run_keybert_extraction(doc_embeddings, word_embeddings, split_corpus):

    # define the large language model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # increase the max sequence length
    model.max_seq_length = 512

    # input model into keyBERT and define the vectoriser
    kw_model = KeyBERT(model)
    my_vectorizer = KeyphraseCountVectorizer(
        pos_pattern="<J.*>?<N.*>{1,2}"
    )  # look for candidates, 0 or 1 adjectives followed by 1 or 2 nouns

    # define how diverse and how many keyphrases per plan                                                       )
    diversity = 0.6
    top_n = 10

    # extract using keybert model. Output
    keyphrases = kw_model.extract_keywords(
        split_corpus,
        use_maxsum=False,
        use_mmr=True,
        diversity=diversity,
        top_n=top_n,
        vectorizer=my_vectorizer,
        doc_embeddings=doc_embeddings,
        word_embeddings=word_embeddings,
    )
    # save output to local csv
    with open(r"data/raw/keyphrases-and-cosine_sim.csv", "w") as f:
        writer = csv.writer(f)
        for row in keyphrases:
            writer.writerow(row)

    return keyphrases
