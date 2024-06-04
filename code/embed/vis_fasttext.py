# TODO:
# 1. Frequency-based sizing
# 2. Transition tpsw() to use a DataFrame internally
# 3. Make it animated (over time)

import argparse

from sklearn.manifold import TSNE
from gensim.models import FastText
import numpy as np
import plotly.graph_objects as go


def plot_similar_words(model_path: str, keys: list, ppl: int = 5):
    model = FastText.load(model_path)

    embedding_clusters = []
    word_clusters = []

    for word in keys:
        embeddings = []
        words = []
        for similar_word, _ in model.wv.most_similar(word, topn=30):
            words.append(similar_word)
            embeddings.append(model.wv[similar_word])
        embedding_clusters.append(embeddings)
        word_clusters.append(words)

    embedding_clusters = np.array(embedding_clusters)
    n, m, k = embedding_clusters.shape  # geting the dimensions
    tsne_model_en_2d = TSNE(perplexity=ppl, n_components=2, init='pca', max_iter=1500, random_state=2020)
    embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)  # reshaping it into 2d so we can visualize it

    tsne_plot_similar_words(keys, embeddings_en_2d, word_clusters, 0.7)


def tsne_plot_similar_words(labels, embedding_clusters, word_clusters, a=0.7):
    fig_data = []
    for label, embeddings, words in zip(labels, embedding_clusters, word_clusters):
        x = embeddings[:, 0]
        y = embeddings[:, 1]
        fig_data.append(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=8, opacity=a),
                                   text=words, hoverinfo='text+name', name=label))
    layout = go.Layout(showlegend=True, legend=dict(orientation="h", y=-0.2))
    fig = go.Figure(data=fig_data, layout=layout)
    fig.show()


if __name__ == '__main__':
    dev_args = ['-m', '/run/media/noah/TOSHIBA EXT/disab_trends_corp/handicap/1990s/fasttext_model.bin', '-k', 'disability', 'neurodiversity', 'handicap', 'golf']

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model_path', type=str, help='Path to the FastText model')
    parser.add_argument('-k', '--keys', nargs='+', help='List of keys')
    args = parser.parse_args(dev_args)
    plot_similar_words(args.model_path, args.keys)
