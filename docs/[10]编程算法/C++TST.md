参考链接：
STL教程:C++ STL快速入门(非常详细)
数据类型
基础类型
1. 整型：short, int, long
2. 浮点型: float, double
3. 布尔型：bool
4. 字符型：char
5. 指针型： type * 
数组
1. 声明：int arr[size]
2. 获取长度：size()
#include <iostream>
using namespace std;

int main(){
    int arr[3] = {1,2,3};
    cout<<sizeof(arr)/sizeof(int)<<endl;
    for (int i=0; i<3; i++){
        cout<<arr[i]<<' ';
    }
    cout<<endl;
}
字符串
1. 长度：size();
2. 添加元素：push_back();
3. 删除元素：pop_back()
#include<iostream>
using namespace std;

int main(){
    string s = "hello World";
    cout<<sizeof(s)<<endl;
    cout<<s.length()<<endl;
    return 0;
}
结构体
#include <iostream>
using namespace std;

struct Node {
    int x;
    int y;
};

struct ListNode {
    int val;
    ListNode *next;
};

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
};

int main() {
    ListNode head = {0,NULL};
    head.next = new(ListNode){1,NULL};
    cout << head.val << ' ' << head.next << endl;
    cout << head.next->val << ' ' << head.next->next << endl;
    return 0;
}
控制流程
输入输出
#include<iostream>
using namespace std;
int main(){
    int x;
    cin>>x;
    cout<<x<<endl;

    double y;
    scanf("%lf",&y);
    printf("%f", y)
    printf("%.3f", y)
}
分支
if (x>y){
    cout<<"bigger"<<endl;
} else if(x==y){
    cout<<"equal"<<endl;
} else {
    count<<"less"<<endl;
}
循环
for(int i=0; i<n; i++){
    cout<<nums[i]<<' '<<endl;
}
count<<endl;
容器(container)


数组(array)
1. 特点：固定连续空间
2. 声明：array<int, N> values，包含N个int元素的数组，并初始化为0，注意N为常数；
3. 元素个数：size()
4. 是否为空：empty()
5. 正序头部：begin()
6. 倒序头部：rbegin()
#include<iostream>
#include<array>
using namespace std;

int main() {
    array<int, 4> nums = {1, 2, 3, 4};
    cout << nums.size() << endl;
    if (!nums.empty()) {
        for (auto it = nums.begin(); it != nums.end(); it++) {
            cout << *it << ' ';
        }
        cout << endl;
    }
    if (!nums.empty()) {
        for (auto it = nums.rbegin(); it != nums.rend(); it++) {
            cout << *it << ' ';
        }
        cout << endl;
    }

    if (!nums.empty()) {
        for (auto val = nums.begin(); val < nums.end(); val++) {
            cout << *val << ' ';
        }
        cout << endl;
    }
    if (!nums.empty()) {
        for (auto val = nums.rbegin(); val < nums.rend(); val++) {
            cout << *val << ' ';
        }
        cout << endl;
    }
    return 0;
}
向量(vector)
1. 特点：单向开口的连续线性空间
2. 声明：vector<int> vec, vector<int> vec(N), vector<int> vec(N, v)
#include<iostream>
#include<vector>
using namespace std;
int main(){
    int m=3;
    int n= 4;
    vector<int> v1;
    vector<int> v2(10);
    vector<int> v3(10, 1);
    vector<vector<int>> v4(m,vector<int>(n));
    for(int i=0; i<m; i++){
        for(int j=0; j<n; j++){
            cout<<v4[i][j]<<' ';
        }
        cout<<endl;
    }
    v1.push_back(0);
    cout<<v1[0]<<endl;
    v1.pop_back();
    cout<<v1.size()<<' '<<v1.at(0)<<endl;
    v1.insert(v1.begin(),1);
    cout<<v1[0]<<endl;
    v1.erase(v1.begin());
    cout<<v1.size()<<endl;
    for(auto i=v1.begin(); i<v1.end(); i++){
        cout<<*i<<' ';
    }
    cout<<endl;
    return 0;
}

双端队列(dequeue)
1. 特点：双端开口的连续线性空间
2. 声明：deque<int> dque
3. 元素操作：back(), front(), push_back(), pop_back(), push_front(), pop_front();
#include<iostream>
#include<deque>
using namespace std;

int main() {
    deque<int> que;
    que.push_back(1);
    que.push_back(2);
    que.push_front(1);
    que.push_front(3);

    while (!que.empty()) {
        cout << que.front() << ' ';
        que.pop_front();
    }
    cout<<endl;
    return 0;
}

链表(list)
1. 特点：双向操作
2. 声明：list<int> 
3. 元素操作：push_front, pop_front, push_back, pop_back, reverse, merge, sort
#include<iostream>
#include<list>
using namespace std;

