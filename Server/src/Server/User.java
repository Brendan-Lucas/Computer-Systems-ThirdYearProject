package Server;

import java.net.InetAddress;
import java.net.UnknownHostException;

public class User {

	private String username;
	private String password;
	private InetAddress address;
	public User(){
		this("","");
	}

	public User(String username, String password){
		this.username = username;
		this.password = password;
		try {
			this.address = InetAddress.getLocalHost();
		} catch (UnknownHostException e) {
		}
		
	}

	public User(String username, String password, String address){
		this.username = username;
		this.password = password;
		try {
			this.address = InetAddress.getByName(address);
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
	}
	
	public User(String username, String password, InetAddress address){
		this.username = username;
		this.password = password;
		this.address = address;
	}
	
	public String getUsername(){
		return this.username;
	}

	public String getPassword(){
		return this.password;
	}
	
	public InetAddress getAddress(){
		return this.address;
	}
	
	public void setAddress(InetAddress address){
		 this.address = address;
	}
	
	public boolean updatePassword(String username, String oldPass, String newPass){
		if (this.username.equals(username) && this.password.equals(oldPass)){
			this.password = newPass;
			return true;
		}
		return false;
	}

	public boolean checkPassword(String username, String password){
		if (this.username.equals(username) && this.password.equals(password)){
			return true;
		}
		return false;
	}
	
	@Override
	public boolean equals(final Object user){
		if( user instanceof String){
			return this.username.equals( (String) username);
		}else if (user instanceof User){
			return this.username.equals(((User) user).getUsername());
		}
		return false;	
	}


}
