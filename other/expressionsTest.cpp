#include <iostream>

//THIS TEST CHECKS COMPLEX AEXP AND BEXP

int main(){
	int x1 = 2;
	int x2 = 6; 
	int x3 = 2;
	bool x = true;
	//CHECK IF ALL PARANTHESIS ARE PRESENT IN PYTHON
	bool resBexp = (!(x1 < 2) || ((x2 > x3) && true) && ((x3 == x2) || ((x3 == x1) && true)));
	//int / int should be casted to int
	int resAexp = (1 + x1 * (x2 + x3 -(12 + x1 *(2+2) / (3-x2))));
	//float/float or float/int shouldnt be casted
	float resAexp2 = (((x1 + x2) / (x2 - 5) / (x3-x1+1)) / ((1-0.1) / 0.2)) / 0.01;
	//end result should be casted to int
	int resAexp3 = (((x1 + x2) / (x2 - 5) / (x3-x1+1)) / ((1-0.1) / 0.2)) / 0.01 + x;
	//cast to int
	int s = x;
	//no cast, only char triggers ord()
	int s2 = x + 2 + 'a';
	//cast to bool should be present
	bool s3 = x + 2 + 'a';
	//no cast is needed, rval is float
	float k = resAexp + resBexp + resAexp2 +resAexp3 + s + s2 + s3;
	//cast to bool
	s3 = x  + 'c';
	//cast to int
	s = false;
	//no cast
	resBexp = true || false;
	//cast to float
	resAexp2 = 1 + 2 + x;
	//no cast, rval is float already
	k = k + s + s3 + resBexp + resAexp2;
	std::cout << k;
	return k;
}