# Write your code here
import nltk
import collections
import random


def stage_6_workflow():
    """Stage 6 implementation"""
    file_name = input()
    # file_name = "corpus.txt"
    token_result = convert(file_name)
    # bigram = convert_to_bigram(token_result)
    trigram = convert_to_trigram(token_result)
    # result = create_head_and_tail_counter(bigram)
    result = create_head_and_tail_counter(trigram)
    construct_random_sentence_by_trigram(result, sentence_required=10, length_required=10)

    # tail_count_enquiry(result)
    # bigram_statistics(bigram)
    # bigram_enquiry(bigram)
    # corpus_statistics(token_result)
    # enquiry(token_result)


def convert(file_name):
    token_result = []
    exclude_them = r"[^\s\n\t]+"
    with open(file_name, "r", encoding="utf-8") as f:
        for i in f.readlines():
            token_result += (nltk.regexp_tokenize(i, exclude_them))
    return token_result


def convert_to_bigram(list_information):
    bigram = list(nltk.bigrams(list_information))
    return bigram


def convert_to_trigram(list_information):
    """stage 6 requirement"""
    trigram = list(nltk.trigrams(list_information))
    return trigram


def find_unique(file_name):
    return len(set(file_name))


def corpus_statistics(list_information):
    unique_number = find_unique(list_information)
    print("Corpus statistics")
    print(f"All tokens: {len(list_information)}")
    print(f"Unique tokens: {unique_number}\n")


def bigram_statistics(bigram_information):
    print(f"Number of bigrams: {len(bigram_information)}\n")


def enquiry(token_list):
    index = input()
    if index == "exit":
        exit()

    try:
        index = int(index)
    except ValueError:
        print("Type Error. Please input an integer.")
        return enquiry(token_list)

    try:
        result = token_list[index]
        print(result)
    except IndexError:
        print("Index Error. Please input an integer that is in the range of the corpus.")
    finally:
        return enquiry(token_list)


def bigram_enquiry(bigram_information):
    index = input()
    if index == "exit":
        exit()

    try:
        index = int(index)
    except ValueError:
        print("Type Error. Please input an integer.")
        return bigram_enquiry(bigram_information)

    try:
        result = bigram_information[index]
        print(f"Head: {result[0]}\tTail: {result[-1]}")
    except IndexError:
        print("Index Error. Please input a value that is not greater than the number of all bigrams.")
    finally:
        return bigram_enquiry(bigram_information)


def tail_count_enquiry(head_and_tail_list):
    head = input()
    if head == "exit":
        exit()

    try:
        print(f"Head: {head}")
        for i in head_and_tail_list[head]:
            print(f"Tail: {i}\t\t\tCount: {head_and_tail_list[head][i]}")
    except KeyError:
        print("Key Error. The requested word is not in the model. Please input another word.")
    finally:
        print()
        return tail_count_enquiry(head_and_tail_list)


def create_head_and_tail_counter(bigram_or_trigram_list):
    dictionary = {}
    for i in bigram_or_trigram_list:
        dictionary.setdefault(" ".join(i[:len(i) - 1]), []).append(i[-1])
    for i, j in dictionary.items():
        dictionary[i] = collections.Counter(j)
    return dictionary


def add_one_word(previous_word, head_tail_counter):
    beginning_word_counter = head_tail_counter[previous_word]
    population = [i for i in beginning_word_counter]
    weights = [beginning_word_counter[i] for i in beginning_word_counter]
    next_word = random.choices(population=population, weights=weights)
    return next_word


def add_one_word_for_trigram(previous_word, head_tail_counter):
    beginning_word_counter = head_tail_counter[previous_word]
    population = [i for i in beginning_word_counter]
    weights = [beginning_word_counter[i] for i in beginning_word_counter]
    next_word = random.choices(population=population, weights=weights)
    return next_word


def construct_beginning_word(list_information):
    sentence_ending = ["?", ".", "!"]
    beginning_word = random.choice(list_information)
    if beginning_word[-1] in sentence_ending or not beginning_word[0].isupper():
        return construct_beginning_word(list_information)
    return beginning_word


def construct_beginning_token(token_dictionary):
    """this function is for stage 6"""
    sentence_ending = ["?", ".", "!"]
    beginning_token = random.choice(list(token_dictionary.keys()))
    first_vocab_end = beginning_token.split()[0][-1]
    if beginning_token[-1] in sentence_ending or first_vocab_end in sentence_ending or not beginning_token[0].isupper():
        return construct_beginning_token(token_dictionary)
    return beginning_token


def construct_random_sentence(list_information, head_tail_counter, sentence_required=10, length_required=10):
    """This function is for stage 5"""
    result_list = []
    sentence_ending = r"[\?\.!]"

    while len(result_list) != sentence_required:
        beginning_word = construct_beginning_word(list_information)
        sentence = [beginning_word]

        while len(sentence) < length_required:
            next_word = add_one_word(sentence[-1], head_tail_counter)
            sentence += next_word
            if len(sentence) < 5 and next_word[0][-1] in sentence_ending:
                sentence = [beginning_word]
            if len(sentence) >= 5 and next_word[0][-1] in sentence_ending:
                break
        result_list.append(sentence)
        if sentence[-1][-1] not in sentence_ending:
            del result_list[-1]

    result_list = [" ".join(i) for i in result_list]

    for i in result_list:
        print(i)


def construct_random_sentence_by_trigram(head_tail_counter, sentence_required=10, length_required=10):
    """This function is for stage 6"""
    result_list = []
    sentence_ending = r"[\?\.!]"

    while len(result_list) != sentence_required:
        beginning_phrase = construct_beginning_token(head_tail_counter).split()
        sentence = beginning_phrase[:]

        while len(sentence) < length_required:
            next_word = add_one_word_for_trigram(" ".join(sentence[len(sentence) - 2:]), head_tail_counter)
            sentence += next_word
            if len(sentence) < 5 and next_word[0][-1] in sentence_ending:
                beginning_phrase = construct_beginning_token(head_tail_counter).split()
                sentence = beginning_phrase[:]
            if len(sentence) >= 5 and next_word[0][-1] in sentence_ending:
                break
        result_list.append(sentence)
        if sentence[-1][-1] not in sentence_ending:
            del result_list[-1]

    result_list = [" ".join(i) for i in result_list]

    for i in result_list:
        print(i)


stage_6_workflow()
