//
// Created by ByteDance on 2023/12/12.
//

#include<iostream>
#include<vector>
#include<cmath>
#include<algorithm>
using namespace std;


vector<vector<int>> twoSum(vector<int>& nums){
    int n = nums.size();
    vector<vector<int>> res;
    sort(nums.begin(), nums.end());

    int i=0, j = n;
    int tmp = nums[0] + nums[j-1];
    while(i<j){
        if(tmp == 0)
            res.push_back({i, j-1});
        else if (tmp < 0)
            i++;
        else
            j--;
    }
    return res;
}

vector<vector<int>> threeSum(vector<int>& nums) {
    vector<vector<int>> res;
    sort(nums.begin(), nums.end());

    int n = nums.size();
    if(n<3 || nums[0]>0 || nums[n-1]<0){
        return res;
    }

    int i=0, j=n;
    int tmp = nums[i]+nums[j-1];
    while(i<j){
        for(int k=i+1; k<j; k++){
            if(tmp + nums[k] == 0){
                res.push_back({i,k,j});
            }
        }
        if(tmp<0)
            i++;
        else
            j--;
    }
    return res;
}

int threeSumClosest(vector<int>& nums, int target) {

    int n = nums.size();
    int ans = nums[0] + nums[1] +nums[2];
    sort(nums.begin(), nums.end());

    int i=0, j=n;
    int tmp = nums[i]+nums[j-1];
    while(i<j){
        for(int k=i+1; k<j; k++){
            if(abs(tmp + nums[k] - target) < abs(ans-target)){
                ans = tmp + nums[k];
            }
        }
        if(tmp<target)
            i++;
        else
            j--;
    }
    return ans;
}

vector<vector<int>> fourNum(vector<int> &nums){
    int n = nums.size();
    vector<vector<int>> res;
    sort(nums.begin(), nums.end());

    int i=0, j = n;
    int tmp = nums[i] + nums[j-1];
    while(i<j){
        int k=i+1, t=j-1;
        while(k<t){
            if(tmp+nums[k]+nums[t-1] == 0) {
                res.push_back({i, k, t - 1, j - 1});
            }else if (tmp+nums[k]+nums[t-1] < 0){
                k++;
            } else {
                t--;
            }
        }
        if(tmp<0){
            i++;
        }else {
            j--;
        }
    }
    return res;
}


void arrayTest(){
    cout<<"hello world"<<endl;

    vector<int> nums = {1,2,4,3,5,6};
    sort(nums.begin(), nums.end());
    for(auto it = nums.begin(); it != nums.end(); it++){
        cout<<*it<<' ';
    }
    cout<<endl;
    cout<<abs(-1)<<endl;
    cout<<abs(-1.5)<<endl;

    return ;
}