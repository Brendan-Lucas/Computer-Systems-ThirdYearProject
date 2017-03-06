import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Arrays;

public class Server extends Thread{
  private static String passcode = "1324";
  private DatagramSocket receiveSocket;
  private ArrayList<Thread> activeRequests;

  private static final int PORT_NUMBER = 1400;

  /*
  * Creates new server Thread initalizes reveive socket and active requests
  */
  public Server(){
    activeRequests = new ArrayList<Thread>();
    try{
      receiveSocket = new DatagramSocket(PORT_NUMBER);
    } catch (SocketException e){
      e.printStackTrace();
    }
  }
  public void run(){
	  byte[] msg = new byte[100];
	  DatagramPacket receivePacket = new DatagramPacket(msg, msg.length);
	
		while(true){
		    System.out.println("SERVER: waiting..\n");
		    try {
		      receiveSocket.receive(receivePacket);
		    } catch(IOException e){
		      e.printStackTrace();
		    }
		    System.out.println("SERVER: Request Received"+ Arrays.toString(msg));
		    addActiveRequest(new ControlThread(receivePacket));
		}
  }
  public void addActiveRequest(Thread request){
    activeRequests.add(request);
    request.start();
  }
  public static String getPasscode(){
    return passcode;
  }


  private class ControlThread extends Thread {
    private DatagramPacket responsePacket;
    private DatagramPacket packet;
    private DatagramSocket sendReceiveSocket;
  	protected boolean doorStatus;
  	protected boolean keypadRequest;
  	protected boolean imageRequest;
  	protected boolean lockDoorRequest;
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
  		doorStatus = false;
  		keypadRequest = false;
  		imageRequest = false;
  		lockDoorRequest = false;
  		System.out.println("CONTROL: new control thread");
  	}
     
  	public void run() {
  		byte[] msg = packet.getData();
      //TODO: brendan Check the first two bits to decide the type where is msg is coming from
  		//house number and door number.
  		//System.out.println("CONTROL: Control thread running, scanning packet"+ Arrays.toString(msg));
  		if (msg[2] == PASS_MSG) {
  			//System.out.println("CONTROL: passmsg detected" + Arrays.toString(msg));
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
      System.out.println("SERVER: keypadRequest determined:  "+ Arrays.toString(msg));
    	byte[] passcode = new byte[4];
      for(int i=3, j=0; j<passcode.length; i++, j++){
        passcode[j] = msg[i];
        if(msg[i]==0) break;
      }

      if(passcode.equals(Server.getPasscode().getBytes())){
        buildResponse(UNLOCK, msg);
        System.out.println("SERVER: unlock building");
      } else{
        buildResponse(LOCK, msg);
        System.out.println("SERVER: lock building");
      }
      try {
      	System.out.println("SERVER: Sending response  : " + Arrays.toString(packet.getData()));
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
        System.out.println("SERVER: Door Locked");
      } else if(msg[3] == 0x00) {
        System.out.println("SERVER: Door Unlocked");
      }
    }

    private void lockDoorMessage(byte[] msg){
      return;
    }

    private void respondWithDoorInfo(byte[] msg){
      return;
    }

    private void buildResponse(byte key, byte[] msg){
      byte[] responseMsg = new byte[4];
      responseMsg[0] = msg[0];
      responseMsg[1] = msg[1];
      responseMsg[2] = msg[2];
      responseMsg[3] = key;
      responsePacket = new DatagramPacket(responseMsg, responseMsg.length, this.packet.getAddress(), this.packet.getPort());
    }
  }
}
