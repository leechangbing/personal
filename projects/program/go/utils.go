package main

type ListNode struct {
	Val  int
	Next *ListNode
}

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func max(x, y int) int {
	if x > y {
		return x
	} else {
		return y
	}
}

func min(x, y int) int {
	if x < y {
		return x
	} else {
		return y
	}
}

func abs(x int) int {
	if x < 0 {
		return -x
	} else {
		return x
	}
}

func isalnum(ch byte) bool {
	return (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9')
}

func fastSort(nums []int, left int, right int) {
	if right-left <= 1 {
		return
	} else if right-left == 2 {
		if nums[left] > nums[right-1] {
			nums[left], nums[right-1] = nums[right-1], nums[left]
			return
		}
	}

	i, j, flag := left, right, nums[left]
	for i < j {
		for i < j && nums[i] <= flag {
			i++
		}
		for i < j && nums[j-1] > flag {
			j--
		}
		if i < j {
			nums[i], nums[j-1] = nums[j-1], nums[i]
			i++
			j--
		}
	}
	fastSort(nums, left, i)
	fastSort(nums, i, right)
}
