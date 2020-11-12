# 首尾指针实现
# 链队 首尾指针实现链队
class Node():
    def __init__(self, value=None):
        self.value = value
        self.next = None

class StcakQueue():
    def __init__(self):
        self.front = Node()
        self.rear = Node()
        self.size = 0

    def enqueue(self, value):
        node = Node(value)
        if self.size == 0:
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise Exception('queue is empty')
        else:
            temp = self.front.value
            self.front = self.front.next
            self.size -= 1
            return temp

    def is_empty(self):
        if self.size == 0 :
            return False
        else:
            return True

    def top(self):
        if self.size == 0 :
            raise LookupError('queue is empty')
        else:
            return self.front.value

    def size(self):
        return self.size

    def __str__(self):
        if self.size == 0:
            return None
        else:
            stack_list = []
            temp, count = self.front, self.size
            while count > 0 :
                stack_list.append(temp.value)
                temp = temp.next
                count -= 1
            return str(stack_list)
