#include <iostream>

//THIS TEST CHECKS NESTED OBJECTS 

int l = 2;
int y = 4;

class Z {
public:
	int varZ = 2;
	int funZ(int arg){
		int ret = arg + varZ;
		return ret;
	}
	int funZobj(Z obj){
		obj.varZ = 4;
		return obj.varZ;
	}
};

class X {
public:
	Z z;
	int varX = 2;
	int funX(int arg){
		int ret = arg + varX;
		return ret;
	}
	int funXobj(X obj){
		obj.varX = 4;
		return obj.varX;
	}
};

class Y {
public:
	X x;
	int varY = 2;
	int funY(int arg){
		int res = arg + 2;
		return res;
	}
};


int main(){
	X x;
	Y y;
	Z z;
	//passing object as argument should trigger deepcopy so it wont change the object
	int zet = z.funZ(z.varZ);
	int tmp = z.funZobj(z);
	zet = zet + tmp + z.varZ;
	int ex = x.funXobj(x);
	tmp = x.funX(x.varX);
	ex = ex + tmp + x.varX;
	int laj = y.funY(y.varY);
	laj = laj + y.varY;
	int nest1 = x.z.funZ(x.z.varZ);
	tmp = x.z.funZobj(x.z);
	nest1 = nest1 + tmp + x.z.varZ;
	int nest2 = y.x.funX(y.x.varX);
	tmp = y.x.varX;
	int tmp2 = y.x.funXobj(y.x);
	nest2 = nest2 + tmp + tmp2;
	int nest3 = y.x.z.funZobj(y.x.z);
	tmp = y.x.z.funZ(y.x.z.varZ);
	nest3 = nest3 + tmp + y.x.z.varZ;
	int k = zet + ex + laj + nest1 + nest2 + nest3;
	std::cout << k;
	return k;
}