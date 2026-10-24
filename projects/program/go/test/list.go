package test

import (
	"fmt"
)

func PrintList(head *ListNode) {
	for head != nil {
		fmt.Printf("%d ", head.Val)
		head = head.Next
	}
	fmt.Printf("\n")
}

func MakeListV1(arr []int) *ListNode {
	if len(arr) == 0 {
		return nil
	}
	head := &ListNode{Val: arr[0]}
	tmp := head
	for i := 1; i < len(arr); i++ {
		tmp.Next = &ListNode{Val: arr[i]}
		tmp = tmp.Next
	}
	return head
}

func MakeListV2(arr []int) *ListNode {
	if len(arr) == 0 {
		return nil
	}
	head := new(ListNode)
	tmp := head
	for i := 0; i < len(arr)-1; i++ {
		tmp.Val = arr[i]
		tmp.Next = new(ListNode)
		tmp = tmp.Next
	}
	tmp.Val = arr[len(arr)-1]
	return head

}

func ReverseList(head *ListNode) *ListNode {
	if head == nil {
		return head
	}
	pre := head.Next
	head.Next = nil
	for pre != nil {
		//tmp := pre.Next
		//pre.Next = head
		//head = pre
		//pre = tmp
		pre, pre.Next, head = pre.Next, head, pre
	}
	return head
}

func DeleteDuplicates(head *ListNode) *ListNode {
	if head == nil {
		return head
	}
	fast := head
	slow := head
	for fast != nil {
		if slow.Val < fast.Val {
			slow.Next = fast
			slow = fast
		}
		fast = fast.Next
	}
	slow.Next = nil
	return head
}
