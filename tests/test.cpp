// MAIN TEST

class X {
public:
	long x = 15;
	int f(int arg) {
		f2();
		int y = x + arg;
		return y;
	}
private:
	void f2() {
		x = x + 5;
	}
};
int main() {
	X obj;
	int y = 5/5 - 1 * 1;
	bool z = true;
	for(int i = 0; i <= 5; i = i + 1) {
		if (y < 10 && z || false) {
			y = obj.f(i);
			continue;
		}
		else
			break;
	}
	return y;
}

