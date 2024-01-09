# 最经典二分查找思路，定义左边右边 index，然后取中间，然后继续查找 2分
# 前提条件就是 这个数组是有顺序的，从小到大，从大到小

class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right - left) // 2 + left
            num = nums[mid]
            if num == target:
                return mid
            elif target > num:
                left = mid + 1
            else:
                right = mid - 1
        return -1
