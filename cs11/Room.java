
public class Room {
	private String type;
	private double length;
	private double width;
	
	public Room(String type, double length, double width) {
		this.type = type;
		this.length = length;
		this.width = width;
	}
	
	public Room(Room room) {
		this.type = room.getType();
		this.length = room.getLength();
		this.width = room.getWidth();
	}
	
	public double area() {
		return length * width;
	}
	
	public String getType() {
		return this.type;
	}
	
	public double getLength() {
		return this.length;
	}
	
	public double getWidth() {
		return this.width;
	}
	
	public void setType(String type) {
		this.type = type;
	}
	
	public void setLength(double length) {
		this.length = length;
	}
	
	public void setWidth(double width) {
		this.width = width;
	}
}
