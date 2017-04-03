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
			Door door1 = new Door();
			ArrayList<Door> doors = new ArrayList<Door>();
			doors.add(door1);

			User blucas = new User("blucas", "Phantom1");
			ArrayList<User> users= new ArrayList<User>();
			users.add(blucas);
			House house1 = new House(doors, users);

			ArrayList<House> houseList = new ArrayList<House>();
			houseList.add(house1);
			Houses houses = new Houses(houseList);
			objMapper.writeValue(database, houses);
  }
}
