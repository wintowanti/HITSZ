#include <cstdio>
#include <cstring>
#include <vector>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
using namespace std;

const double PI = acos(-1.0);
//global variable
fstream output_f;
//define complex struct 
struct C{
    //real and image part
    double real,image;
    // constructor
    C(double _real,double _image){ real = _real; image = _image; }
    //overload operator sign +
    C friend operator + (const C c1,const C c2){
        return C(c1.real + c2.real,c1.image + c2.image);
    }

    //overload operator sign -
    C friend operator - (const C c1,const C c2){
        return C(c1.real - c2.real,c1.image - c2.image);
    }

    //overload operator sign *
    C friend operator * (const C c1,const C c2){
        return C(c1.real * c2.real - c1.image * c2.image,c1.real * c2.image + c1.image * c2.real);
    }

    //get string for complex just for ouput
    string toString(){
        stringstream ss;
        ss<<showpoint<<real<<"+"<<showpoint<<image<<"i ";
        return ss.str();
    }
};
//define FFT struct
class FFT{
    vector<C> Wx;
    int log_num;
public:
    FFT(){

    }
    // constructor 
    FFT( vector<double> Ax){
        // clear vector
        Wx.clear();
        for(int i = 0; i < Ax.size(); i++){
            Wx.push_back( C(Ax[i],0.0) );
        }
        log_num = (int)(log2(Ax.size()));
        cout<<log_num<<endl;
    }
    // test
    void test(ostream ci){
        ci << "good" <<endl;
    }
    // get FFT
    vector<C> get_FFT(vector<C> vc){ 
        if(vc.size() == 1) return vc;
        vector<C> v0;
        vector<C> v1;
        v0.clear();
        v1.clear();
        for(int i = 0; i < vc.size(); i++){
            if(i&1){
                v1.push_back(vc[i]);
            }
            else{
                v0.push_back(vc[i]);
            }
        }
        v0 = get_FFT(v0);
        v1 = get_FFT(v1);
        double angle = - 2*PI / (vc.size()*1.0);
        C wn = C(cos(angle),sin(angle));
        C w = C(1.0,0);
        for(int i = 0; i < vc.size() / 2; i++){
            C tmp1 = v0[i];
            C tmp2 = w * v1[i];
            vc[i] = tmp1 + tmp2;
            vc[i + (vc.size()/2)] = tmp1 - tmp2;
            w = w * wn;
        }
        return vc;
    }
    vector< C > work(){
        return get_FFT(Wx);
    }
private:
    //get bit reverse
    int get_bit_reverse(int dex,int size){
       int i = 0; 
       int j = size - 1;
       for(; j > i ; j--, i++){
            int flagi = 0;
            int flagj = 0;
            if(dex&(1<<i)){
                flagi = 1;
                dex -= (1<<i);
            }
            if(dex&(1<<j)){
                flagj = 1;
                dex -= (1<<j);
            }
            if(flagi) dex += (1<<j);
            if(flagj) dex += (1<<i);
       }
       return dex;
    }
    // reverse index
    void reverse(){
        for(int i = 0; i < Wx.size() /2; i++){
            int dex = get_bit_reverse(i, log_num);
            swap(Wx[i],Wx[dex]);
        }
    }
};
//get data input use ifstream
vector<double> get_input(string filepath,int size){
    fstream fs;
    fs.open(filepath.c_str(),fstream::in);
    vector<double> input;
    input.clear();
    for(int i = 0; i < size; i++){
        double tmp;
        fs>>tmp;
        input.push_back(tmp);
    }
    fs.close();
    return input;
}
//put ouput data into "output.txt"
void write_file(vector<C> ans){
    output_f<<"\n----------------------------------------------------"<<"\n";
    for(int i = 0; i < ans.size(); i++){
        output_f<<ans[i].toString();
    }
    output_f<<"\n----------------------------------------------------"<<"\n";
}
void solve(string inputpath,int size){
    vector<double> input = get_input(inputpath,size);
    FFT test = FFT(input);
    vector<C> ans = test.work();
    write_file(ans);
}
int main(){
    output_f.open("output2.txt",fstream::out);
    solve("./Project_2_test/4.txt",4);
    solve("./Project_2_test/8.txt",8);
    solve("./Project_2_test/16.txt",16);
    solve("./Project_2_test/32.txt",32);
    solve("./Project_2_test/64.txt",64);
    solve("./Project_2_test/128.txt",128);
    solve("./Project_2_test/256.txt",256);
    cout<<"open output2.txt see the result"<<endl;
    output_f.close();
    return 0;
}
