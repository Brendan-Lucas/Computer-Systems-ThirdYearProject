import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Arrays;

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
      	buildResponse(UNLOCK, msg);
      } else{
        System.out.println("CONTROL: lock building");
      	buildResponse(LOCK, msg);
      }
      try {
      	System.out.println("CONTROL: Sending response  : " + Arrays.toString(packet.getData()));
    	  sendReceiveSocket.send(responsePacket);
      } catch (IOException e) {
    	  e.printStackTrace();
      }
    }
    private void imageRequest(byte[] msg){
      return;
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

    private void buildResponse(byte key, byte[] msg){
      byte[] responseMsg = new byte[100];
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
