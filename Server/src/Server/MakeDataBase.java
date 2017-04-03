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
			Door door1 = new Door(false, "10.0.0.20");
			ArrayList<Door> doors = new ArrayList<Door>();
			doors.add(door1);
			doors.add(new Door());
			
			User blucas = new User("blucas", "Phantom1");
			ArrayList<User> users= new ArrayList<User>();
			users.add(blucas);
			House house1 = new House(doors, users, "1326");
			ArrayList<Door> otherDoors = new ArrayList<>();
			otherDoors.add(new Door());
			House house5 = new House(otherDoors, "CC34");
			doors.add(door1);
			House house3 = new House(doors, "A55B");
			
			
			
			

			ArrayList<House> houseList = new ArrayList<House>(16);
			for(int i=0; i<16; i++) houseList.add(null);
			houseList.set(0, house1);
			houseList.set(2, house3);
			houseList.set(4, house5);
			
			Houses houses = new Houses(houseList);
			objMapper.writeValue(database, houses);
  }
}
