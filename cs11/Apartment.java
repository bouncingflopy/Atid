package work;

public class Apartment {
	private String ownerName;
	private Room[] rooms;
	
	public Apartment(String ownerName, Room[] rooms) {
		this.ownerName = ownerName;
		if (rooms.length <= 10) {
			this.rooms = new Room[rooms.length];
			for (int i = 0; i < rooms.length; i++) {
				this.rooms[i] = rooms[i];
			}
		} else {
			System.out.println("Invalid amount of rooms.");
		}
	}
	
	public double area() {
		double total = 0;
		for (int i = 0; i < rooms.length; i++) {
			total += rooms[i].area();
		}
		
		System.out.println("The total area of the apartment is " + total + ".");
		return total;
	}
	
	public String size() {
		double a = this.area();
		
		if (a <= 70) {
			return "small";
		} else if (a <= 110) {
			return "medium";
		} else {
			return "large";
		}
	}
	
	public String getOwnerName() {
		return this.ownerName;
	}
	
	public Room[] getRooms() {
		return rooms;
	}
	
	public void setOwnerName(String ownerName) {
		this.ownerName = ownerName;
	}
	
	public void setRooms(Room[] rooms) {
		if (rooms.length <= 10) {
			this.rooms = new Room[rooms.length];
			for (int i = 0; i < rooms.length; i++) {
				this.rooms[i] = rooms[i];
			}
		} else {
			System.out.println("Invalid amount of rooms.");
		}
	}
	
	@Override
	public String toString() {
		String temp = "";
		for (int i = 0; i < rooms.length; i++) {
			temp += rooms[i].toString() + " ";
		}
		return "owner: " + this.ownerName + ", rooms: {" + temp + "}";
	}
}
