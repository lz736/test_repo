from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        # If the target is not found, 'left' will be the index
        # where the target should be inserted.
        return left

if __name__ == "__main__":
    s = Solution()
    nums = [1, 3, 5, 6]
    target = 5
    print(s.searchInsert(nums, target))  # 预期输出：2
    target = 2
    print(s.searchInsert(nums, target))  # 预期输出：1
    target = 7
    print(s.searchInsert(nums, target))  # 预期输出：4