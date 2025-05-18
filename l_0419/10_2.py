class Solution:
    def romanToInt(self, s: str) -> int:
        """
        将罗马数字字符串转换为对应的整数。

        Args:
            s: 表示罗马数字的字符串。

        Returns:
            对应的整数。
        """
        roman_map = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        
        total = 0
        n = len(s)
        
        # 从左到右遍历字符串
        for i in range(n):
            current_value = roman_map[s[i]]
            
            # 检查当前字符后面是否还有字符，并且当前字符的值是否小于下一个字符的值
            # 如果是，说明是特殊减法情况 (如 IV, IX, XL, XC, CD, CM)，则减去当前字符的值
            if i < n - 1 and current_value < roman_map[s[i+1]]:
                total -= current_value
            # 否则，是普通加法情况，则加上当前字符的值
            else:
                total += current_value
                
        return total

# 示例测试
sol = Solution()
print(sol.romanToInt("III"))       # 输出: 3
print(sol.romanToInt("IV"))        # 输出: 4
print(sol.romanToInt("IX"))        # 输出: 9
print(sol.romanToInt("LVIII"))     # 输出: 58
print(sol.romanToInt("MCMXCIV"))   # 输出: 1994