import java.net.*;
import java.io.*;

public class TestServer extends Thread{
  final int SERVER_PORT = 1400;
  final byte PASS_MSG = 0;
  final byte IMG_MSG = 1;
  final byte D_STAT_MSG = 2;
  final byte LK_MSG = 3;
  //TODO: add the rest of the oppcodes.
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
  byte[] sendMsg;
  InetAddress LOCAL_HOST = InetAddress.getLocalHost();
  Server server;

  DatagramSocket doorSocket;
  DatagramSocket webclientSocket;

  public TestServer() {
      this.server = new Server();
      this.webclientSocket = new DatagramSocket();
      this.doorSocket = new DatagramSocket();
      sendMsg = new byte[100];

      server.start();
  }


  public void bulidStandardRequest(byte b, String s) {
    sendMsg[0] = 1;
    sendMsg[1] = 1;
    sendMsg[2] = b;
    if (s == null) return;
    byte[] tempBytes = s.getBytes();
    int j=0;
    for(int i = 3; i<tempBytes.length; i++){
      sendMsg[i] = tempBytes[j++];
    }

  }

  public void run(){
    byte[] rcvMsg = new byte[512];
    DatagramPacket recievePacket = new DatagramPacket(rcvMsg, rcvMsg.length);

    System.out.println("Test Server recieve Message to unlock door from webclient");

    //Test Correct Passcode
    bulidStandardRequest(PASS_MSG, CORRECT_PASS);
    DatagramPacket testPacket = new DatagramPacket(sendMsg, sendMsg.length, LOCAL_HOST, SERVER_PORT);
    doorSocket.setSoTimeout(10000);
    doorSocket.send(testPacket);
    //NOTE: server has to send to receiveMsg.getPort()
    doorSocket.receive(recievePacket);
    correctPasscodeSuccess = rcvMsg[3]==1;
    System.out.println("Correct Passcode Test: ");
    if(correctPasscodeSuccess) System.out.println("Success");
    else System.out.println("Failed");

    //TEST incorect Passcode
    bulidStandardRequest(PASS_MSG, INCORRECT_PASS);
    testPacket = new DatagramPacket(sendMsg, sendMsg.length, LOCAL_HOST, SERVER_PORT);
    rcvMsg = new byte[512];
    doorSocket.setSoTimeout(10000);
    doorSocket.send(testPacket);
    //NOTE: server has to send to receiveMsg.getPort()
    doorSocket.receive(recievePacket);
    incorrectPasscodeSuccess = rcvMsg[3]==0;
    System.out.println("Incorect Passcode Test: ");
    if(correctPasscodeSuccess) System.out.println("Success");
    else System.out.println("Failed");
  }
  
}
