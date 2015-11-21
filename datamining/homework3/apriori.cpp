#include <cstdio>
#include <cstring>
#include <iostream>
#include <vector>
using namespace std;

// max k itemset
const int MAX_K = 100;
// supprot rate is 0.2
const double SUPPORT_RATE = 0.2;
// confidence rate is 0.2
const double CONFIDENCE_RATE = 0.8;
//
struct Items{
    vector<int> data;
    int count;
    //constructor
    Items(vector<int> _data){
        for(int i = 0; i < _data.size(); i++) data.push_back(_data[i]);
    }
    // judge 2 items whether can union
    bool is_union(Items items1){
        int flag = 1;
        for(int i = 0; i < data.size() -1; i++){
            if(data[i] != items1.data[i]) flag = 0;
        }
        int last = data.size() - 1;
        if(data[last] >= items1.data[last]) flag =0;
        return flag;
    }
    // union 2 Items;
    Items _union(Items items1){
        vector<int> tmp;
        for(int i = 0; i < data.size();i++) tmp.push_back(data[i]);
        int last = items1.data.size() - 1;
        tmp.push_back(items1.data[last]);
        Items ans = Items(tmp);
        return ans;
    }
    void debug(){
        cout<<"( ";
        for(int i = 0; i < data.size(); i++) cout<<data[i]<<" ";
        cout<<")";
    }
};
//globe variable
int data_lib[MAX_K][MAX_K];
vector< vector<int> > input;
int flag[MAX_K];
//initialisze globe variable
void init(){
    memset(data_lib,0,sizeof(data_lib));
}
// count times of items
int items_count(Items items1){
    int ans = 0;
    for(int i = 0; i < input.size(); i++){
        int flag = 1;
        for(int j = 0; j < items1.data.size(); j++){

            if(data_lib[i][items1.data[j]]== 0) flag = 0;
        }
        ans += flag;
    }
    return ans;
}
//get input data
void get_data_lib(){
  for(int i = 0; i < MAX_K; i++) input.clear();
    vector<int> tmp;
        tmp.clear(); tmp.push_back(1); tmp.push_back(2);tmp.push_back(5);input.push_back(tmp);
        tmp.clear(); tmp.push_back(1); tmp.push_back(2);input.push_back(tmp);
        tmp.clear(); tmp.push_back(2); tmp.push_back(4);input.push_back(tmp);
        tmp.clear(); tmp.push_back(1); tmp.push_back(2);tmp.push_back(4);input.push_back(tmp);
        tmp.clear(); tmp.push_back(1); tmp.push_back(3);input.push_back(tmp);
        tmp.clear(); tmp.push_back(1); tmp.push_back(2);tmp.push_back(3);tmp.push_back(5);input.push_back(tmp);
        tmp.clear(); tmp.push_back(1); tmp.push_back(2);tmp.push_back(3);input.push_back(tmp);
        tmp.clear(); tmp.push_back(2); tmp.push_back(5);input.push_back(tmp);
        tmp.clear(); tmp.push_back(2); tmp.push_back(3);tmp.push_back(4);input.push_back(tmp);
        tmp.clear(); tmp.push_back(3); tmp.push_back(4);input.push_back(tmp);
    for(int i = 0; i < input.size(); i++){
       for(int j = 0; j < input[i].size(); j++){
           data_lib[i][input[i][j]] = 1;
       }
    }
    
}
// get k1 item1
vector<Items> init_k1_item(){
    vector< Items > ans;
    ans.clear();
    for(int i = 1 ; i < MAX_K; i++){
        vector<int> tmp;
        tmp.clear();
        tmp.push_back(i);
        Items items1 = Items(tmp);
        // only keep items which large than equal to support rate
        if(items_count(items1) >= SUPPORT_RATE * input.size()){
            ans.push_back(items1);
        }
    }
    return ans;
}
// get k2 k3 ...kn itemset
vector< Items >get_frequent_items(){
    vector< vector<Items> > itemset;
    vector<Items> ans;
    ans.clear();
    itemset.clear();
    itemset.push_back(init_k1_item());
    for(int i = 2; i-2 < itemset.size(); i++){
        vector <Items> tmp;
        tmp.clear();
        for(int j = 0; j < itemset[i-2].size(); j++){
            for(int k = 0; k < itemset[i-2].size(); k++){
                if(j != k){
                    if(itemset[i-2][j].is_union(itemset[i-2][k])){
                        Items items_un = itemset[i-2][j]._union(itemset[i-2][k]);
                        if(items_count(items_un) >= SUPPORT_RATE * input.size()){
                            tmp.push_back(items_un);
                            ans.push_back(items_un);
                        }
                    }
                }
            }
        }
        if(tmp.size() > 0) itemset.push_back(tmp);
    }
    return ans;
}
//dfs enumerate all rules
void dfs(Items items1,int level){
    if(level == items1.data.size()){
        vector <int> p1; p1.clear();
        vector <int> p2; p2.clear();
        for(int i = 0; i < items1.data.size();i++){
            if(flag[i]) p1.push_back(items1.data[i]);
            else  p2.push_back(items1.data[i]);
        }
        if(p1.size() == items1.data.size() || p1.size() == 0) return ;
        Items itemsp1 = Items(p1);
        Items itemsp2 = Items(p2);
        // show only rules only larger than or euqual to confidencw rate
        if(items_count(items1) >= items_count(itemsp1) * CONFIDENCE_RATE){
            itemsp1.debug();
            cout<<" ===> ";
            itemsp2.debug();
            cout<<"  confidence : " <<items_count(items1) * 1.0 / items_count(itemsp1)<<endl;
        }
        return ;
    }
    flag[level] = 1;
    dfs(items1,level + 1);
    flag[level] = 0;
    dfs(items1,level + 1);
    return ;
}
void get_all_rule(Items items1){
    memset(flag,0,sizeof(flag));
    dfs(items1,0);
}
void work(){
    get_data_lib();
    vector<Items> vi = get_frequent_items();
    puts("\n---------------frequent items--------------------");
    cout<<"frequent items is : "<<endl;
    for(int i = 0; i < vi.size(); i++){
       vi[i].debug();
       cout<<" support : "<<items_count(vi[i]) * 1.0 / input.size()<<endl;
    }
    puts("--------------------END--------------------------\n");

    puts("\n---------------rules-----------------------------");
    for(int i = 0; i < vi.size(); i++){
        get_all_rule(vi[i]);
    }
    puts("--------------------END--------------------------\n");
}
int main(){
    work();
    return 0;
}
