#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct ListNode{
    int val;
    ListNode* next;
//    ListNode(): val(0), next(nullptr) {};
//    ListNode(int x): val(x), next(nullptr) {};
//    ListNode(int x, ListNode *next): val(x), next(next) {};
};

ListNode* makeList(vector<int> &nums){
    int n = nums.size();
    if(n==0){
        return nullptr;
    }

    ListNode *head=new(ListNode){val:nums[0], next:nullptr};
    ListNode *tmp = head;
    for(int i=1; i<n; i++){
        tmp->next = new(ListNode){val:nums[i], next:nullptr};
        tmp = tmp->next;
    }
    return head;
}

ListNode* reverseList(ListNode* head){
    if(head==nullptr){
        return head;
    }
    ListNode* next = head->next;
    head->next = nullptr;
    while(next != nullptr){
        ListNode *tmp = next->next;
        next->next = head;
        head = next;
        next = tmp;
    }
    return head;
}

ListNode* deleteKNode(ListNode *head, int k){
    if (k==1) return head->next;
    ListNode *curr = head;
    for(int i=1; i<k-1; i++){
        curr = curr->next;
    }
    curr->next = curr->next->next;
    return head;
}

ListNode* deleteRKNode(ListNode* head, int k){
    ListNode *fast = head, *slow=head;
    for(int i=1; i<=k; i++){
        fast = fast->next;
    }
    if(fast== nullptr) return head->next;

    while(fast->next != nullptr){
        fast = fast->next;
        slow = slow->next;
    }
    slow->next = slow->next->next;
    return head;
}

ListNode* rotateRight(ListNode* head, int k) {
    ListNode *fast=head, *slow=head, *res;
    for(int i=1; i<=k; i++){
        fast = fast->next;
    }
    while(fast->next){
        fast = fast->next;
        slow = slow->next;
    }
    res = slow->next;
    fast->next = head;
    slow->next = nullptr;
    return res;
};

ListNode* deleteDuplicates(ListNode* head) {
    if(head== nullptr) return head;
    ListNode *fast=head->next, *slow=head;
    while(fast){
        if(fast->val != slow->val){
            slow->next = fast;
            slow = fast;
        }
        fast = fast->next;
    }
    slow->next = nullptr;
    return head;
}

ListNode* partition(ListNode* head, int x) {
    ListNode *lessHead = new(ListNode);
    ListNode *bigHead = new(ListNode);
    ListNode *equalHead = new(ListNode);
    ListNode *less= lessHead;
    ListNode *big = bigHead;
    ListNode *equal = equalHead;

    while(head){
        if(head->val == x){
            equal->next = head;
            equal = head;
        }else if(head->val > x){
            big->next = head;
            big = head;
        }else if(head->val < x){
            less->next = head;
            less = head;
        }
        head = head->next;
    }

    less->next = equalHead->next;
    equal->next = bigHead->next;
    return lessHead->next;
}

bool isCycle(ListNode *head){
    if(head== nullptr){
        return false;
    }
    ListNode *fast = head,  *slow = head;
    while(fast && fast->next){
        fast = fast->next->next;
        slow = slow->next;
        if (fast==slow){
            return true;
        }
    }
    return false;
}

ListNode* mergeList(ListNode *head1, ListNode* head2) {
    ListNode *tmp = new(ListNode){val:0, next:nullptr};
    ListNode *res = tmp;

    while(head1 && head2){
        if(head1->val<head2->val){
            tmp->next = head1;
            head1 = head1->next;
        } else {
            tmp->next = head2;
            head2 = head2->next;
        }
    }
    if(head1){
        tmp->next = head1;
    }
    if(head2){
        tmp->next = head2;
    }
    return res->next;
}

ListNode *sortList(ListNode * head) {
    if (head == nullptr || head->next == nullptr) {
        return head;
    }
    if (head->next->next == nullptr) {
        if (head->val > head->next->val) {
            ListNode *tmp = head->next;
            head->next->next = head;
            head->next = tmp;
            return tmp;
        } else {
            return head;
        }
    }
    ListNode *fast = head, *slow = head;
    while (fast && fast->next) {
        fast = fast->next->next;
        slow = slow->next;
    }
    ListNode *head2 = slow->next;
    slow->next = nullptr;

    return mergeList(head, sortList(head2));
}

void printList(ListNode* head){
    while(head != nullptr){
        cout<<head->val<<' ';
        head = head->next;
    }
    cout<<endl;
}


void listTest() {
    vector<int> nums = {1,2,4,3, 3,5,6};
    printList(makeList(nums));
    printList(reverseList(makeList(nums)));
    printList(deleteKNode(makeList(nums), 5));
    printList(deleteRKNode(makeList(nums), 2));
    printList(rotateRight(makeList(nums), 2));
    printList(deleteDuplicates(makeList(nums)));
    printList(partition(makeList(nums), 3));
    printList(sortList(makeList(nums)));

    return;
}
