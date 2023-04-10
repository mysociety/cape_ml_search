import pandas as pd
from utils import clean3, is_pua, remove_punct_nums


# load in plans and clean to make our corpus


def create_corpus(path="data/raw/plans.xlsx"):
    df = pd.read_excel(path)
    drop_cols = [
        "search_link",
        "type",
        "charset",
        "unfound",
        "credit",
        "date_retrieved",
        "time_period",
        "scope",
        "status",
        "well_presented",
        "baseline_analysis",
        "notes",
        "plan_path",
        "file_type",
        "website_url",
        "authority_code",
        "authority_type",
        "wdtk_id",
        "mapit_area_code",
        "country",
        "gss_code",
        "county",
        "region",
        "population",
        "unfound",
        "credit",
        "homepage_mention",
        "dedicated_page",
        "plan_due",
        "title",
        "title_checked",
        "twitter_url",
        "twitter_name",
        "url",
    ]
    df = df.drop(drop_cols, axis=1)
    df = df[df["text"].notna()]
    df["text"] = df["text"].apply(clean3)
    df = df.drop([125, 494], inplace=False) #this removes plan's whose text is there but is just a sti
    corpus = df["text"].to_list()
    return corpus


def split_text(text: str, max_tokens: int = 512):
    sentences = text.split(".")
    chunks = []
    current_chunk = ""
    current_token_count = 0
    for sentence in sentences:
        tokens = sentence.split()
        if current_token_count + len(tokens) <= max_tokens:
            current_chunk += sentence + "."
            current_token_count += len(tokens)
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + "."
            current_token_count = len(tokens)
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def create_split_corpus(corpus):
    # returns a list of 512 token chunks and and index of what plan it originally came from
    split_dict = {}
    for i, v in enumerate(corpus):
        split_dict[i] = split_text(v)
    x = [[key] * len(split_dict[key]) for key in split_dict.keys()]
    plan_index = [item for sublist in x for item in sublist]
    split_corpus = [item for sublist in split_dict.values() for item in sublist]
    return split_corpus, plan_index


corpus = create_corpus()
split_corpus, plan_index = create_split_corpus(corpus)
