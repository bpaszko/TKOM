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

int main(){
	while(false){}
	for(int i = 0; i < 2; i = i + 2){}
	if (false) {} else {}
	Y y;
	int k = 2+ y.x.var;
	fun(y.x, 'a');
	false && ((k < 2) && !(l > k));
	false && ((k < 2) && (!l > k));
	std::cout << k;
	return k;
}