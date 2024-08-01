#pragma once

#include "linked_list.h"
#include <cstdint>


template<typename T>
class Stack {
private:
    int32_t size_;
    LinkedList::SinglyLinkedList<T> data;

public:
    Stack();

    int32_t size();

    T peek();

    void push(T);

    T pop();

    bool isEmpty();
};


template<typename T>
Stack<T>::Stack() {
    size_ = 0;
    data = LinkedList::SinglyLinkedList<T>();
}

template<typename T>
void Stack<T>::push(T val) {
    data.push_back(val);
    size_ += 1;

}

template<typename T>
T Stack<T>::peek() {
    if (isEmpty()) {
        throw std::invalid_argument("Stack is Empty");
    }
    return data[size_ - 1]->val;
}

template<typename T>
T Stack<T>::pop() {
    if (isEmpty()) {
        throw std::invalid_argument("Stack is Empty");
    }
    T el = data[--size_]->val;
    data.remove_by_index(size_);
    return el;
}

template<typename T>
int32_t Stack<T>::size() {
    return size_;
}

template<typename T>
bool Stack<T>::isEmpty() {
    return size_ == 0;
}
