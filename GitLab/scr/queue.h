#pragma once

#include "linked_list.h"

template<typename T>
class Queue {
private:
    LinkedList::SinglyLinkedList<T> data;
    int len;

public:
    Queue();

    T dequeue();

    void enqueue(T);

    int size();

    T operator[](int index);
};


template<typename T>
T Queue<T>::operator[](const int index) {
    return data[index]->val;
}

template<typename T>
Queue<T>::Queue() {
    data = LinkedList::SinglyLinkedList<T>();
    len = 0;
}

template<typename T>
T Queue<T>::dequeue() {
    if (len == 0) {
        throw std::invalid_argument("queue is empty");
    }

    T x = data[0]->val;
    data.remove_by_index(0);
    len--;
    return x;
}

template<typename T>
void Queue<T>::enqueue(T val) {
    len++;
    data.push_back(val);
}


template<typename T>
int Queue<T>::size() {
    return len;
}
