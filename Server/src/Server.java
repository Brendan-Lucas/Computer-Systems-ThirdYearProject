import java.awt.FlowLayout;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Arrays;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

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
  		//house number and door number.
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
    	byte[] receiveBuff = new byte[1024];
      byte[] data = new byte[1020];
      byte[] full = null;
      byte[] ack = {0,4,0,0};
      DatagramPacket receiveImage;
      DatagramPacket ackPacket;
      InetAddress clientAdress = this.packet.getAddress();
      int clientPort = this.packet.getPort();
    	int lastPacket = 0;
    	int packetNum = 0;
      //send  initial Ack
    	System.out.println("CONTROL: image request determined " + Arrays.toString(msg));
    	ackPacket = new DatagramPacket(ack, ack.length, clientAdress, clientPort);
    	try {
				sendReceiveSocket.send(ackPacket);
			} catch (IOException e) {
				e.printStackTrace();
			}
      //begin receive send cycle
      final int NOT_FOUND = -1;
      int index=NOT_FOUND;
    	while (index == NOT_FOUND){

	    	System.out.println("CONTROL: waiting to recieve image ");
	    	receiveBuff = new byte[1024];
	    	receiveImage = new DatagramPacket(receiveBuff, receiveBuff.length);
	    	try {
	    		sendReceiveSocket.receive(receiveImage);
	    	} catch (IOException e){
	    		e.printStackTrace();
	    	}
        //check to ensure packet coming from right place
        if(receiveImage.getPort() != clientPort || receiveImage.getAddress() != clientAdress){
  	    	packetNum = receiveBuff[0]*250 + receiveBuff[1];
  	    	if(packetNum == 1+lastPacket){
  	    		if (receiveBuff[0]==0) break;  //special opcode to indicate message finished,
  	    		data = new byte[1020];
            //move data in packet to buffered byte array
  					for(int i = 0, j = 4; i < data.length && j < receiveBuff.length ; i++, j++)
  					{
  						data[i] = receiveBuff[j];
  						if (data[i]==0) {
  							index = i;
                break;
  						}
            }
  					full = Helpers.concat(full, data);
            //build ack
            ack[2] = receiveBuff[2];
            ack[3] = receiveBuff[3];
            ackPacket = new DatagramPacket(ack, ack.length, clientAdress, clientPort);
          }
          try {
						sendReceiveSocket.send(ackPacket);
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
    	  }
      }
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

    private void buildResponse(byte key, byte[] msg, int packetLength){
      byte[] responseMsg = new byte[packetLength];
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
