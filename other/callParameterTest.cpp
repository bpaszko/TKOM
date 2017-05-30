#include <iostream>

class X{};

void fun(int a, long b, char c, float d, double e, bool f){}

int main(){
	int i = 0;
	long l = 0;
	char c = 0;
	float f = 0;
	double d =0;
	bool b = false;

	//CHECK ALL COMBINATIONS ARG-PARAM TYPES
	fun(i,i,i,i,i,i);
	fun(l,l,l,l,l,l);
	fun(c,c,c,c,c,c);
	fun(f,f,f,f,f,f);
	fun(d,d,d,d,d,d);
	fun(b,b,b,b,b,b);
	fun(1,1,1,1,1,1);
	fun(2.0,2.0,2.0,2.0,2.0,2.0);
	
	std::cout << "1" ;
	return 1;
}