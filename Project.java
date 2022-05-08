package project;

import java.awt.*;
import java.util.Scanner;

public class Project {
	public static int random (int min, int max) {
		return (int)(Math.random() * (max - min + 1)) + min;
	}
	
	public static Scanner reader = new Scanner(System.in);
	
	public static void main(String[] args) {
		Canvas canvas = Canvas.getCanvas();
		
		Rectangle r = new Rectangle(0, 250, 500, 50);
		canvas.setForegroundColour(Color.green);
		canvas.fill(r);
		Square s = new Square(50, 170, 100, "yellow");
		s.draw();
		Triangle t = new Triangle(100, 120, 100, 50, "red");
		t.draw();
		Rectangle r2 = new Rectangle(90, 230, 20, 40);
		canvas.setForegroundColour(Color.black);
		canvas.fill(r2);
		Square s1 = new Square(70, 190, 15, "blue");
		s1.draw();
		Square s2 = new Square(115, 190, 15, "blue");
		s2.draw();
		
		int minx = 175, maxx = 475, miny = 230, maxy = 290, kids = 10;
		System.out.println("Enter number of kids:");
		kids = reader.nextInt();
		Kid[] k = new Kid[kids];
		String[] colors = {"red", "black", "green", "blue", "yellow", "magenta", "white"};
		
		for (int i = 0; i < kids; i++) {
			Kid k1= new Kid(random(minx, maxx), random(miny, maxy), colors[random(0, colors.length - 1)]);
			k1.draw();
			k[i] = k1;
		}
		
		minx = 0;
		maxx = 500;
		miny = 0;
		maxy = 70;
		int clouds = 50;
		System.out.println("Enter number of clouds:");
		clouds = reader.nextInt();
		Circle[] c = new Circle[clouds];
		
		for (int i = 0; i < clouds; i++) {
			Circle c1 = new Circle(random(minx, maxx), random(miny, maxy), 50, "white");
			c1.draw();
			c[i] = c1;
		}
		
		System.out.println("kill?");
		if (reader.nextBoolean()) {
			for (int i = 0; i < k.length; i++) {
				k[i].erase();
				k[i].kill();
				k[i].draw();
				
				canvas.wait(100);
			}
			
			canvas.wait(100);
			
			for (int tt = 0; tt < 50; tt++) {
				for (int cc = 0; cc < clouds; cc++) {
					c[cc].changeSizeTo(c[cc].getDiameter() + 10);
					c[cc].move(-5, -5);
					c[cc].draw();
				}
			}
		}
		
		canvas.setVisible(false);
		
	}
}
