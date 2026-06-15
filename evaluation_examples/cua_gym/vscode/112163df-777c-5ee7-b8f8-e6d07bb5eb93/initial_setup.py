"""
Initial Setup: Prepare VSCode with C/C++ project files, no C/C++ extension installed.
Task ID: vscode_stu_027
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_027'
PROJECT_DIR = f'{WORKDIR}/systems_programming'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_project_files():
    """Create a realistic C/C++ project directory for a systems programming class."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # main.c - a simple linked list implementation
    main_c = '''\
#include <stdio.h>
#include <stdlib.h>
#include "linkedlist.h"

int main(int argc, char *argv[]) {
    Node *head = NULL;

    // Insert some values
    head = insert_front(head, 10);
    head = insert_front(head, 20);
    head = insert_front(head, 30);
    head = insert_end(head, 40);

    printf("Linked list contents:\\n");
    print_list(head);

    printf("List length: %d\\n", length(head));

    // Delete a node
    head = delete_node(head, 20);
    printf("After deleting 20:\\n");
    print_list(head);

    // Free all memory
    free_list(head);
    return 0;
}
'''

    linkedlist_h = '''\
#ifndef LINKEDLIST_H
#define LINKEDLIST_H

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node *insert_front(Node *head, int value);
Node *insert_end(Node *head, int value);
Node *delete_node(Node *head, int value);
void print_list(Node *head);
int length(Node *head);
void free_list(Node *head);

#endif /* LINKEDLIST_H */
'''

    linkedlist_c = '''\
#include <stdio.h>
#include <stdlib.h>
#include "linkedlist.h"

Node *insert_front(Node *head, int value) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (!new_node) {
        fprintf(stderr, "Memory allocation failed\\n");
        exit(EXIT_FAILURE);
    }
    new_node->data = value;
    new_node->next = head;
    return new_node;
}

Node *insert_end(Node *head, int value) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (!new_node) {
        fprintf(stderr, "Memory allocation failed\\n");
        exit(EXIT_FAILURE);
    }
    new_node->data = value;
    new_node->next = NULL;

    if (head == NULL) {
        return new_node;
    }

    Node *current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
    return head;
}

Node *delete_node(Node *head, int value) {
    if (head == NULL) return NULL;

    if (head->data == value) {
        Node *temp = head->next;
        free(head);
        return temp;
    }

    Node *current = head;
    while (current->next != NULL && current->next->data != value) {
        current = current->next;
    }

    if (current->next != NULL) {
        Node *temp = current->next;
        current->next = temp->next;
        free(temp);
    }

    return head;
}

void print_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\\n");
}

int length(Node *head) {
    int count = 0;
    Node *current = head;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    return count;
}

void free_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        Node *temp = current;
        current = current->next;
        free(temp);
    }
}
'''

    makefile = '''\
CC = gcc
CFLAGS = -Wall -Wextra -g -std=c11
TARGET = linkedlist_demo

SRCS = main.c linkedlist.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
\t$(CC) $(CFLAGS) -o $@ $^

%.o: %.c linkedlist.h
\t$(CC) $(CFLAGS) -c $< -o $@

clean:
\trm -f $(OBJS) $(TARGET)

.PHONY: all clean
'''

    with open(os.path.join(PROJECT_DIR, 'main.c'), 'w') as f:
        f.write(main_c)
    with open(os.path.join(PROJECT_DIR, 'linkedlist.h'), 'w') as f:
        f.write(linkedlist_h)
    with open(os.path.join(PROJECT_DIR, 'linkedlist.c'), 'w') as f:
        f.write(linkedlist_c)
    with open(os.path.join(PROJECT_DIR, 'Makefile'), 'w') as f:
        f.write(makefile)

    print(f'Project files created in {PROJECT_DIR}')


def ensure_extension_not_installed():
    """Make sure ms-vscode.cpptools is NOT installed."""
    result = subprocess.run(
        ['code', '--list-extensions'],
        capture_output=True, text=True
    )
    if 'ms-vscode.cpptools' in result.stdout:
        subprocess.run(
            ['code', '--uninstall-extension', 'ms-vscode.cpptools'],
            capture_output=True, text=True
        )
        print('Uninstalled ms-vscode.cpptools')
    else:
        print('ms-vscode.cpptools is not installed (good)')


def main():
    create_project_files()
    ensure_extension_not_installed()

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
