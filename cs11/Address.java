package work;

public class Address {
	private String street;
	private int number;
	private String city;
	
	public Address(String street, int number, String city) {
		this.street = street;
		this.number = number;
		this.city = city;
	}
	
	public String getStreet() {
		return this.street;
	}
	
	public int getNumber() {
		return this.number;
	}
	
	public String getCity() {
		return this.city;
	}
	
	public void setStreet(String street) {
		this.street = street;
	}
	
	public void setNumber(int number) {
		this.number = number;
	}
	
	public void setCity(String city) {
		this.city = city;
	}
	
	@Override
	public String toString() {
		return street + " " + number + ", " + city;
	}
}
