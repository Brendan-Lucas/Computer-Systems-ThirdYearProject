package Server;
import java.util.Map;
import java.util.TreeMap;
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

      //Map<String, Object> treeMapObj = new TreeMap<String, Object>();

      ObjectMapper objMapper = new ObjectMapper();

      JsonGenerator jsonGenerator=null;
			try {
				jsonGenerator = new JsonFactory().createGenerator(new FileOutputStream("database.txt"));
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}

      jsonGenerator.setPrettyPrinter(new DefaultPrettyPrinter());
      jsonGenerator.writeStartObject();
      jsonGenerator.writeArrayFieldStart("Houses");//StartHouses
        jsonGenerator.writeStartObject("House");//StartHouse
          jsonGenerator.writeArrayFieldStart("Doors");//StartDoors
            jsonGenerator.writeStartObject("Door");//StartDoor
              jsonGenerator.writeArrayFieldStart("Requests");
              jsonGenerator.writeEndArray();
              jsonGenerator.writeBooleanField("State", false);
            jsonGenerator.writeEndObject();//endDoor
            //moreDoorsGoHere
          jsonGenerator.writeEndArray();//EndDoors
          jsonGenerator.writeStringField("Passcode", "1324");
          jsonGenerator.writeArrayFieldStart("Users");//StartUsers
            jsonGenerator.writeStartObject("User");//StartUser1
              jsonGenerator.writeStringField("Username", "blucas");
              jsonGenerator.writeStringField("Password", "Phantom1");
            jsonGenerator.writeEndObject();//endUser1
            //more users go here.
          jsonGenerator.writeEndArray();//EndUsers
        jsonGenerator.writeEndObject();//EndHose
        //moreHousesGoHere
      jsonGenerator.writeEndArray();//EndHouses
      //End Route Object
      jsonGenerator.writeEndObject();

      jsonGenerator.flush();
      jsonGenerator.close();
  }
}