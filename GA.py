import numpy as np
import random
from math import e
from math import pi
import matplotlib.pyplot as plt

# Input values
pop_quantity = 10
number_of_iterations = 100
mutates = round(pop_quantity*0.5)
score = []
all_scores = []
quantity = []
best_scores = []
x_list = []
p = 0


#function to convert list into binary
def convert(list_bin):
    s = [str(i) for i in list_bin]
    binary = str("".join(s))
    return (binary)


def get_bin(x, n=0):
    return format(x, 'b').zfill(n)

# Main class with the specimen and attributes
class Specimen(object):

    def __init__(self):
        self.chromo = [random.randint(0, 1) for i in range(0, 11)]
        if self.chromo[0] == 0:
            self.sign = 0
        elif self.chromo[0] == 1:
            self.sign = 1
        self.chromo_list = self.chromo[1:11]
        self.convert = int(convert(self.chromo_list),2)
        self.float_value = round((self.convert/1000)+self.sign+0.5,3)
        self.prob = 0

    def __add__(self, b):
        score = Specimen()
        new = round(random.uniform(0.499,2.501),3)
        score.chromo = new.chromo
        return score

    #estimate value function - it calculates output for float values of each specimen
    @property
    def estimate(self):
        x = self.float_value
        estimate = round((e ** x * np.sin(10 * pi * x) + 1) / x, 3)
        return estimate
    #mutation function - it mutates two random bits in specimens binary code


    def mutation(self):
        index = random.randint(0, 10)
        self.chromo[index] = (self.chromo[index]+1)%2
        if self.chromo[0] == 0:
            self.sign = 0
        elif self.chromo[0] == 1:
            self.sign = 1
        index = random.randint(0, 10)
        self.chromo[index] = (self.chromo[index] + 1) % 2
        if self.chromo[0] == 0:
            self.sign = 0
        elif self.chromo[0] == 1:
            self.sign = 1
        self.chromo_list = self.chromo[1:11]
        self.convert = int(convert(self.chromo_list), 2)
        self.float_value = round((self.convert / 1000) + self.sign + 0.5, 3)
        return self

    #roulette selection function
    def roulette(self,y):
        s = []
        for i in range(0, pop_quantity):
            z = round(((y.specimens[i].estimate)), 2)
            s.append(z)
        target_func = sum(s)
        z = round((target_func), 2)
        x = random.uniform(1, z)
        for i in range(0, pop_quantity):
            z = round(((y.specimens[i].estimate)), 2)
            x = x - z
            if x <= 0:
                self.chromo = y.specimens[i].chromo
                self.float_value = y.specimens[i].float_value
                return self
            else:
                pass

    #main crossover function after selection function this is activated. It produce child specimens out of two randomly selected parents
    def crossover(self):
        index = random.randint(0, 11)
        index1 = random.randint(0, pop_quantity-1)
        index2 = random.randint(0, pop_quantity-1)
        for i in range(1, pop_quantity):
            list1 = y.specimens[index1].chromo
            list2 = y.specimens[index2].chromo
            self.chromo = list1[0:index] + list2[index:11]
            if self.chromo[0] == 0:
                self.sign = 0
            elif self.chromo[0] == 1:
                self.sign = 1
            self.chromo_list = self.chromo[1:11]
            self.convert = int(convert(self.chromo_list), 2)
            self.float_value = round((self.convert / 1000) + self.sign + 0.5, 3)
            return self

# Population class for Specimen object manipulations
class Population(object):

    def __init__(self):
        self.specimens = [Specimen() for i in range(0, pop_quantity)]

    #main selection function it runs the other function in proper way
    def selection(self):
        self.specimens.sort(key=lambda Osobnik: Osobnik.estimate, reverse=True)
        # print("ruletka:")
        i = 2
        for i in range(2,pop_quantity):
            self.specimens[i].roulette(y)
        #     print(i,self.specimens[i].chromo,self.specimens[i].float_value,self.specimens[i].estimate)
        # print("dziedziczenie")
        for i in range(2,pop_quantity):
            self.specimens[i] = self.specimens[i].crossover()
        #     print(i,self.specimens[i].chromo, self.specimens[i].float_value, self.specimens[i].estimate)

        # mutates are 10% of the whole population

        for i in range(1,mutates):
            index = random.randint(2, pop_quantity-1)
            self.specimens[index] = self.specimens[index].mutation()
            print("osobniki zmutowane:",self.specimens[i].chromo, self.specimens[i].float_value,self.specimens[i].estimate)
            i+=1
        self.specimens.sort(key=lambda Osobnik: Osobnik.estimate, reverse=True)
        # print("Najlepszy osobnik w tej iteracji: ")
        # print(self.specimens[0].chromo,self.specimens[0].float_value,self.specimens[0].estimate)
        # print("-------------------------------------------------------")


# Main activation
y = Population()
for i in range(0, number_of_iterations):
    print('iteracja nr: {}'.format(i + 1))
    for j in y.specimens:
        q = y.specimens[p-1].estimate
        x = y.specimens[p-1].float_value
        score.append(q)
        all_scores.append(q)
        x_list.append(x)
        y.specimens.sort(key=lambda Osobnik: Osobnik.estimate, reverse=True)
        print(p+1,y.specimens[p].chromo,y.specimens[p].float_value,y.specimens[p].estimate)
        p+=1
        if p == pop_quantity:
            # print(f'Najlepszy wynik w generacji nr: ',{i + 1}," : ",{max(score)})
            best_scores.append(i)
            best_scores.append([max(score)])
            p = 0
            score = []
    y.selection()
r = 0
for i in all_scores:
    r=r+1
    quantity.append(r)
a = max(all_scores)
b = all_scores.index(max(all_scores))
c = round(b/pop_quantity)+1
d = x_list[b]
print("Najlepszy wynik: ",a,"Dla x = ",d," W Osobniku nr: ",b,"Generacja nr: ",c)
plt.plot(quantity,all_scores)
plt.ylabel('Function output: f(x) value')
plt.show()