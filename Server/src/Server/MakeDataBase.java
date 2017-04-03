package Server;
import java.util.ArrayList;
import java.util.Map;
import java.util.TreeMap;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;

public class MakeDataBase{

  public static void main(String[] args) throws IOException{

      ObjectMapper objMapper = new ObjectMapper();

			File database = new File("database.json");
			
			// Initialize with null doors
			ArrayList<House> houseList = new ArrayList<House>(16);
			doors.add(new Door(false, "10.0.0.20"));
			ArrayList<User> users= new ArrayList<User>();
			users.add(new User("JJohnson", "Phantom1"));
			House house = new House(doors, users, "1326");
			
			// Home 1
			ArrayList<Door> doors = new ArrayList<Door>();
			doors.add(new Door(false, "10.0.0.20"));
			houseList.add(house);
			
			// Home 2
			for(int i=0; i<16; i++) houseList.add(house);
			
			// Home 3
			doors = new ArrayList<Door>();
			doors.add(new Door(false, "10.0.0.20"));
			doors.add(new Door(false, "10.0.0.20"));
			doors.add(new Door(false, "10.0.0.20"));
			users = new ArrayList<User>();
			users.add(new User("AAaronson", "Phantom2"));
			house = new House(doors, users, "A55B");
			houseList.set(2, house);
						
			// Home 5
			doors = new ArrayList<Door>();
			doors.add(new Door(false, "10.0.0.20"));
			users = new ArrayList<User>();
			users.add(new User("TThompson", "Phantom3"));
			house = new House(doors, users, "CC34");
			houseList.set(4, house);
			
			// Home 6
			doors = new ArrayList<Door>();
			doors.add(new Door(false, "10.0.0.20"));
			doors.add(new Door(false, "10.0.0.20"));
			users = new ArrayList<User>();
			users.add(new User("RRichardson", "Phantom4"));
			house = new House(doors, users, "6540");
			houseList.set(5, house);
						
			// Home 9
			doors = new ArrayList<Door>();
			doors.add(new Door(false, "10.0.0.20"));
			doors.add(new Door(false, "10.0.0.20"));
			doors.add(new Door(false, "10.0.0.20"));
			users = new ArrayList<User>();
			users.add(new User("PPeterson", "Phantom5"));
			house = new House(doors, users, "6565");
			houseList.set(8, house);			 
		
			Houses houses = new Houses(houseList);
			objMapper.writeValue(database, houses);
  }
}
