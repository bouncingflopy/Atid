package work;

public class Main {
	public static void maxLarge(Building[] buildings) {
		Building max = buildings[0];
		for (int i = 1; i < buildings.length; i++) {
			if (buildings[i].largeApartments() > max.largeApartments()) {
				max = buildings[i];
			}
		}
		
		for (int i = 0; i < buildings.length; i++) {
			if (buildings[i].largeApartments() == max.largeApartments()) {
				System.out.println(buildings[i].getAddress().toString());
				Apartment[] apartments = buildings[i].getApartments();
				for (int j = 0; j < apartments.length; j++) {
					if (apartments[j].size() == "large") {
						System.out.println(apartments[j].getOwnerName());
					}
				}
			}
		}
		
	}
}
