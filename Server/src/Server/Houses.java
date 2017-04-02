package Server;

import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import Server.House;
import Server.Door;
import Server.User;
public class Houses{

	private ArrayList<House> houses;
	/**********CONSTRUCTORS******************/
	public Houses(){
		this(new ArrayList<House>());
	}

	public Houses(List<House> houses){
		this.houses = (ArrayList<House>)houses;
	}
	/**********METHODS***********************/
	public ArrayList<House> getHouses(){
		return this.houses;
	}

	public void addHouse(House house){
		this.houses.add(house);
	}
}
