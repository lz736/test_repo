class Solution:
    def romanToInt(self, s: str) -> int:
        """
        将罗马数字转换为对应的整数

        Args:
            s: 表示罗马数字的字符串

        Returns:
            转换后的整数.
        """
        # 建立罗马数字符号与其对应整数数值的映射字典
        roman_map = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        } 

        result = 0
        n = len(s)

         # 遍历罗马数字字符串
        for i in range(n):
        # 获取当前字符的值
            current_value = roman_map[s[i]]

        # 检查是否存在下一个字符，并且当前字符的值小于下一个字符的值
        # 如果满足条件，说明是“左减”的情况，当前值应该被减去
            if i + 1 < n and current_value < roman_map[s[i+1]]:
                result -= current_value
            else:
            # 否则，是“右加”或最后一个字符的情况，当前值应该被加上
                result += current_value

        return result
    # 创建 Solution 类的实例
solution_instance = Solution()

#事例一
print(f"III 转换为整数是: {solution_instance.romanToInt('III')}")   #输出 = 3
#事例二
print(f"IV 转换为整数是: {solution_instance.romanToInt('IV')}")   #输出 = 4
#事例三
print(f"IX 转换为整数是: {solution_instance.romanToInt('IX')}")   #输出 = 9
#事例四
print(f"LVIII 转换为整数是: {solution_instance.romanToInt('LVIII')}")   #输出 = 58
#事例五
print(f"MCMXCIV 转换为整数是: {solution_instance.romanToInt('MCMXCIV')}")   #输出 = 1994