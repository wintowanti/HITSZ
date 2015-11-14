using namespace std;
// size of Category
const int Category_SIZE = 3;
// define Point strcut/
struct Point{
    double x,y,category_flag;
    //constructo
    Point(double _x,double _y);
    //overload + 
    Point friend operator + (const Point p1,const Point p2);
    //overload - 
    Point friend operator - (const Point p1,const Point p2);
    //overload /
    Point friend operator / (const Point p1,double v1);
    //debug
    void debug();
};

struct Category{
    double central_x;
    double central_y;
    Category(double _central_x,double _central_y);
    double get_dis(Point p1);
};

struct Control{
    
};
