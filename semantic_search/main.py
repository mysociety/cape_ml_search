from process_plans import create_corpus, split_text, create_split_corpus
from model_keyphrases import make_embeddings, run_keybert_extraction
from process_keyphrases import get_unique_vocab, create_stats_csv, create_pairwise_csv


def full_flow():
    corpus = create_corpus()
    split_corpus, plan_index = create_split_corpus(corpus)
    doc_embeddings, word_embeddings = make_embeddings
    keyphrases = run_keybert_extraction(split_corpus)
    unique_keyphrases = get_unique_vocab()
    clean_key_stats = create_stats_csv(unique_keyphrases, plan_index)
    df_final = create_pairwise_csv()


if name == "__main__":
    full_flow()
    