package main

import (
	"fmt"
	"sort"
)

type Node struct {
	x int
	y int
}

func main() {
	nums := []int{1, 3, 2, 4}
	fmt.Println(nums)
	sort.Ints(nums)
	fmt.Println(nums)

}

func threeSum(nums []int) [][]int {
	sort.Ints(nums)
	return [][]int{}

}
