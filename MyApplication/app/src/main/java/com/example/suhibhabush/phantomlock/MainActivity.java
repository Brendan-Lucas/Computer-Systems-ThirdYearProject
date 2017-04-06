package com.example.suhibhabush.phantomlock;

import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.*;
import java.net.*;
import java.security.Timestamp;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutionException;

import android.os.AsyncTask;


public class MainActivity extends AppCompatActivity {
    //TODO: Add image request, add multiple doors
    //private String hostName = "99.248.222.229";
    private String hostName = "10.0.2.2";
    private InetAddress hostAddress;
    //TODO: external ip address of the pi or internal if we doing it thru the local network
    private static final int portnumber = 1400;
    private static final String debugString = "debug";
    public byte housenumber = 0x01;
    public byte doornumber = 0x01;
    public final byte UNLOCK = (byte) 0xFF;
    public final byte LOCK = 0x00;
    public final byte PASS_MSG = 0;
    public final byte IMG_MSG = 1;
    public final byte D_STAT_MSG = 2;
    public final byte LK_MSG = 3;
    public final byte GET_DOR = (byte) 0xFF;
    public DatagramSocket socket;
    private TextView tvDoorStatus;
    public final static String eventString = "Door doornum was ";
    public List<String> eventArrayList;
    public boolean currentDoorState;
    public ArrayAdapter<String> adapter;
    private DatagramPacket sendPacket, receivePacket;
    private runUdpClient sendReceiveTask;
    public String username = "suhaib";
    public Receive receiveTask;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        CreateAddress addressGetter = new CreateAddress();
        try {
            hostAddress = addressGetter.execute(hostName).get();
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("Finished previous hickup");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        currentDoorState = true;
        eventArrayList = new ArrayList<String>();

        tvDoorStatus = (TextView) findViewById(R.id.tvDoorStatus);
        ListView listView = (ListView) findViewById(R.id.lvRecAct);
        final ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, eventArrayList);
        listView.setAdapter(adapter);


        //Connecting
        eventArrayList.add(0, (getCurrentTimeStamp() + "App Launched."));
        //initialize text view with doorstatus
        //updateDoorStatus(requestDoorStatus());

        sendReceiveTask = new runUdpClient();
        receiveTask = new Receive();
        //receiveTask.execute();
        byte[] udpMsg1 = {(byte) housenumber, (byte) doornumber, (byte) 0xFF};
        byte[] udpMsg2 = username.getBytes();
        byte[] udpMessage = new byte[udpMsg1.length + udpMsg2.length];
        System.arraycopy(udpMsg1, 0, udpMessage, 0, udpMsg1.length);
        System.arraycopy(udpMsg2, 0, udpMessage, udpMsg1.length, udpMsg2.length);
        System.out.println(hostAddress);
        sendPacket = new DatagramPacket(udpMessage, udpMessage.length, hostAddress, portnumber);
        DatagramPacket receivePacket = null;
        try {
            receivePacket = sendReceiveTask.execute(sendPacket).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }

        Button btnLock = (Button) findViewById(R.id.btnLock);
        btnLock.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                runUdpClient sendReceive = new runUdpClient();
                byte[] udpMsg = {(byte) housenumber, (byte) doornumber, LK_MSG, UNLOCK};
                System.out.println(hostAddress);
                sendPacket = new DatagramPacket(udpMsg, udpMsg.length, hostAddress, portnumber);
                DatagramPacket receivePacket = null;



                //currentDoorState = (receivePacket.getData()[3] == UNLOCK);
                //


            }
        });


        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
    }

    public void updateLockState(byte[] msg){
        currentDoorState = (msg[3]==UNLOCK);
        updateDoorStatus(currentDoorState);
        int doorNum = doornumber;
        eventArrayList.add(0, (getCurrentTimeStamp() + eventString.replace("doornum", Integer.toString(doorNum))) + ((currentDoorState) ? "unlocked." : "locked."));
        adapter.notifyDataSetChanged();

    }

    private boolean requestDoorStatus() {
        byte[] sendMsg = new byte[100];
        byte[] recMsg = new byte[100];
        sendMsg[0] = housenumber;
        sendMsg[1] = doornumber;
        sendMsg[2] = GET_DOR;

        DatagramPacket sendPacket;
        DatagramPacket receivePacket;
        receivePacket = new DatagramPacket(recMsg, recMsg.length);

        try {
            sendPacket = new DatagramPacket(sendMsg, sendMsg.length, hostAddress, portnumber);
            socket.send(sendPacket);
            socket.receive(receivePacket);
        } catch (Exception e) {
            e.printStackTrace();
        }

        byte[] receiveMsg = receivePacket.getData();
        return (receiveMsg[3] == UNLOCK);
    }

    private void updateDoorStatus(boolean isUnlocked) {
        if (isUnlocked) {
            tvDoorStatus.setText("Unlocked");
        } else {
            tvDoorStatus.setText("Locked");
        }
    }

    public static String getCurrentTimeStamp() {
        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//dd/MM/yyyy
        Date now = new Date();
        String strDate = sdfDate.format(now);
        return ("[" + strDate + "] ");
    }



    private class runUdpClient extends AsyncTask<DatagramPacket, Void, DatagramPacket> {

        @Override
        protected DatagramPacket doInBackground(DatagramPacket... params) {

            DatagramSocket ds = null;
            //SEND
            try {
                ds = new DatagramSocket();
                DatagramPacket dp;
                //dp = new DatagramPacket(udpMsg.getBytes(), udpMsg.length(), hostAddress, portnumber);
                dp = params[0];
                ds.send(dp);
            } catch (SocketException e) {
                e.printStackTrace();
            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (Exception e) {
                e.printStackTrace();
            }
            //RECEIVE
            DatagramPacket incomingPacket = new DatagramPacket(new byte[100], 100);
            try {
                ds.setSoTimeout(1000);
            } catch (SocketException e) {
                e.printStackTrace();
            }
            try {
                ds.receive(incomingPacket);
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (ds != null) ds.close();
            }
            System.out.println("Packet recieved from server" + Arrays.toString(incomingPacket.getData()));
            return incomingPacket;
        }

    }


    private class Receive extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            DatagramSocket receiveSocket = null;
            DatagramPacket receivePacket = null;
            try {
                receiveSocket = new DatagramSocket(portnumber);
            } catch (SocketException e) {
                e.printStackTrace();
            }
            while (true){

                receivePacket = new DatagramPacket(new byte[100], 100);

                try {
                    receiveSocket.receive(receivePacket);
                } catch (IOException e){
                    e.printStackTrace();
                };


                addThread(receivePacket);
            }

        }

        private void addThread(DatagramPacket packet){
            new ControlThread().execute(packet);
        }

        private class ControlThread extends AsyncTask<DatagramPacket, Void, Void>{


            @Override
            protected Void doInBackground(DatagramPacket... params){

              if(params[0].getData()[2]==D_STAT_MSG){
                updateLockState(params[0].getData());
              }

                return null;
            }

        }
        
    }

    private class CreateAddress extends AsyncTask<String, Void, InetAddress> {

        private Exception e;

        @Override
        protected InetAddress doInBackground(String... params) {
            try {

                return InetAddress.getByName(params[0]);
            } catch (UnknownHostException e) {
                e.printStackTrace();
            }
            System.out.println("ANDROID: FUCKING UP BAD ");
            return null;
        }
    }
}
