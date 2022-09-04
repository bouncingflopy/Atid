package project;

class Kid {
	Circle head;
	Line body;
	Line armR;
	Line armL;
	Line legL;
	Line legR;
	int x, y;
	String color;
	
	Kid(int x, int y, String color) {
		this.x = x;
		this.y = y;
		this.color = color;
		
		this.calculate();
	}
	
	void calculate() {
		head = new Circle(x - 5, y - 10, 10, color);
		body = new Line(x, y, x, y + 10, color);
		armR = new Line(x, y + 5, x + 5, y + 5, color);
		armL = new Line(x, y + 5, x - 5, y + 5, color);
		legL = new Line(x, y + 10, x - 5, y + 15, color);
		legR = new Line(x, y + 10, x + 5, y + 15, color);
	}
	
	void draw() {
		head.draw();
		body.draw();
		armR.draw();
		armL.draw();
		legL.draw();
		legR.draw();
	}
	
	void erase() {
		head.erase();
		body.erase();
		armR.erase();
		armL.erase();
		legL.erase();
		legR.erase();
	}
	
	void kill() {
		this.color = "red";
		this.calculate();
	}
	
	int getX() {
		return this.x;
	}
	
	int getY() {
		return this.y;
	}
	
	void changeX(int d) {
		this.x += d;
		this.calculate();
	}
	
	void changeY(int d) {
		this.y += d;
		this.calculate();
	}
}
