"""
LeetCode Problem: Maximum Sum Subarray of Size K
BAD IMPLEMENTATION - Intentionally inefficient for testing
"""

def max_sum_subarray(nums, k):
    """
    BAD: O(n*k) time complexity - should be O(n)
    BAD: No input validation
    BAD: No error handling
    BAD: Inefficient nested loops
    """
    # BAD: No input validation
    # BAD: No check for empty array
    # BAD: No check for k > len(nums)
    
    max_sum = float('-inf')
    
    # BAD: Inefficient - recalculates sum for each window
    for i in range(len(nums) - k + 1):
        current_sum = 0
        # BAD: Nested loop causes O(n*k) complexity
        for j in range(i, i + k):
            current_sum += nums[j]
        
        if current_sum > max_sum:
            max_sum = current_sum
    
    # BAD: No error handling if max_sum is still -inf
    return max_sum


def max_sum_subarray_optimized(nums, k):
    """
    This is the correct implementation but it's not being used.
    The bad implementation above should be replaced with this.
    """
    if not nums or k <= 0 or k > len(nums):
        return 0
    
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum


# BAD: No test cases
# BAD: No main guard
if __name__ == "__main__":
    nums1 = [2, 1, 5, 1, 3, 2]
    k1 = 3
    result1 = max_sum_subarray(nums1, k1)
    print(f"Test 1: {result1}")
