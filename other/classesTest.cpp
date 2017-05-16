#include <iostream>

class X {
public:
	int var = 3;
	int fun(int a){
		int res = var * a;
		return res;
	}
};

int fun_glob(X a, char b){
	int res = a.var + b;
	int tmp = a.fun(b);
	res = res + tmp;
	return res;
} 

class Y {
private:
	int k = 2;
	int fun2(){k = 2 + k;}
	char x2 = 'a';
public:
	X x;
	int fun(int arg){
		int tmp = 0;
		while(false){}
		for(int i = 0; i < 5; i = i + 2){
			k = k + 2;
			fun2();
			k = k + x2;
			tmp = fun_glob(x, x2);
			k = k + tmp;
			tmp = x.fun(2);
			k = k + tmp;
			k = k + x.var;
		}
		return k;
	}
	int fun3(int x, int x2){
		int res = x + x2;
		return res;
	}

};

int main(){
	Y y;
	int res = y.fun(2);
	int tmp = y.fun3(10, 10);
	int k = res + tmp;
	std::cout << k;
	return k;
}