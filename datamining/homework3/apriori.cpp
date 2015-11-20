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
        cout<<"\n----------------------------------------"<<endl;
        for(int i = 0; i < data.size(); i++) cout<<data[i]<<" ";
        cout<<"\n----------------------------------------"<<endl;
    }
};
//globe variable
int data_lib[MAX_K][MAX_K];
vector< vector<int> > input;
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
//get data
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
    puts("good");
    for(int i = 0; i < input.size(); i++){
       for(int j = 0; j < input[i].size(); j++){
           cout<<i <<"  "<<input[i][j]<<endl;
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
            cout<< i << " ++ "<<items_count(items1)<<endl;
            ans.push_back(items1);
        }
    }
    return ans;
}
// get kn item1
vector< vector<Items> >get_frequent_items(){
    vector< vector<Items> > itemset;
    itemset.clear();
    itemset.push_back(init_k1_item());

    for(int i = 0; i < itemset[0].size(); i++){
        itemset[0][i].debug();
        cout<<"count: " << items_count(itemset[0][i])<<endl;
    }
    puts("*");
    for(int i = 2; i-2 < itemset.size(); i++){
        vector <Items> tmp;
        tmp.clear();
        for(int j = 0; j < itemset[i-2].size(); j++){
            for(int k = 0; k < itemset[i-2].size(); k++){
                if(j != k){
                    if(itemset[i-2][j].is_union(itemset[i-2][k])){
                        Items items_un = itemset[i-2][j]._union(itemset[i-2][k]);
                        if(items_count(items_un) >= SUPPORT_RATE * input.size()){
                            items_un.debug();
                            cout<<"count: "<<items_count(items_un)<<endl;
                            tmp.push_back(items_un);
                        }
                    }
                }
            }
        }
        if(tmp.size() > 0) itemset.push_back(tmp);
    }
    puts("*");
    return  itemset;
}

int main(){
    get_data_lib();
    puts("~~");
    get_frequent_items();
    puts("mark");
    return 0;
}
