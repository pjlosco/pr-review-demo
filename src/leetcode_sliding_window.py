"""
LeetCode Problem: Maximum Sum Subarray of Size K

Given an array of integers and a number k, find the maximum sum of any contiguous subarray of size k.

Example:
Input: nums = [2, 1, 5, 1, 3, 2], k = 3
Output: 9
Explanation: Subarray [5, 1, 3] has the maximum sum of 9.
"""

def max_sum_subarray(nums, k):
    """
    Find maximum sum of subarray of size k.
    
    This solution works but is inefficient - it recalculates sums
    for overlapping windows instead of using the sliding window technique.
    
    Time Complexity: O(n * k) - inefficient!
    Space Complexity: O(1)
    
    Args:
        nums: List of integers
        k: Size of subarray
        
    Returns:
        Maximum sum of any subarray of size k
    """
    if not nums or k <= 0 or k > len(nums):
        return 0
    
    max_sum = float('-inf')
    
    # Go through each possible starting position
    for i in range(len(nums) - k + 1):
        # Calculate sum for this window from scratch
        current_sum = 0
        for j in range(i, i + k):
            current_sum += nums[j]
        
        # Update max if this sum is larger
        if current_sum > max_sum:
            max_sum = current_sum
    
    return max_sum


def max_sum_subarray_optimized(nums, k):
    """
    Optimized version using sliding window technique.
    
    This is the correct approach - we maintain a running sum
    and slide the window by subtracting the left element and
    adding the right element.
    
    Time Complexity: O(n) - much better!
    Space Complexity: O(1)
    """
    if not nums or k <= 0 or k > len(nums):
        return 0
    
    # Calculate sum of first window
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(nums)):
        # Remove leftmost element, add rightmost element
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum


# Test cases
if __name__ == "__main__":
    # Test case 1
    nums1 = [2, 1, 5, 1, 3, 2]
    k1 = 3
    result1 = max_sum_subarray(nums1, k1)
    print(f"Test 1: {result1} (expected: 9)")
    
    # Test case 2
    nums2 = [1, 4, 2, 10, 23, 3, 1, 0, 20]
    k2 = 4
    result2 = max_sum_subarray(nums2, k2)
    print(f"Test 2: {result2} (expected: 39)")

