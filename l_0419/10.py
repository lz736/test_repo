class Solution:
    def isPalindrome(self, x: int) -> bool:
        """
        检查一个整数是否是回文数。

        如果 x 是回文整数，返回 true ；否则，返回 false 。
        回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
        例如，121 是回文，而 123 不是。

        Args:
            x: 输入的整数。

        Returns:
            如果 x 是回文数，返回 True；否则返回 False。
        """
        # 负数不是回文数，因为有负号
        if x < 0:
            return False

        # 将整数转换为字符串
        s = str(x)

        # 检查字符串是否与其反转相同
        return s == s[::-1]

# 示例用法：
solution = Solution()

# 示例 1
x1 = 121
print(f"Input: x = {x1}")
print(f"Output: {solution.isPalindrome(x1)}") # 预期输出: True

# 示例 2
x2 = -121
print(f"Input: x = {x2}")
print(f"Output: {solution.isPalindrome(x2)}") # 预期输出: False

# 示例 3
x3 = 10
print(f"Input: x = {x3}")
print(f"Output: {solution.isPalindrome(x3)}") # 预期输出: False

# 示例 4
x4 = 0
print(f"Input: x = {x4}")
print(f"Output: {solution.isPalindrome(x4)}") # 预期输出: True
