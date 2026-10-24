package test

import (
	"fmt"
	"strconv"
)

func IntTest() {
	a := '1'
	b := "1"
	c := b[0]
	d := 1
	fmt.Println(a, b, c, d)
	fmt.Printf("%T %T %T %T \n", a, b, c, d)

	fmt.Println('1' - '0')
	fmt.Printf("%T", '1'-'0')
}

func ConvertTest() {
	a := "0"
	b, _ := strconv.Atoi(a)
	fmt.Println(a, b)
}

func SliceTest() {
	var tmp1 []int
	tmp2 := make([]int, 10)
	tmp3 := make([][]int, 4)
	fmt.Println(len(tmp1), len(tmp2), len(tmp3))

	fmt.Printf("%p\t %d\n", &tmp2, len(tmp2))
	tmp2 = append(tmp2, 1)
	fmt.Printf("%p\t %d\n", &tmp2, len(tmp2))
}

func BigIntAdd(a, b string) string {
	return ""
}
