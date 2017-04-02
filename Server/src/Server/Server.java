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

  private static final int PORT_NUMBER = 1400;

  /*
  * Creates new server Thread initalizes reveive socket and active requests
  */
  public Server(){
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
		    msg = new byte[100];
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
    final byte UNLOCK = (byte) 0xFF;
    final byte LOCK = 0x00;
    final byte ACK = 0x04;
    final byte PASS_MSG = 0;
    final byte IMG_MSG = 1;
    final byte D_STAT_MSG = 2;
    final byte LK_MSG = 3;
    final byte GET_DOR = (byte) 0xFF;

    public ControlThread (DatagramPacket packet)
  	{
  		this.packet=packet;
  		try {
  			sendReceiveSocket = new DatagramSocket();
  		} catch (SocketException e) {
  			e.printStackTrace();
  		}
  		System.out.println("CONTROL: new control thread");
  	}

  	public void run() {
  		byte[] msg = packet.getData();
  		//TODO: brendan Check the first two bits to decide the type where is msg is coming from
  		Houses houses = null;
  		List<Door> doors;
  		List<User> users; 		
  		ObjectMapper objectMapper = new ObjectMapper();
  		
  		try {
				houses = objectMapper.readValue(new File("database.json"), Houses.class);
			} catch (IOException e) {
				e.printStackTrace();
			}
  		//Check Valid House Number
  		//TODO:check Database for those house numbers
  		
  		
  		//door number.
  		//TODO:check Database for that door number at that house numberl.
  		//System.out.println("CONTROL: Control thread running, scanning packet"+ Arrays.toString(msg));
  		if (msg[2] == PASS_MSG) {
  			System.out.println("CONTROL: passmsg detected" + Arrays.toString(msg));
        keypadRequest(msg);
  		}else if (msg[2] == IMG_MSG) {
        imageRequest(msg);
  		}else if (msg[2] == D_STAT_MSG){
        doorStateMessage(msg);
  		}else if (msg[2] == LK_MSG){
        lockDoorMessage(msg);
      }else if (msg[2] == GET_DOR){
        respondWithDoorInfo(msg);
      }

    }

    private void keypadRequest(byte[] msg){
      System.out.println("CONTROL: keypadRequest determined:  "+ Arrays.toString(msg));
    	byte[] passcode = new byte[4];
      for(int i=3, j=0; j<passcode.length; i++, j++){
        passcode[j] = msg[i];
        if(msg[i]==0) break;
      }
      byte[] serverPass = Server.getPasscode().getBytes();
      System.out.println("CONTROL: ServerPass: " + Arrays.toString(serverPass) + ", PasswordReceived: " + Arrays.toString(passcode));
      if(Arrays.equals(passcode, serverPass)){
      	System.out.println("CONTROL: unlock building");
      	buildResponse(UNLOCK, msg, 4);
      } else{
        System.out.println("CONTROL: lock building");
      	buildResponse(LOCK, msg, 4);
      }
      try {
      	System.out.println("CONTROL: Sending response  : " + Arrays.toString(packet.getData()));
    	  sendReceiveSocket.send(responsePacket);
      } catch (IOException e) {
    	  e.printStackTrace();
      }
    }
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
      final int NOT_FOUND = -1;
      int index = NOT_FOUND;
    	while (index <= 3){

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
  					full = full!= null? Helpers.concat(full, data) : data;
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
    	displayImage(img);

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

    private void doorStateMessage(byte[] msg){
      if(msg[3] == 0xFF) {
        System.out.println("CONTROL: Door Locked");
      } else if(msg[3] == 0x00) {
        System.out.println("CONTROL: Door Unlocked");
      }
    }

    private void lockDoorMessage(byte[] msg){
      return;
    }

    private void respondWithDoorInfo(byte[] msg){
      return;
    }

    private void buildResponse(byte key, byte[] msg, int length){
      byte[] responseMsg = new byte[length];
      responseMsg[0] = msg[0];
      responseMsg[1] = msg[1];
      responseMsg[2] = msg[2];
      responseMsg[3] = key;
      responsePacket = new DatagramPacket(responseMsg, responseMsg.length, this.packet.getAddress(), this.packet.getPort());
    }
  }

  public static void main(String[] args){
  	Server server = new Server();
  	server.start();
  }
}
