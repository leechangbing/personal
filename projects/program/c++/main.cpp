#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

void print1DVector(vector<int> &nums){
    for(int i=0; i<nums.size(); i++){
        cout<<nums[i]<<' ';
    }
    cout<<endl;
    return ;
}


void print2DVector(vector<vector<int>> &nums){
    int m=nums.size();
    if(!m) return;
    int n = nums[0].size();

    for(int i=0; i<m; i++){
        for(int j=0; j<n; j++){
            cout<<nums[i][j]<<' ';
        }
        cout<<endl;
    }
    return ;
}

int uniquePaths(int m, int n) {
    vector<vector<int>> dp(m, vector<int>(n));
    for(int i=0; i<m; i++){
        dp[i][0] = 1;
    }
    for(int j=0; j<n; j++){
        dp[0][j] = 1;
    }
    for(int i=1; i<m; i++){
        for(int j=1; j<n; j++){
            dp[i][j] = dp[i-1][j]+dp[i][j-1];
        }
    }
    return dp[m-1][n-1];
}

int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
    int m = obstacleGrid.size();
    int n = obstacleGrid[0].size();
    if(obstacleGrid[0][0]==1) return 0;

    obstacleGrid[0][0] = 1;
    for(int i=1; i<m; i++){
        if(obstacleGrid[i][0]==1){
            obstacleGrid[i][0] = 0;
        }else {
            obstacleGrid[i][0] = obstacleGrid[i-1][0];
        }
    }
    for(int j=1; j<n; j++){
        if(obstacleGrid[0][j]==1){
            obstacleGrid[0][j] = 0;
        }else {
            obstacleGrid[0][j] = obstacleGrid[0][j-1];
        }
    }

    for(int i=1; i<m; i++){
        for(int j=1; j<n; j++){
            if(obstacleGrid[i][j]==1){
                obstacleGrid[i][j] = 0;
            }else {
                obstacleGrid[i][j] = obstacleGrid[i-1][j] + obstacleGrid[i][j-1];
            }
        }
    }
    return obstacleGrid[m-1][n-1];
}

int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size();
    int n = grid[0].size();

    for(int i=1; i<m; i++){
        grid[i][0] += grid[i-1][0];
    }
    for(int j=1; j<n; j++){
        grid[0][j] += grid[0][j-1];
    }

    for(int i=1; i<m; i++){
        for(int j=1; j<n; j++){
            grid[i][j] += min(grid[i-1][j], grid[i][j-1]);
        }
    }
    return grid[m-1][n-1];
}

int minDistance(string word1, string word2) {
    int m = size(word1);
    int n = size(word2);
    if(!m) return n;
    if(!n) return m;

    vector<vector<int>> dp(m, vector<int>(n));
    if(word1[0]==word2[0]){
        dp[0][0] = 0;
     }else{
        dp[0][0] = 1;
    }
    for(int i=1; i<m; i++){
        if(word1[i]==word2[0])
            dp[i][0] = i;
        else
            dp[i][0] = dp[i-1][0] + 1;
    }
    for(int j=1; j<n; j++){
        if(word2[j]==word1[0])
            dp[0][j] = j;
        else
            dp[0][j] = dp[0][j-1] + 1;
    }

    for(int i=1; i<m; i++){
        for(int j=1; j<n; j++){
            if(word1[i] == word2[j]){
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = min(dp[i-1][j-1], min(dp[i-1][j], dp[i][j-1])) + 1;
            }
        }
    }
//    print2DVector(dp);
    return dp[m-1][n-1];
}

int minimumTotal(vector<vector<int>>& triangle) {
    int m = triangle.size();
    for(int i=1; i<m; i++){
        int n = triangle[i].size();
        triangle[i][0] += triangle[i-1][0];
        triangle[i][n-1] += triangle[i-1][n-2];
        for(int j=1; j<n-1; j++){
            triangle[i][j] += min(triangle[i-1][j-1], triangle[i-1][j]);
        }
    }

    int res = triangle[m-1][0];
    for(int j=0; j<triangle[m-1].size(); j++){
        res = min(res, triangle[m-1][j]);
    }
    return res;
}

int maxProduct(vector<int>& nums) {
    int n = nums.size();
    vector<int> pos(n), neg(n);

    int res = nums[0];
    if(nums[0]>=0){
        pos[0] = nums[0];
        neg[0] = 0;
    }else{
        pos[0] = 0;
        neg[0] = nums[0];
    }
    for(int i=1; i<n; i++) {
        if (nums[i] >= 0) {
            pos[i] = max(nums[i], nums[i] * pos[i - 1]);
            neg[i] = nums[i] * neg[i - 1];
        } else {
            pos[i] = nums[i] * neg[i - 1];
            neg[i] = min(nums[i], nums[i] * pos[i - 1]);
        }
        res = max(res, pos[i]);
    }
    print1DVector(pos);
    print1DVector(neg);
    return res;
}

int main(){
//    cout<<uniquePaths(4, 6)<<endl;
//    string word1="intention", word2="execution";
//    cout<<minDistance(word1, word2)<<endl;
    vector<int> nums = {2,3,0,-2,4};
    cout<<maxProduct(nums)<<endl;

    return 0;
}