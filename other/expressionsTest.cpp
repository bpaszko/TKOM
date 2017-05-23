#include <iostream>

int main(){
	int x1 = 2;
	int x2 = 6; 
	int x3 = 2;
	bool x = true;
	bool resBexp = (!(x1 < 2) || ((x2 > x3) && true) && ((x3 == x2) || ((x3 == x1) && true)));
	int resAexp = (1 + x1 * (x2 + x3 -(12 + x1 *(2+2) / (3-x2))));
	float resAexp2 = (((x1 + x2) / (x2 - 5) / (x3-x1+1)) / ((1-0.1) / 0.2)) / 0.01;
	int resAexp3 = (((x1 + x2) / (x2 - 5) / (x3-x1+1)) / ((1-0.1) / 0.2)) / 0.01 + x;
	int s = x;
	int s2 = x + 2 + 'a';
	bool s3 = x + 2 + 'a';
	float k = resAexp + resBexp + resAexp2 +resAexp3 + s + s2 + s3;
	s3 = x  + 'c';
	s = false;
	resBexp = true || false;
	resAexp2 = 1 + 2 + x;
	k = k + s + s3 + resBexp + resAexp2;
	std::cout << k;
	return k;
}