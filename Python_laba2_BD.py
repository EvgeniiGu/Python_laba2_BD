from dataclasses import *
from random import sample
from threading import Thread
from timeit import time
from operator import itemgetter

@dataclass
class Memory:
    _size: int = 0
    _memory_dict: dict = field(default_factory=dict)
    def _create_empty_chunk(self, size):
        self._memory_dict.update({x: None for x in range(self._size, self._size + size + 1)})
        self._update_size(self._size + size + 1)
    def _update_size(self, i):
        self._size += i

    #при связанном распределении памяти
    def allocate_associated_chunk(self, list_of_elements):
        iter = 0
        first_cell_address = self._size
        len_list_of_elements = len(list_of_elements)
        if len_list_of_elements <= self._size + len_list_of_elements:
            self._create_empty_chunk(len_list_of_elements)
        for i in self._memory_dict:
            if self._memory_dict[i] is None:
                if all(self._memory_dict[number] is None for number in [j for j in range(i, len_list_of_elements)]):
                    self._memory_dict[i] = list_of_elements[iter]
                    iter += 1
                    if iter == len_list_of_elements:
                        return first_cell_address
                
    #при последовательном распределении памяти
    def allocate_sequential_chunk(self, list_of_elements):
        flag = False
        len_list_of_elements = len(list_of_elements)
        if len_list_of_elements <= self._size + len_list_of_elements:
            self._create_empty_chunk(len_list_of_elements)
        for i in self._memory_dict:
            if self._memory_dict[i] is not None:
                continue
            else:
                if flag != True:
                    first_cell_address = i
                    flag = True
                self._memory_dict[i]
        return first_cell_address
    def read(self, first_cell_address):
        list_of_elements = []
        address_space = list(self._memory_dict.keys())
        for iter in address_space:
            if iter == first_cell_address:
                for k in address_space[iter:]:
                    if self._memory_dict[k] is not None:
                        list_of_elements.append(self._memory_dict[k])
                    else:
                        break
        return list_of_elements


#@dataclass
#class Memory:
#    _size: int = 0
#    _memory_cell_addresses: list = field(default_factory=list)
#    _memory_dict: dict = field(default_factory=dict)

#    def pick_out_and_save(self, size, list_of_elements):
#        new_size = self._size + size
#        self._memory_cell_addresses = [x for x in range(new_size)]
#        new_address_space = self._memory_cell_addresses[self._size:new_size]
#        self._memory_dict.update({memory_cell: y for memory_cell, y in zip(new_address_space, list_of_elements)})
#        self._size = new_size
#        return new_address_space



def adjusting_memory_size():
    #memory.size += size
    #memory.memory_cell_addresses[memory.size:memory.size+size]
    #while not memory.stop:
    #print(memory.size)
    #memory.memory_cell_addresses = range(memory.size)
    time.sleep(1)

class Stack:
    pass

class Stack_consistent(Stack):
    def __init__(self, list_of_elements):
        self._list_of_elements_size = len(list_of_elements)
        self._first_cell_address = memory.pick_out_and_save(self._list_of_elements_size, list_of_elements)

    def __add__(self, other):
        _new_address_space = self._address_space + other._address_space
        new_size = self._size + other.size
        return Stack_consistent(_new_address_space)

    def inserting(self, element):
        if len(self._stack) < self._size:
            self._stack.append(element)
        else:
            print("ERROR")

    def delete(self):
        removed_element = self._stack.pop(len(self._stack)-1)
        return removed_element
    def browse(self):
        return([memory._memory_dict[i] for i in self._address_space])

class Stack_related(Stack):
    def __init__(self, list_of_elements):
        self._first_cell_address = allocate_sequential_chunk(list_of_elements)

    def __add__(self, other):
        _new_stack = self._stack + other._stack
        return Stack_related(_new_stack)

    def inserting(self, element):
        self._stack.append(element)

    def delete(self):
        removed_element = self._stack.pop(len(self._stack)-1)
        return removed_element

    def browse(self):
        return(self._stack)

def main():
    choise_1 = input('''1)Соэдать три стека при последовательном распределении памяти\n2)Соэдать три стека при связанном распределении памяти\n''')
    stack = []
    if choise_1=="1":
        stack.append(Stack_consistent(list(input("Введите элементы стека с разделителем пробел (если ввести больше, запишутся только первые): ").split())))
    elif choise_1=="2":
        stack.append(Stack_related(list(input("Введите элементы стека с разделителем пробел: ").split())))
    print("Вы ввели: ", stack[i].browse())
    while True:
        choise_2 = input('''1)Вставка элемента в стек\n2)Удаления элемента из стека\n3)Просмотр стека\n4)Объединить стеки\n5)Завершить работу\n''')
        if choise_2 == "5":
            break
        elif choise_2 == "4":
            new_stack = stack[0] + stack[1]
            new_stack = new_stack + stack[2]
            print(new_stack._address_space)
        else:
            choise_2_dict = {"1": "вставки элемента в стек", "2": "удаления элемента из стека", "3":"просмотра стека"}
            choise_3 = int(input('''Введите номер стека для ''' + choise_2_dict[choise_2] + ": "))
            if choise_2 == "1":
                stack[choise_3-1].inserting(input("Введите элемент: "))
            elif choise_2 == "2":
                print("Удалено: " + stack[choise_3-1].delete())
            elif choise_2 == "3":
                print(stack[choise_3-1].browse())

#th_1, th_2 = Thread(target = adjusting_memory_size), Thread(target = main)

def new():
    inp = input("Введите элементы стека с разделителем пробел: ").split()
    cell = memory.allocate_associated_chunk(inp)
    print(memory._memory_dict)
    inp2 = input("Введите элементы стека с разделителем пробел: ").split()
    cell2 = memory.allocate_associated_chunk(inp2)
    #print(memory._size)
    print(memory._memory_dict)
    print(memory.read(cell))

if __name__ == "__main__":
    memory = Memory()
    #main()
    new()
#    th_1.start(), th_2.start()
#    th_1.join(), th_2.join()