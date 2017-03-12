# coding=utf-8
# 参考 http://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
from math import exp
from random import seed
from random import random


# 初始化一组参数，支持多个隐藏层
def initialize_network(n_inputs, n_hidden_layers, n_outputs):
    network = list()
    for i in range(len(n_hidden_layers)):
        if i == 0:
            pre_hidden_layer = n_inputs
        else:
            pre_hidden_layer = n_hidden_layers[i - 1]

        current_hidden_layer = n_hidden_layers[i]
        hidden_layer = [{'weights': [random() for _i in range(pre_hidden_layer + 1)]} for _i in
                        range(current_hidden_layer)]
        network.append(hidden_layer)

    output_layer = [{'weights': [random() for _i in range(current_hidden_layer + 1)]} for _i in range(n_outputs)]
    network.append(output_layer)
    return network


# 计算一个神经元的激活
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


# 转变激活值
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))


# 梯度转换，依据所用激活函数而定
def transfer_derivative(output):
    return output * (1.0 - output)


# 前向计算输出
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs


# 反向传播误差，并将各层每个结果存放在对应的神经元
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        # 其余层
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        # 最后一层
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])


# 更新各个神经元的权重
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
            neuron['weights'][-1] += l_rate * neuron['delta']


# 训练
def train_network(network, train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - outputs[i]) ** 2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))


# 预测
def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))


seed(1)
dataset = [[2.7810836, 2.550537003, 0],
           [1.465489372, 2.362125076, 0],
           [3.396561688, 4.400293529, 0],
           [1.38807019, 1.850220317, 0],
           [3.06407232, 3.005305973, 0],
           [7.627531214, 2.759262235, 1],
           [5.332441248, 2.088626775, 1],
           [6.922596716, 1.77106367, 1],
           [8.675418651, -0.242068655, 1],
           [7.673756466, 3.508563011, 1]]
n_inputs = len(dataset[0]) - 1
n_outputs = len(set([row[-1] for row in dataset]))
network = initialize_network(n_inputs, [5, 4], n_outputs)
train_network(network, dataset, 0.05, 1000, n_outputs)
for layer in network:
    print(layer)

for row in dataset:
    prediction = predict(network, row)
    print('Expected=%d, Got=%d' % (row[-1], prediction))
