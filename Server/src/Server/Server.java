package Server;
import java.awt.FlowLayout;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

import java.net.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Vector;
import java.util.HashMap;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public class Server extends Thread{
  private static String passcode = "1324";
  private DatagramSocket receiveSocket;
  private ArrayList<ControlThread> activeRequests;
  public static boolean verbose;
  private static final int PORT_NUMBER = 1400;
  protected static Vector file = new Vector();
  protected static InetAddress androidAddress;
  /*
  * Creates new server Thread initalizes reveive socket and active requests
  */
  public Server(){
  	this.verbose = true;
  	System.out.println("SERVER: Server started.");
    activeRequests = new ArrayList<ControlThread>();
    try{
      receiveSocket = new DatagramSocket(PORT_NUMBER);
    } catch (SocketException e){
      e.printStackTrace();
    }
  }

  public void run(){
	  byte[] msg;
	  DatagramPacket receivePacket;
		while(true){
		    System.out.println("SERVER: waiting..\n");
		    msg = new byte[8];
		    receivePacket = new DatagramPacket(msg, msg.length);
		    try {
		      receiveSocket.receive(receivePacket);
		    } catch(IOException e){
		      e.printStackTrace();
		    }
		    System.out.println("SERVER: Request Received"+ Arrays.toString(receivePacket.getData()));
		    addActiveRequest(new ControlThread(receivePacket));
		}
  }
  public void addActiveRequest(Thread request){
    activeRequests.add((ControlThread)request);
    request.start();
  }
  public static String getPasscode(){
    return passcode;
  }


  private class ControlThread extends Thread {
		private DatagramPacket responsePacket;
		private DatagramPacket packet;
		private DatagramSocket sendReceiveSocket;
		final byte ACK = 0x04;
		final byte ACCEPT = (byte) 0x00;
		final byte REJECT = (byte) 0xFF;
		final byte PASS_MSG = (byte) 0x00;
		final byte IMG_MSG = (byte) 0x01;
		final byte D_STAT_MSG = (byte) 0x02;
		final byte LK_MSG = (byte) 0x03;
		final byte GET_DOR = (byte) 0x04;
		final byte ANDROID_ADDRESS = (byte) 0xFF;
		final int WKP = 1400; // WELL KNOWN PORT
		final int minPacketLength = 4;
		int houseNum;
		int doorNum;
    
    public ControlThread(DatagramPacket packet){
    	this.packet=packet;
  		try {
  			sendReceiveSocket = new DatagramSocket();
  		} catch (SocketException e) {
  			e.printStackTrace();
  		}
  		this.houseNum = this.packet.getData()[0]-1;
  		this.doorNum = this.packet.getData()[1]-1;
  		System.out.println("CONTROL: new control thread");
    }

    
  	public void run() {

  		byte[] msg = packet.getData();
  		Houses houses = null;
  		ObjectMapper objectMapper = new ObjectMapper();
  		
  		synchronized(Server.file){
	  		try {
					houses = objectMapper.readValue(new File("database.json"), Houses.class);
				} catch (IOException e) {
					e.printStackTrace();
				}
  		
	  		
	  		//Check Valid House Number
	  		if(houses.getHouses().get(houseNum) == null){
	  			if(Server.verbose) System.out.println("CONTROL: INACTIVE HOUSE NUMBER, IGNORING REQUEST");
	  			return;
	  		}
	      if(Server.verbose) System.out.println("CONTROL: HOUSE NUMBER CHECKED AND IS VALID");
	  		//Check Valid Door Number
	  		if(houses.getHouses().get(houseNum).getDoors().get(doorNum) == null){
	  			if(Server.verbose) System.out.println("CONTORL: INACTIVE DOOR NUMBER, IGNORING REQUEST");
	  			return;
	  		}
	      if(Server.verbose) System.out.println("CONTROL: DOOR NUMBER CHECKED AND IS VALID");
	
	  		if(Server.verbose) System.out.println("CONTROL: Control thread running, scanning packet"+ Arrays.toString(msg));
	  		Door door = houses.getHouses().get(houseNum).getDoors().get(doorNum);
	  		if (msg[2] == PASS_MSG) {
	  			if(Server.verbose) System.out.println("CONTROL: passmsg detected" + Arrays.toString(msg));
	  			keypadRequest(msg, houses.getHouses().get(houseNum));
	  			storeRequest(door, msg);
	  		}
	  		else if (msg[2] == IMG_MSG) {
	  			imageRequest(msg);
	  			storeRequest(door, msg);
	  		}
	  		else if (msg[2] == D_STAT_MSG){
	  			doorStateMessage(door, houses.getHouses().get(houseNum), msg);
	  			storeRequest(door, msg);
	  		}
	  		else if (msg[2] == LK_MSG){
	  			lockDoorMessage(door, msg);
	  			storeRequest(door, msg);
	  		}
	  		else if (msg[2] == GET_DOR){
	  			respondWithDoorInfo(door, msg);
	  			storeRequest(door, msg);
	  		}
	  		else if (msg[2] == ANDROID_ADDRESS){
	  			storeUserAndroidAddress(houses.getHouses().get(houseNum), msg);
  			}
	  		
	  		try {
					objectMapper.writeValue(new File("database.json"), houses);
				} catch (IOException e) {
					e.printStackTrace();
				}
  		}//EndSynchronized
    
  	}//EndRun

  	/*
  	 * Receives passcode entry from door and checks it agianst stored passcode for the house
  	 * Resends a packet to exactly where it came from port and address containing a byte 
  	 * indicating weather the passcode received was correct 
  	 */
		private void keypadRequest(byte[] msg, House house){
      System.out.println("CONTROL: keypadRequest determined:  "+ Arrays.toString(msg));
    	byte[] passcode = new byte[4];
      for(int i=3, j=0; j<passcode.length; i++, j++){
        passcode[j] = msg[i];
        if(msg[i]==0) break;
      }

      System.out.println("CONTROL: ServerPass: " + house.getPasscode() + ", PasswordReceived: " + new String(passcode));

      if(house.checkPasscode(new String(passcode))){
      	System.out.println("CONTROL: Accepted Response");
      	buildResponse(ACCEPT, msg, 4);
      } else{
        System.out.println("CONTROL: Rejected Response");
      	buildResponse(REJECT, msg, 4);
      }
      
      try {
      	System.out.println("CONTROL: Sending response  : " + Arrays.toString(packet.getData()));
    	  sendReceiveSocket.send(responsePacket);
      } catch (IOException e) {
    	  e.printStackTrace();
      }
    }

		/*
		 * sends from door to Server, then transfers that image to the android application. 
		 */
		private void imageRequest(byte[] msg){
    	byte[] receiveBuff = new byte[Helpers.packetLength];
      byte[] data = new byte[Helpers.packetLength-Helpers.opcodeLength];
      byte[] full = null;
      byte[] ack = {0,ACK,0,0};
      DatagramPacket receiveImage;
      DatagramPacket ackPacket;
      InetAddress clientAddress = this.packet.getAddress();
      int clientPort = this.packet.getPort();
      System.out.println("CONTROL: clientPort = "+clientPort+", clientAddress = "+clientAddress);
    	int lastPacket = 0;
    	int packetNum = 0;
      //send  initial Ack
    	System.out.println("CONTROL: image request determined " + Arrays.toString(msg));
    	ackPacket = new DatagramPacket(ack, ack.length, clientAddress, clientPort);
    	try {
				sendReceiveSocket.send(ackPacket);
			} catch (IOException e) {
				e.printStackTrace();
			}
      //begin receive send cycle
      final int NOT_FOUND = 0;
      int index = NOT_FOUND;
    	while (index < 5){

	    	System.out.println("CONTROL: waiting to recieve image ");
	    	receiveBuff = new byte[Helpers.packetLength];
	    	receiveImage = new DatagramPacket(receiveBuff, receiveBuff.length);
	    	try {
	    		sendReceiveSocket.receive(receiveImage);
          System.out.println("CONTROL: Received imagePacket");
	    	} catch (IOException e){
	    		e.printStackTrace();
	    	}
        //check to ensure packet coming from right place
        System.out.println("CONTROL: recieved from port: "+receiveImage.getPort()+", and address: "+receiveImage.getAddress());
        if(receiveImage.getPort() == clientPort && receiveImage.getAddress().equals(clientAddress)){
  	    	packetNum = ((receiveBuff[2] & 0xff) << 8) | (receiveBuff[3] & 0xff);
          System.out.println("CONTROL: received packet number: " + packetNum);
  	    	if(packetNum == 1+lastPacket){
            //TODO: make this functional
  	    		if (receiveBuff[1]==0) break;  //special opcode to indicate message finished,
  	    		data = new byte[Helpers.packetLength-Helpers.opcodeLength];
  					for(int i = 0, j = Helpers.opcodeLength; i < data.length && j < receiveBuff.length ; i++, j++)
  					{
  						data[i] = receiveBuff[j];
  						if (data[i] == 0x00){
  							index++;
  						} else {
  							index = NOT_FOUND;
  						}

  					}
  					if(full!= null){
  						full = Helpers.concat(full, data);
  					} else { 
  						full = data;
  	    			}
  					lastPacket++;
  					//build ack
  					ack[2] = receiveBuff[2];
  					ack[3] = receiveBuff[3];
  					System.out.println("CONTROL: Sending Ack: " + ack[2] + " , " + ack[3]);
  					ackPacket = new DatagramPacket(ack, ack.length, clientAddress, clientPort);
          } else System.out.println("CONTROL: resending old ack:");
          try {
						sendReceiveSocket.send(ackPacket);
					} catch (IOException e) {
						e.printStackTrace();
					}
    	  }
      }
      System.out.println("CONTROL: Received Entire image in bytes. Formatting to image.");

    	BufferedImage img = null;
      	try {
			img = ImageIO.read(new ByteArrayInputStream(full));
			} catch (IOException e) {
				e.printStackTrace();
			}
        try {
            FileOutputStream fos = new FileOutputStream("output.jpg");
            fos.write(full);
            fos.close();
         } catch (IOException e) {
            e.printStackTrace();
         }
         //displayImage(img);
    }


    /*
     * Receives Door state info from door at any point that door changes
     * Sends change to android users to tell the Application of the current state of the door
     */
    private void doorStateMessage(Door door, House house, byte[] msg){
      if(msg[3] == 0xFF) {
        System.out.println("CONTROL: Door Locked");
        door.setState(true);
      } else if(msg[3] == 0x00) {
        System.out.println("CONTROL: Door Unlocked");
        door.setState(false);
      }
      //update android application with state of the door
      for( User user : house.getUsers()){
      	buildResponse(msg[3], msg, minPacketLength, user.getAddress(), WKP); 
      	try {
					sendReceiveSocket.send(responsePacket);
				} catch (IOException e) {
					e.printStackTrace();
				}
      }
    }

    /*
     * Method accepts params Door and byte[] message, Door info comes from HouseNum->DoorNum from packet 
     * message bytes are bytes received in original UDP message to server
     * this method is expected to be called by android or web clients to send a message to the doors telling them to lock or unlock themselves. 
     */
    private void lockDoorMessage(Door door, byte[] msg){
    	
    		buildResponse(msg[3], msg, minPacketLength, door.getAddress(), WKP);
    		
    		try {
					sendReceiveSocket.send(responsePacket);
				} catch (IOException e) {
					e.printStackTrace();
				}
    		
    		buildResponse((byte)0x00, msg, minPacketLength);
    		try {
    			sendReceiveSocket.send(responsePacket);
    		} catch (IOException e){
    			e.printStackTrace();
    		}
    
    }
    /*
     * Method accepts params Door and Byte message, These come from the packet that was sent to the server,
     * the door is representative of the door indicated by House number -> Door number.
     * This method is expected to be called by external clients such as android or desktop applications. 
     * Sends the information back to where it came from both address and port
     */
    private void respondWithDoorInfo(Door door, byte[] msg){
      System.out.println("CONTROL: Door Info sending ");
      byte doorState = door.getState()? (byte)0x00: (byte)0xFF;
      //sends to place where we got the packet with the weather the door is locked(0xFF) or unlocked(0x00)
      buildResponse(doorState, msg, 4);
    	try {
				sendReceiveSocket.send(responsePacket);
			} catch (IOException e) {
				e.printStackTrace();
			}
    }
    /*
     * this method is intended to store the address of the android client based on username
     * so that it can be used for future sending of door state updates. 
     */
    private void storeUserAndroidAddress(House house, byte[] msg) {
    	byte[] usernameBytes = new byte[10];
    	for (int i=0, j = 3; i<usernameBytes.length && j<msg.length && msg[j]!=0; i++, j++){
    		usernameBytes[i] = msg[j];
    	}
    	if(house.getUsers().contains(new String(usernameBytes))){
    		int userIndex = house.getUsers().indexOf(new String(usernameBytes));
    		house.getUsers().get(userIndex).setAddress(packet.getAddress());
    	}
    	//TODO: could implement add users here
			
		}
    //TODO: implement door port differences
    private void buildResponse(byte key, byte[] msg, int length){
    	buildResponse(key, msg, length, this.packet.getAddress(), this.packet.getPort());
    }
    
    private void buildResponse(byte key, byte[] msg, int length, InetAddress address, int port){
    	byte[] responseMsg = new byte[length];
      responseMsg[0] = msg[0];
      responseMsg[1] = msg[1];
      responseMsg[2] = msg[2];
      responseMsg[3] = key;
      //TODO: implement door diffs here;;;;
      responsePacket = new DatagramPacket(responseMsg, responseMsg.length, address, port);
    }
    
    public void displayImage(BufferedImage img){
	    ImageIcon icon = new ImageIcon(img);
	  	JFrame frame = new JFrame();
	  	frame.setLayout(new FlowLayout());
	  	frame.setSize(200, 300);
	  	JLabel label = new JLabel();
	  	label.setIcon(icon);
	  	frame.add(label);
	  	frame.setVisible(true);
	  	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    private void storeRequest(Door door, byte[] msg) {
    	door.getRequests().add(Arrays.toString(msg));
		}
  }

  public static void main(String[] args){
  	Server server = new Server();
  	server.start();
  }
}
