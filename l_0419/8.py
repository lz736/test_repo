def twoSum(nums, target):
    num_dict = {}  # 存储数字和其索引的字典
    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return [num_dict[complement], index]
            num_dict[num] = index

# 测试用例
if __name__ == "__main__":
    # 示例 1
    assert twoSum([2, 7, 11, 15], 9) == [0, 1], "示例 1 失败"
    
    # 示例 2
    assert twoSum([3, 2, 4], 6) == [1, 2], "示例 2 失败"
    
    # 示例 3（重复元素）
    assert twoSum([2, 4], 6) == [0, 1], "示例 3 失败"
    
    # 其他测试情况
    assert twoSum([5, 3, 4], 8) == [1, 2], "测试情况 1 失败"
    assert twoSum([-1, 5, 6], 5) == [0, 1], "测试情况 2（负数）失败"
    assert twoSum([1, 2, 3, 4, 5], 9) == [3, 4], "测试情况 3（解在末尾）失败"
    assert twoSum([10, 20, 30, 40], 70) == [2, 3], "测试情况 4（大数）失败"

    print("所有测试用例通过！🎉")