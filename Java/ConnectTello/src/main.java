import java.io.*;
import java.net.*;
import java.nio.charset.*;
import java.util.Scanner;

class main
{
   public static void main(String args[]) throws Exception
   { 
	   String responseSentence= "";
	    Scanner scanner = new Scanner(System.in, "UTF-8");
	    DatagramSocket clientSocket = new DatagramSocket();
		  
	    InetAddress IPAddress = InetAddress.getByName("192.168.10.1");
		  
	    System.out.println("Connected to Tello");
		  
	    byte[] sendData = null;
	    byte[] receiveData = new byte[256];
	      	  
	    String sentence = "command";
		System.out.println("command");
	    sendData = sentence.getBytes();
	    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	    clientSocket.send(sendPacket);
		   
	    //DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
	    //clientSocket.receive(receivePacket);
	          		  	       		 
Thread.sleep(50);

System.out.println("takeoff");
	     sentence = "takeoff";
		 		
	    sendData = sentence.getBytes();
	     sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	    clientSocket.send(sendPacket);
	    
	    clientSocket.close();
   }
}