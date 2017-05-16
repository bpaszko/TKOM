#include <iostream>

int main(){
	int x1 = 2;
	int x2 = 6; 
	int x3 = 2;
	bool resBexp = (!(x1 < 2) || ((x2 > x3) && true) && ((x3 == x2) || ((x3 == x1) && true)));
	int resAexp = (1 + x1 * (x2 + x3 -(12 + x1 *(2+2) / (3-x2))));
	int k = resAexp + resBexp;
	std::cout << k;
	return k;
}