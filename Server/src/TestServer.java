import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;

public class TestServer extends Thread{
  final int SERVER_PORT = 1400;
  final byte PASS_MSG = 0;
  final byte IMG_MSG = 1;
  final byte D_STAT_MSG = 2;
  final byte LK_MSG = 3;
  //TODO: add the rest of the oppcodes.
  boolean[] tests;
  boolean correctPasscodeSuccess;
  boolean incorrectPasscodeSuccess;
  boolean imageSendSuccess;
  boolean invalidHomeSuccess;
  boolean invalidDoorSuccess;
  boolean createDoorSuccess;
  boolean unlockDoorRequestRecievedSuccess;
  boolean unlockDoorRequestSentSuccess;
  //NOTE: Maybe have opcode for all doors in house for general requests from webclients to be 0000;
  final String CORRECT_PASS = "1324";
  final String INCORRECT_PASS = "1234";
  InetAddress LOCAL_HOST;
  byte[] sendMsg;
  Server server;

  DatagramSocket doorSocket;
  DatagramSocket webclientSocket;

  public TestServer() {
      this.sendMsg = new byte[100];
      this.tests = new boolean[8];
      try {
      	this.webclientSocket = new DatagramSocket();
				this.doorSocket = new DatagramSocket();
			} catch (SocketException e1) {
				e1.printStackTrace();
			}
      try{
      	LOCAL_HOST = InetAddress.getLocalHost();
      } catch (UnknownHostException e){
      	e.printStackTrace();
      }
      Server server = new Server();
      server.start();
      System.out.println("TEST: Server started");
  }

  public void run(){
    System.out.println("TEST: Test Server receive Message to unlock door from webclient");
    //TEST: Correct Passcode
    try {
			testPasscode(CORRECT_PASS, "Correct Passcode Test: ", 0, (byte)0xFF);
		} catch (IOException e) {
			e.printStackTrace();
		} 
    //TEST: Incorrect Passcode
    try {
			testPasscode(INCORRECT_PASS, "Incorect Passcode Test: ",1, (byte)0);
		} catch (IOException e) {
			e.printStackTrace();
		}
    //TEST: Image Request
    
    doorSocket.setSoTimeout(10000);
    
    DatagramPacket sendPacket = bulidStandardRequest(IMG_MSG, "");
    
    doorSocket.send(sendPacket);
   
    byte [] msg = new byte[100];
    DatagramPacket receivePacket = new DatagramPacket(msg, msg.length);
    
    doorSocket.receive(receivePacket);
    //parse receivedPacket for the info that we need
    System.out.println("TEST: Received: "+ Arrays.toString(receivePacket.getData()));
  	BufferedImage img = new ImageIO.read(new File("Server/test/embarassingPhotoOfBrendan.jpg"));
  	ByteArrayOutputStream baos = new ByteArrayOutputStream();
  	ImageIO.write(img, "jpg", baos);
  	baos.flush();
  	byte[] buf = baos.toByteArray();
  	DatagramPacket imagePacket = new DatagramPacket(buf, buf.length, receivePacket.getAddress(), receivePacket.getPort());
   
    
  }

  public DatagramPacket bulidStandardRequest(byte b, String s) {
    sendMsg[0] = 1;
    sendMsg[1] = 1;
    sendMsg[2] = b;
    if (s == null) return new DatagramPacket(sendMsg, sendMsg.length, LOCAL_HOST, SERVER_PORT);
    byte[] tempBytes = s.getBytes(StandardCharsets.UTF_8);
    int j=0;
    for(int i = 3; j<tempBytes.length; i++){
      sendMsg[i] = tempBytes[j++];
    }
    return new DatagramPacket(sendMsg, sendMsg.length, LOCAL_HOST, SERVER_PORT);
  }

  private void testPasscode(String pass, String out, int i, byte expected) throws IOException, SocketException{
  	byte[] rcvMsg = new byte[100];
    DatagramPacket receivePacket = new DatagramPacket(rcvMsg, rcvMsg.length);
  	DatagramPacket testPacket = bulidStandardRequest(PASS_MSG, pass);
		doorSocket.setSoTimeout(10000);
		doorSocket.send(testPacket);
		System.out.println("TEST: Packet sent");
    //NOTE: server has to send to receiveMsg.getPort()
    doorSocket.receive(receivePacket);
    System.out.println("TEST: packetReceived: "+Arrays.toString(rcvMsg));
    tests[i] = rcvMsg[3]==expected;
    System.out.println("TEST: "+out);
    if(tests[i]) System.out.println("TEST: Success");
    else System.out.println("TEST: Failed");
  }
  
  public static void main(String[] args){
  	TestServer test = new TestServer();
  	test.start();
    }
}
