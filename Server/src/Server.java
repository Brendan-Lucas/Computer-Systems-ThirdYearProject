import java.io.*;
import java.net.*;
import java.util.ArrayList;

public class Server extends Thread{
  private String passcode = "1324";
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
        System.out.println("Server waiting..\n");
        try {
          receiveSocket.receive(receivePacket);
        } catch(IOException e){
          e.printStackTrace();
        }
        System.out.println("Request Received");
        addActiveRequest(new ControlThread(receivePacket));
    }
  }
  public void addActiveRequest(Thread request){
    activeRequests.add(request);
    request.start();
  }
  public String getPasscode(){
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
    final byte UNLOCK = 0xFF;
    final byte LOCK = 0x00;
    final byte PASS_MSG = 0;
    final byte IMG_MSG = 1;
    final byte D_STAT_MSG = 2;
    final byte LK_MSG = 3;
    final byte GET_DOR = 0xFF;
  	public ControlThread (DatagramPacket packet)
  	{
  		this.packet=packet;
      sendReceiveSocket = new DatagramSocket();
  		doorStatus = false;
  		keypadRequest = false;
  		imageRequest = false;
  		lockDoorRequest = false;
  	}

  	public void run() {
  		byte[] msg = packet.getData();
      //TODO: brendan Check the first two bits to decide the type where is msg is comign from
  		//house number and door number.
  		if (msg[2] == PASS_MSG) {
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
      sendReceiveSocket.send(responsePacket);
    }

    private void keypadRequest(byte[] msg){
      byte[] passcode = new byte[97];
      int j=0;
      for(int i=3; i<msg.length; i++){
        passcode[j++] = msg[i];
        if(msg[i]==0) break;
      }
      if(Arrays.toString(passcode).equals(Server.getPasscode())){
        buildResponse(UNLOCK, msg);
      } else{
        buildResponse(LOCK, msg);
      }
    }
    private void imageRequest(byte[] msg){
      return;
    }

    private void doorStateMessage(byte[] msg){
      if(msg [3] == 0xFF) {
        System.out.println("Door Locked");
      } else if (msg [2] == D_STAT_MSG) && (msg [3] == 0x00) {
        System.out.println("Door Unlocked");
      }
    }

    private void lockDoorMessage(byte[] msg){
      return;
    }

    private void respondWithDoorInfo(){
      return
    }

    private void buildResponse(byte key, byte[] msg){
      //TODO: make responseMsg out of first three bytes of the recievePacket along with key
      byte[] responseMsg = new byte[4];
      responseMsg[0] = msg[0];
      responseMsg[1] = msg[1];
      responseMsg[2] = msg[2];
      responseMsg[3] = key;
      responsePacket = new DatagramPacket(responseMsg, responseMsg.length, recievePacket.getAddress(), recievePacket.getPort());
    }



  }
}
