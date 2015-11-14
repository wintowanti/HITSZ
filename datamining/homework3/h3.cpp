#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;

// size of Category
const int CATEGORY_SIZE = 3;
// define Point struct/
struct Point{
    double x,y,category_flag;
    //constructo
    Point(){ }
    Point(double _x,double _y){ x = _x; y = _y; }
    //overload + 
    Point friend operator + (const Point p1,const Point p2){ return Point(p1.x + p2.x,p1.y + p2.y); }
    //overload - 
    Point friend operator - (const Point p1,const Point p2){ return Point(p1.x - p2.x,p1.y - p2.y); }
    //overload /
    Point friend operator / (const Point p1,double v1){ return Point(p1.x / v1,p1.y / v1); }
    // get distance of two points;
    double dis (const Point p1){ 
        return (x - p1.x)*(x - p1.x) + ( y - p1.y) * (y - p1.y);
    }
    //debug
    void debug(){ cout<<"( "<<x<<", "<<y<<")"<<endl; }
};
// define Category struct
struct Category{
    Point centre;
    Category(double _central_x,double _central_y){ centre = Point(_central_x,_central_y); } 
    // debug print centre point
    void debug(){
       cout<<"centre: ";
       centre.debug();
    }
};

//globle 
vector< Point > points;
vector<Category> categorys;
//control 
struct Control{ 
    // initialize data
    void init(){
        // init point data
        points.clear();
        //init categoary data
        categorys.clear();
    }
    // classsify all points
    void classify(){
        for(int i = 0; i < points.size(); i++){
            // select a catogory central point is closed to point
            double dis0 = points[i].dis(categorys[0].centre);
            double dis1 = points[i].dis(categorys[1].centre);
            double dis2 = points[i].dis(categorys[2].centre);
            double tmin = min(dis0,dis1);
            tmin = min(dis2,tmin);
            int category_id = 0;
            if(dis1 == tmin) category_id = 1;
            if(dis2 == tmin) category_id = 2;
            points[i].category_flag = category_id;
        }
    }
    // find new centre point for each category
    void find_new_centre(){
        for(int i = 0; i < CATEGORY_SIZE; i++){
            Point new_centre = Point(0,0);
            double count = 0.0;
            for(int j = 0; j < points.size(); j++){
                if(points[j].category_flag == i){
                    new_centre = new_centre + points[j];
                    count += 1.0;
                }
            }
            if(count > 0) new_centre = new_centre / count;
            categorys[i].centre = new_centre;
        }
    }
    // get the sum of distantce points to their category centrl
    double get_all_point_dis(){
        double tsum = 0.0;
        for(int i = 0; i < points.size(); i++){
            tsum += points[i].dis( categorys[points[i].category_flag].centre );
        }
        return tsum;
    }
    // output information
    void debug(){
        puts("\n----------------------------------------\n");
        cout<<"the sum of distance : "<< get_all_point_dis()<<endl;
        for(int i = 0; i < CATEGORY_SIZE; i++){
            cout<<"\ncategory  id : "<<i<<endl;
            categorys[i].debug();
            for(int j = 0; j < points.size(); j++){
                if(points[j].category_flag == i){
                    points[j].debug();
                    cout<<"dis to centre : "<<categorys[i].centre.dis(points[j])<<"\n"<<endl;
                }
            }
        }
        puts("\n----------------------------------------\n");
    }

}test;
int main(){
    test;
    test.init();
    // add point
    points.push_back(Point(2,10));
    points.push_back(Point(2,5));
    points.push_back(Point(8,4));
    points.push_back(Point(5,8));
    points.push_back(Point(7,5));
    points.push_back(Point(6,4));
    points.push_back(Point(1,2));
    points.push_back(Point(4,9));
    points.push_back(Point(7,3));
    points.push_back(Point(1,3));
    points.push_back(Point(3,9));
    // add three category
    categorys.push_back(Category(2,10));
    categorys.push_back(Category(5,8));
    categorys.push_back(Category(1,2));
    test.classify();
    test.debug();
    for(int i = 0; i < 6; i++){
        test.classify();
        test.find_new_centre();
        test.debug();
    }
    return 0;
}

