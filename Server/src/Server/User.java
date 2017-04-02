package Server;

public class User {

	private String username;
	private String password;

	public User(){
		this("","");
	}

	public User(String username, String password){
		this.username = username;
		this.password = password;
	}

	public String getUsername(){
		return this.username;
	}

	public String getPassword(){
		return this.password;
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


}