int main() {
    list<int> nums;
    nums.push_front(2);
    nums.push_back(1);
    for (auto it = nums.begin(); it != nums.end(); it++) {
        cout << *it << ' ';
    }
    cout << endl << nums.size() << endl;
    nums.sort();
    for (auto it = nums.begin(); it != nums.end(); it++) {
        cout << *it << ' ';
    }
    cout << endl;
    return 0;
}
栈(stack)
1. 特点：先入后出，以list作为底层容器
2. 声明：stack<int> sta
3. 操作：size, empty, push, pop, top
#include<iostream>
#include<stack>
using namespace std;
int main(){
    stack<int> sta;
    sta.push(1);
    sta.push(2);
    cout<<sta.size()<<endl;
    while(!sta.empty()){
        cout<<sta.top()<<' ';
        sta.pop();
    }
    cout<<endl;
    return 0;
}
队列(queue)
1. 特点：先入先出，以list作为底层容器
2. 声明：queue<int> que
3. 操作：size, empty, push, pop, back, front
#include<iostream>
#include<queue>
using namespace std;
int main(){
    queue<int> que;
    que.push(1);
    que.push(2);
    cout<<que.size()<<endl;
    while(!que.empty()){
        cout<<que.front()<<' ';
        que.pop();
    }
    cout<<endl;
    return 0;
}
优先队列(priority_queue)
1. 特点：以vector作为底层容器;
2. 声明：priority_queue<int> ipq;
3. 操作：size, empty, push, pop, top
#include<iostream>
#include<queue>
using namespace std;
struct cmp{
    bool operator() (int x, int y){
        return x>y;
    }
};
int main(){
   int ia[9] = {0, 1, 2, 3, 4,5,6, 7, 8};
    priority_queue<int> ipq_min(ia, ia+9);
    priority_queue<int, vector<int>, cmp> ipq_max(ia, ia+9);
    for(int i=0; i<ipq_min.size(); i++){
        cout<<ipq_min.top()<<' ';
    }
    cout<<endl;
    while(!ipq_min.empty()){
        cout<<ipq_min.top()<<' ';
        ipq_min.pop();
    }
    cout<<endl;
    for(int i=0; i<ipq_max.size(); i++){
        cout<<ipq_max.top()<<' ';
    }
    cout<<endl;
    while(!ipq_max.empty()){
        cout<<ipq_max.top()<<' ';
        ipq_max.pop();
    }
    cout<<endl;
    return 0;
}
集合(set)
1. 特点：所有元素都会根据元素的键值自动排序，而set中键值(key)就是实值(value)；
2. 声明：set<int> is;
3. 元素操作：size(), empty(), insert(), erase(), clear();
#include<iostream>
#include<set>
using namespace std;

int main() {
    set<int> is;
    is.insert(3);
    is.insert(1);
    is.insert(2);
    is.insert(4);
    is.erase(2);
    for (auto it = is.begin(); it != is.end(); it++) {
        cout << *it << ' ';
    }
    cout << endl;
    return 0;
}
映射(map)
1. 特点：所有元素都会根据键值自动排序，所有元素都是pair，同时包括实值(value)和键指(key)；
2. 声明：map<int, int> im;
3. 元素操作：size(), empty(), begin(), end();
#include<iostream>
#include<map>
using namespace std;

int main() {
    map<int, int> im;
    im[0] = 0;
    im[2] = 2;
    im[1] = 1;
    cout << im[0] << endl;
    cout << im.size() << endl;
    for (auto it = im.begin(); it != im.end(); it++) {
        cout << it->first << ' ' << it->second << endl;
    }
    cout << endl;

    // 判断是否包含key
    cout << (im.find(3) == im.end()) << endl;
    return 0;
}
常用算法
排序(sort)
#include<iostream>
#include<algorithm>
using namespace std;

bool cmp(int x, int y) {
    return x > y;
}

void print_arr(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

void print_vector(vector<int> vec) {
    for (auto x: vec) {
        cout << x << " ";
    }
    cout << endl;
}

int main() {
    int arr[5] = {1, 3, 4};
    print_arr(arr, 5);
    sort(arr, arr + 5);
    print_arr(arr, 5);
    sort(arr, arr + 5, cmp);
    print_arr(arr, 5);

    vector<int> nums = {3, 1, 4, 0, 0};
    print_vector(nums);
    sort(nums.begin(), nums.end());
    print_vector(nums);
    sort(nums.begin(), nums.end(), cmp);
    print_vector(nums);
    return 0;
}
最大值(max)
#include<iostream>
#include<algorithm>
using namespace std;

int main() {
    cout << min(0, 1) << endl;
    cout << min(1.5, 0.5) << endl;
    return 0;
}
最小值(min)
#include<iostream>
#include<algorithm>
using namespace std;

int main() {
    cout << min(0, 1) << endl;
    cout << min(1.5, 0.5) << endl;
    return 0;
}
绝对值(abs)
#include<math.h>
#include<iostream>
using namespace std;

int main() {
    cout << abs(-1) << endl;
    cout << abs(-1.5) << endl;
    return 0;
}
类和对象
1. 声明&调用
#include <iostream>
using namespace std;

class Student {
public:
    string name;
    string get_name();
};

string Student::get_name() {
    return this->name;
};

int main() {
    Student std1 ={"xiaohong"};
    cout << std1.name << endl;
    cout << std1.get_name() << endl;
    return 0;
}
