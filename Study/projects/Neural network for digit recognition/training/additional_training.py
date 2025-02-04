import random
import csv
import numpy as np

x_test=[]
y_test=[]
x_train=[]
y_train=[]
with open('mnist_train_50_50_center.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        row=list(map(float,list(row[0].split(","))))
        x_train.append(np.array([row[1:]])/255.0)
        y=[[0]]*10
        y[int(row[0])]=[1]
        y_train.append(y)
with open('mnist_test_50_50_center.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        row=list(map(float,list(row[0].split(","))))
        x_test.append(np.array([row[1:]])/255.0)
        y=[[0]]*10
        y[int(row[0])]=[1]
        y_test.append(y)
print(x_test,'1')
def readFile(fileName):
    rez=[]
    with open(fileName, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            row=list(map(float,list(row[0].split(","))))
            rez.append(row)
    return np.array(rez)
class neoron_cet:
    def __init__(self, x, y):  # Инициализация класса сети
        self.input = x  # Входные данные
        self.biases1 = readFile('biases1.csv')  # Инициализация смещений для первого слоя
        self.biases2 = readFile('biases2.csv')  # Инициализация смещений для выходного слоя
        self.weights1 = readFile('weight1.csv')  # Инициализация весов для первого слоя
        self.weights2 = readFile('weight2.csv')  # Инициализация весов для выходного слоя
        self.y = y  # Целевой вывод
    
    def SGD(self, x_train,y_train, epochs, mini_batch_size, lmd):
        n = len(x_train)
        for j in range(epochs):
            mini_batches_x = [x_train[k:k+mini_batch_size]for k in range(0, n, mini_batch_size)]
            mini_batches_y = [y_train[k:k+mini_batch_size]for k in range(0, n, mini_batch_size)]
            for i in range(len(mini_batches_x)):
                self.update_mini_batch(mini_batches_x[i],mini_batches_y[i], lmd)
            print("Epoch:", j+1)
            loss_temp = self.calculate_mse(x_train, y_train)
            rez_temp=test()
            if (loss > loss_temp)or(rez_test>rez_temp):
                write_files(self.weights1, self.weights2, self.biases1, self.biases2)
                loss = loss_temp
                rez_test=rez_temp
            print("MSE:", loss_temp)
            

    def calculate_mse(self, x, y):
        mse = 0
        for i in range(len(x)):
            self.feedforward(x[i])
            mse += np.mean((self.output - y[i]) ** 2)
        mse /= len(x)
        return mse
    
    def update_mini_batch(self, mini_batch_x,mini_batch_y, lmd):
        nabla_b1 = np.zeros(self.biases1.shape)
        nabla_b2 = np.zeros(self.biases2.shape)
        nabla_w1 = np.zeros(self.weights1.shape)
        nabla_w2 = np.zeros(self.weights2.shape)
        for i in range(len(mini_batch_x)):
            d_weight1,d_weight2,d_biases1,d_biases2 = self.backprop(mini_batch_x[i], mini_batch_y[i],lmd)
            nabla_b1 += d_biases1
            nabla_b2 +=d_biases2
            nabla_w1 += d_weight1
            nabla_w2 +=d_weight2
        self.weights1 -=nabla_w1
        self.weights2 -=nabla_w2
        self.biases1 -=nabla_b1
        self.biases2 -=nabla_b2
        
    def feedforward(self, input):
        self.layer1 = relu(np.dot(self.weights1, input.transpose()) + self.biases1)# Прямое распространение через первый слой(получения вектор столбца)
        self.output = sigmoid(np.dot(self.weights2, self.layer1) + self.biases2)  # Прямое распространение через второй слой
        
    def backprop(self,x,y,lmd):
    #генерация случаеных входных\выходных данных из обучаещей выборки
        self.feedforward(x)
        delta2 = 2*(self.output-y)*sigmoid_prime(self.output)#градиент для выходного слоя
        d_weight2 =lmd*( np.dot(delta2, self.layer1.transpose()))
        delta1 = np.dot(self.weights2.transpose(), delta2) * reluPrime(self.layer1)#градиент для первого слоя
        d_weight1 = np.dot(delta1, x)*lmd
        d_biases2 = delta2*lmd
        d_biases1 = delta1*lmd 
        return d_weight1,d_weight2,d_biases1,d_biases2

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))  # Функция активации сигмоид

def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))  # Производная функции активации сигмоид

def softmax(x):
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps, axis=0)

def softmax_derivative(x):
    s = softmax(x)
    return np.diagflat(s) - np.dot(s, s.transpose())

def relu(x):
    return np.maximum(0., x)

def reluPrime(x):
    return np.where(x > 0, 1., 0.)

def cross_entropy_derivative(y, y_hat):
    return y_hat - y

def test():
    loss=0
    rez=""
    for x,y in zip(x_test,y_test):
        net.feedforward(x)
        if(np.where(net.output == max(net.output))[0][0]!=(y.index(max(y)))):
            loss+=1
    print("не угаданных",loss)
    return loss

def write_files(weights1,weights2,biases1,biases2):
    with open('weight1.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for w1 in weights1:
            spamwriter.writerow(w1)
    with open('weight2.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for w2 in weights2:
            spamwriter.writerow(w2)
    with open('biases1.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for b1 in biases1:
            spamwriter.writerow(b1)
    with open('biases2.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for b2 in biases2:
            spamwriter.writerow(b2)
    
    
net = neoron_cet(x_train, y_train)
#net.SGD(x_train, y_train,10000,1,0.05)

