1. 常见问题
1. make函数 与 new函数有什么区别？  make()：type必须是slice, map, or channel
2. 数据类型
2.1 变量(variable)
1. 基础类型
  1. 有符号整型：int int8 int16 int32 int64 rune，其中rune是int32的别名
  2. 无符号整型：uint uint8 uint16 uint32 uint64 byte，其中byte是uint8的别名
  3. 浮点型：float32 float64
  4. 字符串：string 
  5. 布尔型：bool
2. 声明方式
  1. 标准方式：var name type
  2. 简单格式：name := 表达式，name1, name2 := 表达式1， 表达式2
3. 初始化
  1. 默认初始化：整型和浮点型为0和0.0，布尔值为false，字符串为""，切片、指针变量、函数为nil
  2. 手动初始化：var a int = 0, var b float32 = 0.0
4. 赋值
  1. 单变量赋值：a = 0
  2. 多变量赋值：a, b = 1, 2
5. 类型转换
  1. 显式声明：a := 1, b := 2.0, a = int(b)
  2. 相同底层类型的变量可以转换，否则会出错
2.2 指针(point)
1. 声明方式：var a *int, b := 1, c := &b
2. 初始化：默认为nil
3. 赋值： a := &b
4. 取值： fmt.Println(*a)
5. 备注：取地址符号&，取值符号*
3. 容器(container)
数组：数组
映射：映射
栈：列表
队列：列表
优先队列：堆
3.1 数组(array)
1. 声明：var a [10]int, var a [10][10]int
2. 初始化：为基础数据类型的默认值
3. 长度：len(arr)
4. 是否相等：==
5. 数组遍历：
for k, v := range(arr){
    fmt.Println(k, v)
}
for _, x := range(arr){
    fmt.Println(x)
}
for i:=0; i<len(arr); i++{
    fmt.Println(arr[i])
}
3.2 切片(slice)
1. 声明：var arr []int, var arr [][]int
2. 长度：len()
3. 初始化：默认为基础类型的默认值
4. 构造函数
m, n := 3, 3
// 一维切片
arr := make([]int, m)
// 二维切片
arr := make([][]int, m)
for i := 0; i < m; i++ {
    arr[i] = make([]int, n)
}
5. 新增元素
arr = append(arr, element)
arr = append(arr, arr_2...)
6. 删除元素
// 从头删除,包含idx
arr[idx:]
// 从尾部删除，不包含idx
arr[:idx]
// 从中间删除，idx个元素
append(arr[:idx], arr[idx+1:]...)
// 清除全部元素
arr[0:0]
7. 元素遍历
for k, v := range(arr){
    fmt.Println(k, v)
}
for _, x := range(arr){
    fmt.Println(x)
}
for i:=0; i<len(arr); i++{
    fmt.Println(arr[i])
}
3.3 映射(map)
1. 声明：var m map[string]int
2. 长度：len()
3. 创建map：dict := make(map[int]int)
4. 删除元素：delect(dict, 1)
5. 新增元素：dict[1] = 2
6. 判断key是否存在
val, ok := dict[1]
if ok {
    fmt.Println(val)
} else {
    fmt.Println("不存在")
}
7. 遍历元素：
for k,v := range(dict){
    fmt.Println(k, v)
}
for k := range(dict){
    fmt.Println(k)
 }
 for _, v:= range(dict){
     fmt.Println(v)
 }
3.4 列表(container/list)
1. 声明：tmp := list.new()
2. 列表长度：tmp.Len()
3. 插入元素：tmp.PushBack(), tmp.PushFront()
4. 删除元素：tmp.Remove(tmp.Front()) tmp.Remove(tmp.Back())
5. 头部元素：tmp.Front()
6. 尾部元素：tmp.Back()
7. 遍历元素：
import "container/list"
// 正向遍历
for t:=tmp.Front(); t!=nil; t=t.Next(){
    fmt.Println(t.Val())
}
// 反向遍历
for t:=tmp.Back(); t!=nil; t=t.Prev(){
    fmt.Println(t.Val())
}
3.5 环(container/ring)
1. 声明：tmp = ring.New()
2. 环长度：tmp.Len()
3. 下一个元素：tmp.Next()
4. 上一个元素：tmp.Preve()
3.6 堆(container/heap)
1. 声明：heap.Init()
2. 接口函数：Len(), Less(), Swap(), Pop(), Push()
4. 控制流程
4.1 分支结构(if else)
if condition {
    //
}
if condition {
    //...
} else {
    //...
}
 
if condition1 {
    // ...
} else if condition2{
    // ...
}
4.2 循环结构(for)
基础元素：初始语句，条件表达式，结束语句
for i:=0; i<n; i++{
    //...
}
for i<n {
    i++
}
for x:=range(arr){
    //...
}
5. 函数(function)
基础元素：关键字，函数名，参数列表，返回值，函数体，返回语句
func max(x, y int) int{
    if x>y {
        return x
    } else {
        return y
    }
}
func max(x, y int) (z int){
    if x>y {
        z = x
    } else {
        z = y
    }
    return z 
}
6. 结构体(struct)
1. 声明方式
type ListNode struct{
    Val  int
    Next *ListNode
}
1. 实例化方式
head := new(ListNode)
head :=  &ListNode{Val: 2}
head := ListNode{Val: 2}
