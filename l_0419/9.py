# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        将两个逆序存储的非负整数链表相加，并返回结果链表。

        Args:
            l1: 第一个非负整数链表（逆序存储）。
            l2: 第二个非负整数链表（逆序存储）。

        Returns:
            表示两个数之和的链表（逆序存储）。
        """
        dummy_head = ListNode(0)  # 创建一个虚拟头节点
        current = dummy_head      # 当前节点指针
        carry = 0                 # 进位

        while l1 or l2 or carry:
            # 获取当前节点的值，如果链表已耗尽则取 0
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # 计算当前位的和以及进位
            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            # 创建新的节点并添加到结果链表
            current.next = ListNode(digit)
            current = current.next

            # 移动到下一个节点（如果存在）
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy_head.next  # 返回结果链表的头节点（跳过虚拟头节点）

# Helper function to create a linked list from a list of integers
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper function to convert a linked list to a list of integers
def linked_list_to_list(head):
    arr = []
    current = head
    while current:
        arr.append(current.val)
        current = current.next
    return arr

# 示例用法
# 示例 1
l1 = create_linked_list([2, 4, 3])
l2 = create_linked_list([5, 6, 4])
solution = Solution()
result = solution.addTwoNumbers(l1, l2)
print(f"示例 1 输入: l1 = [2,4,3], l2 = [5,6,4]")
print(f"示例 1 输出: {linked_list_to_list(result)}") # 预期输出: [7, 0, 8]

# 示例 2
l1 = create_linked_list([0])
l2 = create_linked_list([0])
solution = Solution()
result = solution.addTwoNumbers(l1, l2)
print(f"\n示例 2 输入: l1 = [0], l2 = [0]")
print(f"示例 2 输出: {linked_list_to_list(result)}") # 预期输出: [0]

# 示例 3
l1 = create_linked_list([9, 9, 9, 9, 9, 9, 9])
l2 = create_linked_list([9, 9, 9, 9])
solution = Solution()
result = solution.addTwoNumbers(l1, l2)
print(f"\n示例 3 输入: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]")
print(f"示例 3 输出: {linked_list_to_list(result)}") # 预期输出: [8, 9, 9, 9, 0, 0, 0, 1]