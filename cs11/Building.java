
public class Building {
	private Address address;
	private Apartment[] apartments;
	
	public Building(Address address, Apartment[] apartments) {
		this.address = address;
		if (apartments.length <= 100) {
			for (int i = 0; i < 100; i++) {
				this.apartments[i] = apartments[i];
			}
		} else {
			System.out.println("Invalid amount of apartments");
		}
	}
	
	public int largeApartments() {
		int sum = 0;
		for (int i = 0; i < apartments.length; i++) {
			if (apartments[i].size() == "large") {
				sum++;
			}
		}
		
		return sum;
	}
	
	public Address getAddress() {
		return this.address;
	}
	
	public Apartment[] getApartments() {
		return this.apartments;
	}
	
	public void setAddress(Address address) {
		this.address = address;
	}
	
	public void setApartments(Apartment[] apartments) {
		if (apartments.length <= 100) {
			for (int i = 0; i < 100; i++) {
				this.apartments[i] = apartments[i];
			}
		} else {
			System.out.println("Invalid amount of apartments");
		}
	}
}
