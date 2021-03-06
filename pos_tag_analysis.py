from nltk.tag import pos_tag
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from datautils import *
import os
import pickle
from collections import defaultdict

genres = os.listdir(PATH)

tags_per_genre = defaultdict(lambda: defaultdict(int))        #{genre: {tag: count}}
tags_per_author = defaultdict(lambda: defaultdict(int))
total_tags_per_genre = defaultdict(int)
total_tags_per_author = defaultdict(int)
all_tags = set()

for g in genres:
    print("genre: {}".format(g))
    gpath = os.path.join(PATH, g)
    for a in os.listdir(gpath):
        apath = os.path.join(gpath, a)
        tokenized_sentences = document_tokenize(apath)
        for sent in tokenized_sentences:
            #print(sent)
            tags = pos_tag(sent)
            for word, tag in tags:
                tags_per_genre[g][tag] += 1
                tags_per_author[g + '_' + a][tag] += 1
                total_tags_per_genre[g] += 1
                total_tags_per_author[g + '_' + a] += 1
                all_tags.update([tag])

print_dict(total_tags_per_genre)
TAGS = list(all_tags)
means = [0]*len(TAGS)
indices = [x for x in range(len(TAGS))]
color_g={'Adventure':'b','Horror': 'k', 'Humor': 'c', 'Fantasy': 'r', 'Detective':'g'}
plt.figure(1)
for j, (key, values) in enumerate(tags_per_genre.items()):
    X = indices
    Y = [values[TAGS[x]]/float(total_tags_per_genre[key]) * 100 for x in indices]
    means = [means[i] + Y[i] for i in indices]
    plt.plot(X, Y, label=key, color=color_g[key])
plt.legend()
plt.xticks(indices, TAGS, rotation="vertical")
plt.xlabel("POS TAGS")
plt.ylabel("Percentage")
#plt.show()
plt.savefig("./plots/output.png")

means = [val / float(5) for val in means]
plt.figure(2)
for j, (key, values) in enumerate(tags_per_genre.items()):
    X = indices
    Y = [values[TAGS[x]]/float(total_tags_per_genre[key]) * 100 - mean[x] for x in indices]
    plt.plot(X, Y, label=key, color=color_g[key])
plt.legend()
plt.xticks(indices, TAGS, rotation="vertical")
plt.xlabel("POS TAGS")
plt.ylabel("deviation from mean")
#plt.show()
plt.savefig("./plots/output_against_mean.png")

j = 3
for g in genres:
    colors = ['b','k','c','r','m']
    plt.figure(j)
    j += 1
    means = [0]*len(TAGS)
    m = 0
    for k, (key, values) in enumerate(tags_per_author.items()):
        genre = key.split('_')[0]
        if genre == g:
            print(genre, g)
            X = indices
            Y = [values[TAGS[x]]/float(total_tags_per_author[key]) * 100 for x in indices]
            means = [means[i] + Y[i] for i in indices]
            plt.plot(X, Y, label=key, color=colors[m])
            m += 1
    plt.legend()
    plt.xticks(indices, TAGS, rotation="vertical")
    plt.xlabel("POS TAGS")
    plt.ylabel("Percentage")
    #plt.show()
    plt.savefig("./plots/output_{}.png".format(g))

    means = [m/float(5) for m in means]
    plt.figure(j)
    j += 1
    m = 0
    for k, (key, values) in enumerate(tags_per_author.items()):
        genre = key.split('_')[0]
        if genre == g:
            X = indices
            Y = [values[TAGS[x]]/float(total_tags_per_author[key]) * 100 - means[x] for x in indices]
            plt.plot(X, Y, label=key, color=colors[m])
            m += 1
    plt.legend()
    plt.xticks(indices, TAGS, rotation="vertical")
    plt.xlabel("POS TAGS")
    plt.ylabel("deviation from mean")
    #plt.show()
    plt.savefig("./plots/output_against_mean_{}.png".format(g))
