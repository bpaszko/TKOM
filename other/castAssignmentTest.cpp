#include <iostream>

int l = 2;
int y = 4;

class Z {};

class X {
public:
	int fun(int a){}
	int var = 3;
};

class Y {
public:
	X x;
private:
	int k = 2;
	int fun2(){k = 2 + k;}
	char x2 = 'a';
};

int fun(X a, char b){} 
X fun2(){}
int ff1(){return 2.2;}
long ff2(){return 1;}
char ff3(){return 0;}
float ff4(){return 2;}
double ff5(){return 2.0;}
bool ff6(){return 2;}

int main(){
	//check all combinations of ltype-rtype in assignment
	int a1 = ff1();
	int a2 = ff2();
	int a3 = ff3();
	int a4 = ff4();
	int a5 = ff5();
	int a6 = ff6();
	bool b1 = ff1();
	bool b2 = ff2();
	bool b3 = ff3();
	bool b4 = ff4();
	bool b5 = ff5();
	bool b6 = ff6();
	float f1 = ff1();
	float f2 = ff2();
	float f3 = ff3();
	float f4 = ff4();
	float f5 = ff5();
	float f6 = ff6();
	long l1 = ff1();
	long l2 = ff2();
	long l3 = ff3();
	long l4 = ff4();
	long l5 = ff5();
	long l6 = ff6();
	double d1 = ff1();
	double d2 = ff2();
	double d3 = ff3();
	double d4 = ff4();
	double d5 = ff5();
	double d6 = ff6();
	char c1 = ff1();
	char c2 = ff2();
	char c3 = ff3();
	char c4 = ff4();
	char c5 = ff5();
	char c6 = ff6();

	//check casting when r-value is expression
	float x = 2+ 3 - 4;
	int x1 = 2 + 3 - 4;
	int x2 = 2 + 3 - x;
	long x3 = 1 + 1;
	bool x4 = false;
	int x5 = x3 + 2;
	int x6 = x3 + 2.0;
	int x7 = x3 + x4;
	bool x8 = x4 + 2;

	Y y;
	int k = 2+ y.x.var;
	fun(y.x, 'a');

	std::cout << k;
	return k;
}