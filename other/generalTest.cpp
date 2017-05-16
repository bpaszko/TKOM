#include <iostream>

class X {
public:
	long x = 15; 
private:
	void f2() {
		x = x + 5;
	}
public:
	int f(int arg) {
		f2();
		int y = x + arg;
		return y;
	}
};

class Z {
public:
	X fun(){
		X x;
		x.x = 5; 
		return x;
	}
};

int main() {
	X obj;
	Z objZ;
	int y = 0;
	int tmp = 0;
	for(int i = 0; i < 5; i = i + 1) {
		if (y < 10) {
			tmp = obj.f(i);
			y = y + tmp;
			continue;
		}
		else
			break;
	}
	obj = objZ.fun();
	y = y + obj.x;
	tmp = obj.f(y);
	y = y + tmp;

	std::cout << y << std::endl;
	return y;
}
