import numpy as np
from collections import Counter
from swaptest import fidelity
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def accuracy(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)
def major_vote(labels):
    x = Counter(labels)
    return x.most_common(1)[0][0]
def sort_but_return_index(xs):
    """Note that we must sort for large to small, because scalar product between 
    two similar vectors is almost 1 (other wise with Eucliean distance), I wrong this
    point and take few hours to catch this error :))

    Args:
        xs (list): list of scalar products between train vectors and one test vector

    Returns:
        list: sorted list but return indices 
    """
    newxs = sorted(range(len(xs)), key=lambda k: xs[k])
    newxs.reverse()
    return newxs
def get_sublist_with_indices(xs, indices, k):
    return [xs[index] for index in indices][:k]
def encode(xss):
    amplitudes = np.sqrt(np.einsum('ij,ij->i', xss, xss))
    amplitudes[amplitudes == 0] = 1
    normalised_data = xss / amplitudes[:, np.newaxis]
    return normalised_data
def distances(xs, yss, iteration):
    distances = []
    for ys in yss:
        distances.append(fidelity(xs,ys, iteration))
    return distances

def predict(train_datas, train_labels, test_datas, k, iteration):
    """Return predict labels QKNN algorithm

    Args:
        train_datas (numpy array 2D): Vectors in train data
        train_labels (numpy array 1D): Labels in train data
        test_datas (numpy array 2D): Vectors in test data
        k (interger): Number of neighboors

    Returns:
        [type]: [description]
    """
    predict_labels = []
    num_of_test_datas = len(test_datas)
    i = 0
    for test_data in test_datas:
        xs = distances(test_data, train_datas, iteration)
        indices_of_sorted_xs = sort_but_return_index(xs)
        labels = get_sublist_with_indices(train_labels, indices_of_sorted_xs, k)
        predict_labels.append(major_vote(labels))
        i = i + 1
        print(str(i/num_of_test_datas*100) + '%')
        # print('xs: ', xs)
        # print('indices_of_sorted_xs: ', indices_of_sorted_xs)
        # print('labels: ', labels)
    return predict_labels
def bench_mark(ground_truth, predict):
    accuracy = accuracy_score(ground_truth, predict)
    # precision tp / (tp + fp)
    precision = precision_score(ground_truth, predict, average="weighted")
    # recall: tp / (tp + fn)
    recall = recall_score(ground_truth, predict, average="weighted")
    f1 = f1_score(ground_truth, predict, average="micro")
    matrix = confusion_matrix(ground_truth, predict)
    return accuracy, precision, recall, matrix

# # xs = np.asarray([1,2,3,2])
# train_datas = np.asarray([
#     [1,1,1,2],
#     [1,0,0,2],
#     [1,2,0.5,2],
#     [1,0,0,0.6],
#     [2,3,0.5,2],
#     [2,0,0,0.6]
# ])

# train_labels = np.asarray([
#     1,2,1,1,0,2
# ])

# test_datas = np.asarray([
#     [1,1,1,2.1],
#     [1.3,0,0,2],
# ])

# print(predict(train_datas, train_labels, test_datas))




