#include <iostream>

//THIS TEST CHECKS NULL CLASSES, FUNCTIONS AND COMPOUND STATEMETS
//SHOULD TRIGGER PASS IN PYTHON CODE

class Z {};

class X {
public:
private:
protected:
};

class Y {
	X fun2(){}
	int fun(int a, X b){}
};

X fun2(){}

int fun(int a, X b){}

int main(){
	while(false){}
	for(int i = 0; i < 2; i = i + 2){}
	if (false) {} else {}
	int k = 2;	
	std::cout << k;
	return k;
}