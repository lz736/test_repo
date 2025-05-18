class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        """
        删除排序数组中的重复项，使每个元素只出现一次，并返回新的长度。
        要求原地修改数组，元素的相对顺序保持一致。

        Args:
            nums: 一个非严格递增排列的整数数组。

        Returns:
            删除重复项后数组的新长度。
        """
        if not nums:
            return 0

        # write_pointer 指向下一个不重复元素应该被写入的位置
        # 数组的第一个元素（如果存在）肯定是唯一的，所以 write_pointer 从 1 开始
        # （nums[0] 将是第一个唯一元素，nums[1] 将是下一个写入位置）
        write_pointer = 1

        # read_pointer 从数组的第二个元素开始遍历
        for read_pointer in range(1, len(nums)):
            # 如果当前读取的元素与前一个写入的唯一元素不同
            # (nums[write_pointer - 1] 是最后一个已确定的唯一元素)
            if nums[read_pointer] != nums[write_pointer - 1]:
                # 将这个新的唯一元素放到 write_pointer 指向的位置
                nums[write_pointer] = nums[read_pointer]
                # 移动 write_pointer 到下一个可写入位置
                write_pointer += 1
        
        # write_pointer 最终的值就是唯一元素的数量，也是新数组的长度
        return write_pointer
         
# 示例 1
nums1 = [1, 1, 2]
expectedNums1 = [1, 2]
solver = Solution()
k1 = solver.removeDuplicates(nums1)

print(f"输出: {k1}, nums = {nums1[:k1]}{['_'] * (len(expectedNums1) - k1) if k1 < len(expectedNums1) else ''}") 
assert k1 == len(expectedNums1)
for i in range(k1):
    assert nums1[i] == expectedNums1[i]
print("示例 1 通过")

# 示例 2
nums2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
expectedNums2 = [0, 1, 2, 3, 4]
k2 = solver.removeDuplicates(nums2)

print(f"输出: {k2}, nums = {nums2[:k2]}{['_'] * (len(expectedNums2) - k2) if k2 < len(expectedNums2) else ''}") 
assert k2 == len(expectedNums2)
for i in range(k2):
    assert nums2[i] == expectedNums2[i]
print("示例 2 通过")
