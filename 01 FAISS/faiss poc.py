import requests
from io import StringIO
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np


def create_embeddings_from_file(input_path, output_path):

    with open(input_path, 'r') as fp:
        sentences = fp.read().split('\n')

    #remove duplicate & NaN's
    sentences = [word for word in list(set(sentences)) if type(word) is str]

    model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = model.encode(sentences)
    print('Training done')
    np.save(output_path, sentence_embeddings)

    return sentence_embeddings


def get_demo_sentences_and_create_embeddings():
    res = requests.get('https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/sick2014/SICK_train.txt')
    # create dataframe
    data = pd.read_csv(StringIO(res.text), sep='\t')
    # data.head()


    # we take all samples from both sentence A and B
    sentences = data['sentence_A'].tolist()
    sentence_b = data['sentence_B'].tolist()
    sentences.extend(sentence_b)  # merge them
    len(set(sentences))  # together we have ~4.5K unique sentences


    urls = [
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2012/MSRpar.train.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2012/MSRpar.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2012/OnWN.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2013/OnWN.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2014/OnWN.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2014/images.test.tsv',
        'https://raw.githubusercontent.com/brmson/dataset-sts/master/data/sts/semeval-sts/2015/images.test.tsv'
    ]
    # each of these dataset have the same structure, so we loop through each creating our sentences data
    for url in urls:
        res = requests.get(url)
        # extract to dataframe
        data = pd.read_csv(StringIO(res.text), sep='\t', header=None, error_bad_lines=False)
        # add to columns 1 and 2 to sentences list
        sentences.extend(data[1].tolist())
        sentences.extend(data[2].tolist())

    # remove duplicates and NaN
    sentences = [word for word in list(set(sentences)) if type(word) is str]

    print(sentences[:10])

    # initialize sentence transformer model
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = model.encode(sentences)
    print('Training done')
    return sentence_embeddings

def download_example_sentence_embeddings():
    data_url = "https://raw.githubusercontent.com/jamescalam/data/main/sentence_embeddings_15K/"

    # create data directory to store data
    if not os.path.exists('./data'):
        os.mkdir('./data')

    # download the numpy binary files (dense vectors)
    for i in range(57):
        res = requests.get(data_url+f"embeddings_{i}.npy")
        with open(f'./data/embeddings_{i}.npy', 'wb') as fp:
            for chunk in res:
                fp.write(chunk)
        print('.', end='')

    # and download the respective text file
    res = requests.get(f"{data_url}sentences.txt")
    with open(f"./data/sentences.txt", 'wb') as fp:
        for chunk in res:
            fp.write(chunk)

    # return sentence_embeddings

def load_sentence_embeddings():
    if not os.path.exists('./data'):
        print('Sentence embeddingsfolder doesn\'t exist. Fetching embeddings...')
        download_example_sentence_embeddings()

    for i in range(57):
        # temp = np.load(f'./data/embeddings_{i}.npy', allow_pickle=True)
        # sentence_embeddings.append(temp)
        if i == 0:
            with open(f'./data/embeddings_{i}.npy', 'rb') as fp:
                sentence_embeddings = np.load(fp)
        else:
            with open(f'./data/embeddings_{i}.npy', 'rb') as fp:
                sentence_embeddings = np.append(sentence_embeddings, np.load(fp), axis=0)

    return sentence_embeddings


def search_experiments(embeddings, lines):
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    if embeddings:
        # load sentence embeddings & sentences
        with open(embeddings, 'rb') as fp:
            embeddings = np.load(fp)
    else:
        embeddings = load_sentence_embeddings()

    with open(lines, 'r', encoding="utf-8") as fp:
        experiments = fp.read().split('\n')

    # create index from dimension
    d = embeddings.shape
    index = faiss.IndexFlatL2(d[1])

    # add embeddings to index
    index.add(embeddings)

    k = 4
    searches = ["Man walking in the park", "The girl is cooking in the kitchen", "Two dogs digging in the dirt"]

    for x in searches:
    # query vector
        xq = model.encode([x])


        D, I = index.search(xq, k)  # search
        print('#####')
        print(x)
        for i in I[0]:
            print(experiments[i])



def main():
    # create_embeddings_from_file('./data/sentences.txt', './data/sentences.npy')
    search_experiments('', './data/sentences.txt')



if __name__ == '__main__':
    main()
