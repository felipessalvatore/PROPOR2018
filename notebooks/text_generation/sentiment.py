import numpy as np
import pandas as pd
import os

try:
    from word_lists import masculine_names, feminine_names, bad_adjectives, good_adjectives
except ImportError:
    from text_generation.word_lists import masculine_names, feminine_names, bad_adjectives, good_adjectives  # noqa

try:
    from word_lists import masculine_names, feminine_names, bad_adjectives, good_adjectives
except ImportError:
    from text_generation.word_lists import masculine_names, feminine_names, bad_adjectives, good_adjectives  # noqa


def get_new_item(item_list, src_list):
    size = len(src_list)
    new_item = src_list[np.random.choice(size)]
    while new_item in item_list:
        new_i = np.random.choice(size)
    return new_item


def generate_sentiment_data(size=5000,
                            train_test_split=0.8):

    upper_bound = int(size / 3)

    # positive sentences
    all_positive_sen = []
    for i in range(upper_bound):
        good_predicate = get_new_item([], good_adjectives)
        bad_predicate = get_new_item([], bad_adjectives)
        if i % 2 == 0:
            person = get_new_item([], masculine_names)
        else:
            person = get_new_item([], feminine_names)
            if good_predicate[-1] == "o":
                good_predicate = good_predicate[:-1] + "a"
            if bad_predicate[-1] == "o":
                bad_predicate = bad_predicate[:-1] + "a"
        if i % 4 == 0:
            sentence = "{} é {}".format(person, good_predicate)
        elif i % 4 == 1:
            sentence = "{} sempre foi {}".format(person, good_predicate)
        elif i % 4 == 2:
            sentence = "{} era {}".format(person, good_predicate)
        else:
            sentence = "{} é {}, mas as vezes ele parece ser {}".format(person,
                                                                        good_predicate, bad_predicate)
        all_positive_sen.append(sentence)

    # negative sentences
    all_negative_sen = []
    for i in range(upper_bound):
        good_predicate = get_new_item([], good_adjectives)
        bad_predicate = get_new_item([], bad_adjectives)
        if i % 2 == 0:
            person = get_new_item([], masculine_names)
        else:
            person = get_new_item([], feminine_names)
            if good_predicate[-1] == "o":
                good_predicate = good_predicate[:-1] + "a"
            if bad_predicate[-1] == "o":
                bad_predicate = bad_predicate[:-1] + "a"
        if i % 4 == 0:
            sentence = "{} é {}".format(person, bad_predicate)
        elif i % 4 == 1:
            sentence = "{} sempre foi {}".format(person, bad_predicate)
        elif i % 4 == 2:
            sentence = "{} era {}".format(person, bad_predicate)
        else:
            sentence = "mesmo que as vezes {} é {}, {} é muito {}".format(person,
                                                                          good_predicate,
                                                                          person,
                                                                          bad_predicate)
        all_negative_sen.append(sentence)

    # neutral sentences
    all_neutral_sen = []
    for i in range(upper_bound):
        good_predicate = get_new_item([], good_adjectives)
        bad_predicate = get_new_item([], bad_adjectives)
        if i % 2 == 0:
            person = get_new_item([], masculine_names)
        else:
            person = get_new_item([], feminine_names)
            if good_predicate[-1] == "o":
                good_predicate = good_predicate[:-1] + "a"
            if bad_predicate[-1] == "o":
                bad_predicate = bad_predicate[:-1] + "a"
        if i % 4 == 0:
            sentence = "{} não é {} nem {}".format(person,
                                                   good_predicate,
                                                   bad_predicate)
        elif i % 4 == 1:
            predicate = get_new_item([], [good_predicate, bad_predicate])
            sentence = "{} nunca foi {}".format(person, predicate)
        elif i % 4 == 2:
            predicate = get_new_item([], [good_predicate, bad_predicate])
            sentence = "{} parece ser {}, mas eu não sei".format(
                person, predicate)
        else:
            sentence = "{} é tanto {} quanto {}".format(person,
                                                        good_predicate,
                                                        bad_predicate)
        all_neutral_sen.append(sentence)

    np.random.shuffle(all_positive_sen)
    np.random.shuffle(all_negative_sen)
    np.random.shuffle(all_neutral_sen)

    sentences = all_negative_sen + all_positive_sen + all_neutral_sen
    labels = [0] * len(all_negative_sen) + [1] * \
        len(all_positive_sen) + [2] * len(all_neutral_sen)

    df_dict = {"text": sentences,
               "label": labels}

    df = pd.DataFrame(df_dict)
    df = df[["text", "label"]]
    df = df.sample(frac=1).reset_index(drop=True)

    cut_point = int(len(df) * train_test_split)

    df_train = df.iloc[:cut_point]
    df_test = df.iloc[cut_point:]

    # ### Saving to CSV

    if not os.path.exists("./data"):
        os.makedirs("data/")

    df_train.to_csv("data/sentiment_train.csv", index=False)
    df_test.to_csv("data/sentiment_test.csv", index=False)


if __name__ == '__main__':
    generate_sentiment_data()
