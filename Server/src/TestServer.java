import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import javax.imageio.ImageIO;
import java.awt.Image;
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
  // boolean correctPasscodeSuccess;
  // boolean incorrectPasscodeSuccess;
  // boolean imageSendSuccess;
  // boolean invalidHomeSuccess;
  // boolean invalidDoorSuccess;
  // boolean createDoorSuccess;
  // boolean unlockDoorRequestRecievedSuccess;
  // boolean unlockDoorRequestSentSuccess;
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
    testImageSend();
  }

  public DatagramPacket bulidStandardRequest(byte b, String s) {
    sendMsg = new byte[100];
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

  public void testImageSend(){
    try {
			doorSocket.setSoTimeout(10000);
		} catch (SocketException e1) {
			e1.printStackTrace();
		}

    DatagramPacket sendPacket = bulidStandardRequest(IMG_MSG, "");

    try {
			doorSocket.send(sendPacket);
		} catch (IOException e1) {
			e1.printStackTrace();
		}

    byte [] msg = new byte[100];
    DatagramPacket receivePacket = new DatagramPacket(msg, msg.length);

    try {
			doorSocket.receive(receivePacket);
		} catch (IOException e1) {
			e1.printStackTrace();
		}
    //parse receivedPacket for the info that we need
    System.out.println("TEST: Received: "+ Arrays.toString(receivePacket.getData()));
  	BufferedImage img = null;
		try {
			img = ImageIO.read(new File("Server/embarassingPhotoOfBrendan.jpg"));
		} catch (IOException e) {
			e.printStackTrace();
		}
  	ByteArrayOutputStream baos = new ByteArrayOutputStream();
  	try {
			ImageIO.write(img, "jpg", baos);
		} catch (IOException e) {
			e.printStackTrace();
		}
  	try {
			baos.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}

  	byte[] imgArr = baos.toByteArray();
  	System.out.println("TEST: image size in bytes: " + imgArr.length);
    //sending img in many packets
    byte[] buf;
  	DatagramPacket imagePacket=null;
  	byte[] writeOP = {0,3,0,1};
  	for(int i = 0, j=Helpers.packetLength-Helpers.opcodeLength, k=1; j<imgArr.length; k++, i+=j, j+= j+(Helpers.packetLength-Helpers.opcodeLength)>=imgArr.length? (imgArr.length-1)-j : Helpers.packetLength){
      writeOP[2] = (byte)(k/Helpers.maxByteSize);
  		writeOP[3] = (byte)(k%Helpers.maxByteSize);
      System.out.println("TEST: i: "+ i + ", j: "+ j+"\nMsg#: " + writeOP[2] + ", " + writeOP[3]);
  		buf = Helpers.concat( writeOP, Arrays.copyOfRange(imgArr, i, j));
  		imagePacket = new DatagramPacket(buf, buf.length, receivePacket.getAddress(), receivePacket.getPort());
  		do{
        System.out.println("TEST: outgoing:" + buf[2] + ", " + buf[3]);
	  		try {
	    		doorSocket.send(imagePacket);
	    	} catch (IOException e){
	    		e.printStackTrace();
	    	}
	  		msg = new byte[4];
	  		try {
	  			doorSocket.receive(receivePacket);
	  		}catch(IOException e) {
	  			e.printStackTrace();
	  		}
        if (msg[2] == k/255 && msg[3]==k%255)
          System.out.println("TEST: Successful ack recieved: " + msg[2] + ", "+ msg[3]);
        else
          System.out.println("TEST: ack: " + msg[2] + ", " + msg[3] + " recieved, resending packet.");
  		}while(msg[2]!=k/255 || msg[3]!=k%255);
  	}
  	//TODO: Receive successful or unsuccessful command.
  }

  public static void main(String[] args){
  	TestServer test = new TestServer();
  	test.start();
    }
}
