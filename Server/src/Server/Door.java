package Server;

import java.util.List;
import java.util.ArrayList;

public class Door {
	private boolean state;
	private List<String> requests;
	
	public Door(){
		this(false);
	}
	public Door(boolean state){
		this.state = state;
		this.requests = new ArrayList<String>();
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
}
