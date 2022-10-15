from errno import errorcode
from json.tool import main
import math
from pyexpat import features
from statistics import mean
import time
from scipy.io import loadmat
import matplotlib
import matplotlib.pyplot as pyplot
import numpy as np
TRAIN_K, TRAIN_D, TRAIN_m = 10, 64, 700
class gaussian_classifier:
    def __init__(self, data):
        self.mean_vectors = list()
        self.variance_squared = list()
        self.training_data = np.array(data['digits_train'])
        self.test_data = np.array(data['digits_test'])

    def calculate_mean_vector(self, class_index):
        digits_train = self.training_data
        mean_vector = [0] * 64 # 64 features
        num_training_points = np.size(digits_train, 1)
        for i in range(num_training_points): # loop through training data
            datapoint = digits_train[:,i,class_index]
            # for each training datapoint, add the value to the mean
            mean_vector = mean_vector + datapoint

        # divide meanvector by num of training data
        mean_vector = mean_vector / num_training_points
        return mean_vector
    
    def calculate_variance_squared(self):
        digits_train = self.training_data
        mean_vectors = self.mean_vectors
        num_classes, num_datapoints, num_features = np.size(digits_train, 2), np.size(digits_train, 1), np.size(digits_train, 0)
        variance = 0

        for class_num in range(num_classes):
            mean_vector = self.mean_vectors[class_num]
            for data_point in range(num_datapoints):
                for feature in range(num_features):
                    x, u = digits_train[feature, data_point, class_num], mean_vector[feature]
                    variance += (x-u)**2
        DM = num_features*num_datapoints * 10 # K = 10

        return variance / DM

    def classify_data(self, datapoint):
        D = 64
        K = 10
        def conditional_probability(class_id):
            variance_squared, mean_vector = self.variance_squared, np.asarray(self.mean_vectors[class_id])
            variance_sum = sum((datapoint - mean_vector)**2)
            #print('variance_squared ', variance_squared)
            probability = (2*math.pi*variance_squared)**(-D/2)*math.exp(-1/(2*variance_squared)* variance_sum)
            return probability
        #find conditional probablity for each class
        probabilities = list()
        for i in range(K):
            probabilities.append(conditional_probability(i))
        return np.argmax(probabilities)
    
    def test(self):
        digits_test = self.test_data
        m, K = 400, 10
        error_counter = [0] * K
        for class_id in range(K):
            for datapoint_id in range(m):
                datapoint = digits_test[:,datapoint_id, class_id]
                if self.classify_data(datapoint) != class_id:
                    error_counter[class_id] += 1
        print(f'Total Error: {sum(error_counter)}/4000')
        print('Error by digit:')
        for i in range(K):
            digit = (i+1)%10
            print(f'Digit <<{digit}>> : {error_counter[i]}/400')



    def train(self):
        digits_train = self.training_data
        num_classes = np.size(digits_train, 2)
        for i in range(num_classes):
            mean_vector = self.calculate_mean_vector(i)
            self.mean_vectors.append(mean_vector)
        self.variance_squared= self.calculate_variance_squared()
    
    def plot(self):
        fig, ax = pyplot.subplots(1, TRAIN_K, figsize=(15,2.3), dpi=300)
        fig.suptitle('Gaussian Classifier Trained Model', size=15, x=0.2)
        for digit_id in range(0, TRAIN_K):
            mean_vector = self.mean_vectors[digit_id]
            ax[digit_id].imshow(np.reshape(mean_vector,(8,8)))
            ax[digit_id].axis('off')
            ax[digit_id].set_title(str(digit_id+1))

class bayes_classifier:
    
    def __init__(self, data):
        self.n_k_values = list()
        self.training_data = np.array(data['digits_train'])
        self.test_data = np.array(data['digits_test'])
        ## convert the data to binary
        def convert_data(dataset):
            K, m_Val, D = np.size(dataset, 2), np.size(dataset, 1), np.size(dataset, 0)
            for k in range(K):
                for m in range(m_Val):
                    for d in range(D):
                        val = dataset[d, m, k]
                        if val > 0.5:
                            val = 1
                        else:
                            val = 0
                        dataset[d, m, k] = val
            return dataset

        self.training_data = convert_data(self.training_data)
        self.test_data = convert_data(self.test_data)


    def calculate_n_k(self, class_index):
        digits_train = self.training_data
        p_ck = 1/10
        n_k = [0] * TRAIN_D
        for datapoint_id in range(TRAIN_m):
            n_k = n_k + digits_train[:, datapoint_id, class_index]
        n_k = n_k / TRAIN_m
        return n_k

    def classify_data(self, datapoint):
        D = 64
        K = 10
        def conditional_probability(class_id):
            probability = 1
            n_k = self.n_k_values[class_id]
            for feature_id in range(D):
                if datapoint[feature_id] == 1:
                    probability *= n_k[feature_id]
                else:
                    probability *= (1 - n_k[feature_id])
            return probability
        #find conditional probablity for each class
        probabilities = list()
        for i in range(K):
            probabilities.append(conditional_probability(i))
        return np.argmax(probabilities)
    
    def test(self):
        digits_test = self.test_data
        m, K = 400, 10
        error_counter = [0] * K
        for class_id in range(K):
            for datapoint_id in range(m):
                datapoint = digits_test[:,datapoint_id, class_id]
                if self.classify_data(datapoint) != class_id:
                    error_counter[class_id] += 1
        print(f'Total Error: {sum(error_counter)}/4000 | {sum(error_counter)/4000}')
        print('Error by digit:')
        for i in range(K):
            digit = (i+1)%10
            print(f'Digit <<{digit}>> : {error_counter[i]}/400')

    def train(self):
        digits_train = self.training_data
        num_classes = np.size(digits_train, 2)
        for i in range(num_classes):
            n_k = self.calculate_n_k(i)
            self.n_k_values.append(n_k)

    def plot(self):
        fig, ax = pyplot.subplots(1, TRAIN_K, figsize=(15,2.3),dpi=300)
        fig.suptitle('Naive Bayes Trained Model', size=15, x=0.2)
        for digit_id in range(0, TRAIN_K):
            n_k = self.n_k_values[digit_id]
            ax[digit_id].imshow(np.reshape(n_k,(8,8)))
            ax[digit_id].axis('off')
            ax[digit_id].set_title(str(digit_id+1))


if __name__ == "__main__":
    data = loadmat('data/assignment1.mat')
    gc = gaussian_classifier(data)
    gc.train()
    gc.test()
    gc.plot()
    time.sleep(5)
    bc = bayes_classifier(data)
    bc.train()
    bc.test()
    bc.plot()
    pass
