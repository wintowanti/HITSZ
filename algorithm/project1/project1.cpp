#include <cstdio>
#include <iostream>
#include <cmath>
#include <cstring>
using namespace std;

const int MX = 1000; // MX is the max size of point
const int INF = 0x3f3f3f3f; // A big integer number
double dp[MX][MX]; //dp[i][j] the min value from vertex_i to vertex_j
int mark[MX][MX]; //mark[i][j] the split vertex position from vertex_i to vertex_j which can get the min value
double point[MX][2];

//get the distance of the two points indexs are index_1 index_2
double get_dis(int index_1,int index_2){
    double ans = (point[index_1][0] - point[index_2][0]) *(point[index_1][0] - point[index_2][0]);
    ans += (point[index_1][1] - point[index_2][1]) *(point[index_1][1] - point[index_2][1]);
    return sqrt(ans);
}

//get the value of the triangle which point indexs are index_1,index_2,and index_3
double get_triangle(int index_1,int index_2,int index_3){
   return get_dis(index_1,index_2) + get_dis(index_2,index_3) + get_dis(index_3,index_1);
}

//print the answer;
void print_split_position(int index_1,int index_2){
    puts("\n----------------------------------------------------");
    printf("split position index is %d, produce triangle (V%d,V%d,V%d) \n",mark[index_1][index_2],index_1,mark[index_1][index_2],index_2);
    printf("the min value from index:V%d to index: V%d is %.4lf !\n",index_1,index_2,dp[index_1][index_2]);
    if(mark[index_1][index_2] - index_1 > 1) printf("get a subproblem which index from V%d to V%d \n",index_1,mark[index_1][index_2]);
    if(index_2 - mark[index_1][index_2] > 1) printf("get a subproblem which index from V%d to V%d \n",mark[index_1][index_2],index_2);
    puts("----------------------------------------------------\n");
    if(mark[index_1][index_2] - index_1 > 1) print_split_position(index_1,mark[index_1][index_2]);
    if(index_2 - mark[index_1][index_2] > 1) print_split_position(mark[index_1][index_2],index_2);
}
int main(){
    int n;
    // use project1_input.txt file as standard input
    freopen("project1_input.txt","r",stdin);
    // if you want to use project1_output.txt file as standard output, uncomment next line
    //freopen("project1_output.txt","w",stdout);
    while(~scanf("%d",&n)){
        puts("\n\n----------------------------------------------------------------------------------------");
        puts("-------------------------------------START----------------------------------------------");
        cout<<n<<endl;
        for(int i = 0; i < n; i++){
            scanf("%lf%lf",&point[i][0],&point[i][1]);
        }
        //init each value equal INF
        for(int i = 0; i < n; i++) 
            for(int j = 0; j < n; j++) 
                dp[i][j] = INF * 1.0;
        for(int i = 0; i < n; i++){
            for(int j = 0; i + j < n ;j++){
                if(i == 0 || i == 1){
                    dp[j][j + i] = 0.00;
                }
                else{
                    // select a index k from (j,j+i) which can get min value
                    for(int k = j+1; k < j + i; k++){
                        int value =  dp[j][k] + dp[k][j + i] + get_triangle(j,k,j + i); //the value if we select k as split position
                        if(value < dp[j][j + i]){
                            dp[j] [j + i] = value;
                            mark[j][j + i] = k;
                        }
                    }
                }
            }
        }
        printf("\nthe answer is %.4lf\n",dp[0][n-1]);
        print_split_position(0,n-1);
        puts("---------------------------------------END----------------------------------------------");
        puts("----------------------------------------------------------------------------------------\n\n");
    }
}

