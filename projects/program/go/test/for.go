package test

import "fmt"

func ForTest() {
	s := "123"
	for i := 0; i < len(s); i++ {
		fmt.Println(s[i])
	}

	for i := 0; i < len(s); i++ {
		fmt.Printf("%d ", s[i])
	}
	fmt.Printf("\n")

	for _, v := range s {
		fmt.Printf("%d ", v)
	}
	fmt.Printf("\n")

	ch := '1'
	fmt.Println(ch)
}
