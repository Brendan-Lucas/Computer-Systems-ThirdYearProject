package Server;

import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;



public class House {
	private List<Door> doors;
	private List<User> users;
	private String passcode;

	public House(){
		this(new ArrayList<Door>(), new ArrayList<User>());
	}

	public House(ArrayList<Door> doors, ArrayList<User> users){
		this(doors, users, "1324");
	}

	public House(ArrayList<Door> doors, ArrayList<User> users, String passcode){
		this.doors = doors;
		this.users = users;
		this.passcode = passcode;
	}

	public String getPasscode(){
		return this.passcode;
	}

	public void setPasscode(String passcode){
		this.passcode = passcode;
	}

	public void addDoor(Door door){
		this.doors.add(door);
	}

	public void addDoor(){
		try {
			this.doors.add(new Door());
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
	}

	public List<Door> getDoors(){
		return this.doors;
	}

	public void addUser(User user){
		this.users.add(user);
	}

	public List<User> getUsers(){
		return this.users;
	}

	public boolean checkPasscode(String pass){
		return this.passcode.equals(pass);
	}

	public void setPass(String newPass){
		this.passcode = newPass;
	}

}
