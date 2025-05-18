class Solution:
    def isValid(self, s: str) -> bool:
        """
        判断给定的字符串是否为有效的括号序列。

        Args:
            s: 只包含 '(', ')', '{', '}', '[', ']' 的字符串。

        Returns:
            如果字符串有效则返回 True，否则返回 False。
        """
        stack = []  # 使用列表作为栈
        mapping = {")": "(", "}": "{", "]": "["} # 括号映射关系

        for char in s:
            # 如果是左括号，则入栈
            if char in mapping.values():
                stack.append(char)
            # 如果是右括号
            elif char in mapping.keys():
                # 检查栈是否为空，或者栈顶元素是否与当前右括号匹配
                if not stack or mapping[char] != stack.pop():
                    return False
            # 其他无效字符（题目说明只有括号，但为健壮性可保留）
            # else:
            #     return False # 或者忽略

        # 如果栈为空，说明所有括号都已正确匹配
        return not stack 

solver = Solution()
s1 = "()"
result1 = solver.isValid(s1)
print(f"输入：s = \"{s1}\"")
print(f"输出：{str(result1).lower()}") # .lower()确保输出 true/false 而不是 True/False
#示例2
s2 = "()[]{}"
result2 = solver.isValid(s2)
print(f"输入：s = \"{s2}\"")
print(f"输出：{str(result2).lower()}")
#示例3
s3 = "(]"
result3 = solver.isValid(s3)
print(f"输入：s = \"{s3}\"")
print(f"输出：{str(result3).lower()}")
#示例4
s4 = "([])"
result4 = solver.isValid(s4)
print(f"输入：s = \"{s4}\"")
print(f"输出：{str(result4).lower()}")