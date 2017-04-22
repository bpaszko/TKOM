// FAULT TEST
// example errors at lines 9, 18, 19, 29
// to test an error remove all previous errors
// lexer only inform about first encountered error

class X {
public:
	long x = 15;
	int f(int arg) {	 #error
		f2();
		int y = x + arg;
		return y;
	}
private:
	void f2() {
		x = x + 5;
	}
};					'another error'
					"one more"
int main() {
	X obj;
	int y = 5/5 - 1 * 1;
	bool z = true;
	for(int i = 0; i <= 5; i = i + 1) {
		if (y < 10 && z || false) {
			y = obj.f(i);
			continue;
		}
		else			\error
			break;
	}
	return y;
}

