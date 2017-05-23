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

int main() {
	X obj;
	int y = 0;
	for(int i = 0; i < 5; i = i + 1) {
		if (y < 10) {
			y = obj.f(i);
			continue;
		}
		else
			break;
	}
	std::cout << y << std::endl;
	return y;
}
