#pragma once

#include <iostream>
#include <cstdint>


namespace LinkedList {
    // Node represents simple node for singly-linked list
    // has value and a pointer to a next Node
    template<typename T>
    class Node {
    public:
        T val;
        Node<T> *next;

        explicit Node<T>(T _val) : val(_val), next(nullptr) {}
    };

    template<typename T>
    class SinglyLinkedList {
    private:
        Node<T> *first;
        Node<T> *last;

        // length contains current length of a list
        int32_t length;

        // remove first element by index and change head
        void remove_first();

        // remove last element by index and change tail
        void remove_last();

    public:
        // default constructor creates empty list
        SinglyLinkedList();

        // check if list has at least 1 element
        bool is_empty();

        void push_by_index(int32_t index, T val);

        void push_back(T val);

        void push_front(T val);

        Node<T> *operator[](int index);

        void remove_by_value(T val);

        void remove_by_index(int32_t index);

        Node<T> *find_by_value(T val);
    };
}

template<typename T>
void LinkedList::SinglyLinkedList<T>::remove_first() {
    if (is_empty()) return;
    LinkedList::Node<T> *p = first;
    first = p->next;
    delete p;
}

template<typename T>
void LinkedList::SinglyLinkedList<T>::remove_last() {
    if (is_empty()) return;
    if (first == last) {
        remove_first();
        return;
    }
    LinkedList::Node<T> *p = first;
    while (p->next != last) p = p->next;
    p->next = nullptr;
    delete last;
    last = p;
}

template<typename T>
LinkedList::SinglyLinkedList<T>::SinglyLinkedList() : first(nullptr), last(nullptr), length(0) {}

template<typename T>
bool LinkedList::SinglyLinkedList<T>::is_empty() {
    return first == nullptr;
}

template<typename T>
void LinkedList::SinglyLinkedList<T>::push_by_index(const int32_t index, const T val) {
    LinkedList::Node<T> *n = new Node(val);
    LinkedList::Node<T> *p = first;
    for (int32_t i = 0; i < index; i++) {
        p = p->next;
        if (!p) {
            return;
        }
    }

    n->next = p->next;
    p->next = n;

}

// push after the last element
template<typename T>
void LinkedList::SinglyLinkedList<T>::push_back(const T val) {
    LinkedList::Node<T> *n = new Node(val);

    if (is_empty()) {
        first = n;
        last = n;
        length++;
        return;
    }

    last->next = n;
    last = last->next;
    length++;
}

// push before the first element
template<typename T>
void LinkedList::SinglyLinkedList<T>::push_front(const T val) {
    LinkedList::Node<T> *n = new Node(val);
    if (is_empty()) {
        first = n;
        last = n;
        length++;
        return;
    }
    LinkedList::Node<T> *tmp = first;
    first = n;
    first->next = tmp;
    length++;
}

// overriding this operator allows you to get elements by index
template<typename T>
LinkedList::Node<T> *LinkedList::SinglyLinkedList<T>::operator[](const int index) {
    if (is_empty()) return nullptr;
    LinkedList::Node<T> *p = first;
    for (int i = 0; i < index; i++) {
        p = p->next;
        if (!p) return nullptr;
    }
    return p;
}


// removes all occurrences of a value
template<typename T>
void LinkedList::SinglyLinkedList<T>::remove_by_value(const T val) {
    if (is_empty()) return;
    while (first->val == val) {
        remove_first();
        length--;
    }

    while (last->val == val) {
        remove_last();
        length--;
    }

    LinkedList::Node<T> *slow = first;
    LinkedList::Node<T> *fast = first->next;
    while (fast) {
        if (fast->val == val) {
            slow->next = fast->next;
            length--;
        }
        fast = fast->next;
        slow = slow->next;
    }
    delete slow;
    delete fast;
}

// removes element by index
template<typename T>
void LinkedList::SinglyLinkedList<T>::remove_by_index(const int32_t index) {
    if (is_empty()) return;
    if (index == 0) {
        first = first->next;
        if (length == 1) {
            last = nullptr;
        }
        length--;
        return;
    }

    LinkedList::Node<T> *p = first;
    for (int32_t i = 0; i < index - 1; i++) {
        p = p->next;
        if (!p) return;
    }
    if (p->next == last) {
        last = p;
    }
    p->next = p->next->next;
    length--;

}

// finds first occurrence of element by value
template<typename T>
LinkedList::Node<T> *LinkedList::SinglyLinkedList<T>::find_by_value(const T val) {
    if (is_empty()) return nullptr;
    LinkedList::Node<T> *p = first;
    while (p) {
        if (p->val == val) {
            return p;
        }
        p = p->next;
    }
    return nullptr;
}
