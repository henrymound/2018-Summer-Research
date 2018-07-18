import java.io.*;
import java.net.*;
import java.nio.charset.*;
import java.util.Scanner;

public class main {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub

    String sentence = "";
    String responseSentence= "";
    Scanner scanner = new Scanner(System.in, "UTF-8");
    DatagramSocket clientSocket = new DatagramSocket();
	  
    InetAddress IPAddress = InetAddress.getByName("TELLO-C47FD9");
	  
    System.out.println("Connected to Tello.");
	  
    byte[] sendData = null;
    byte[] receiveData = new byte[256];
      	  
    while (!sentence.equals("bye")){
       System.out.print("Command: ");       
       sentence = scanner.nextLine();
	 		
       sendData = sentence.getBytes();
       DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
       clientSocket.send(sendPacket);
	   
       DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
       clientSocket.receive(receivePacket);
      
       responseSentence = new String(receivePacket.getData(), StandardCharsets.UTF_8);
	  	   
       System.out.println("Tello:" + responseSentence);
      }//end while
	  
    clientSocket.close();
   }
}