package Server;

import java.util.List;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;

public class Door {
	
	private final static String DEFAULT_ADDRESS = "10.0.0.20";
	private boolean state;
	private List<String> requests;
	private InetAddress address; 
	public Door() throws UnknownHostException{
		this(false, DEFAULT_ADDRESS);
	}
	
	public Door(boolean state, String address) throws UnknownHostException{
		this(state, InetAddress.getByName(address)); 
	}
	
	public Door(boolean state, InetAddress address){
		this.state = state;
		this.requests = new ArrayList<String>();
		this.address = address;
	}
	
	public void addRequest(String request){
		this.requests.add(request);
	}
	
	public List<String> getRequests(){
		return this.requests;
	}
	
	public void setState(boolean state){
		this.state = state;
	}
	
	public boolean getState(){
		return this.state;
	}
	
	public InetAddress getAddress(){
		return this.address;
	}
}
