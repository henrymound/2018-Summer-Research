import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.*;
import java.util.*;
import java.net.*;

public class main {
	
	int GRID_SIZE = 50;
	
    public static void main(String[] args) {
       
        new main();
    }

    public main() {
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException ex) {
                }

                JFrame frame = new JFrame("Tello Flight Path Planner");
                JButton deployCodeButton = new JButton("Deploy Flight");
                deployCodeButton.addActionListener(new ActionListener() { 
              	  public void actionPerformed(ActionEvent e) { 
              		    try {
							deployCodeButtonPressed();
						} catch (Exception e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
              		  } 
              		} 
              );
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.setLayout(new BorderLayout());
                frame.add(new TestPane(), BorderLayout.NORTH);
                frame.add(deployCodeButton, BorderLayout.CENTER);
                frame.pack();
                frame.setLocationRelativeTo(null);
                frame.setVisible(true);
            }
        });
    }

    public class TestPane extends JPanel {
    	
    	
        public TestPane() {
            setLayout(new GridBagLayout());

            GridBagConstraints gbc = new GridBagConstraints();
            for (int row = 0; row < GRID_SIZE; row++) {
                for (int col = 0; col < GRID_SIZE; col++) {
                    gbc.gridx = col;
                    gbc.gridy = row;

                    CellPane cellPane = new CellPane(row, col);
                    Border border = null;
                    if (row < GRID_SIZE - 1) {
                        if (col < GRID_SIZE - 1) {
                            border = new MatteBorder(1, 1, 0, 0, Color.GRAY);
                        } else {
                            border = new MatteBorder(1, 1, 0, 1, Color.GRAY);
                        }
                    } else {
                        if (col < GRID_SIZE - 1) {
                        	// For the last row
                            border = new MatteBorder(1, 1, 1, 0, Color.GRAY);
                        } else {
                            // For the bottom right corner
                        	border = new MatteBorder(1, 1, 1, 1, Color.GRAY);
                        }
                    }
                    cellPane.setBorder(border);
                    add(cellPane, gbc);
                }
            }
        }
    }


    Deque<CellPane> cellStack = new ArrayDeque<CellPane>();
    Deque<CellObject> intStack = new ArrayDeque<CellObject>();
    int CONSTANT_DISTANCE = 50;
    
    public void deployCodeButtonPressed() throws Exception {
    	
    	 System.out.println("DEPLOYING CODE");
    	 String instructionString = generateStringFromStack();
    	 System.out.println(instructionString);
    	 
    	 
    	 DatagramSocket clientSocket = new DatagramSocket();
  	     InetAddress IPAddress = InetAddress.getByName("192.168.10.1"); 
  	     System.out.println("Connected to Tello");
  		  
  	     byte[] sendData = null;
  	     byte[] receiveData = new byte[256];
  	      	  
  	     for (char ch: instructionString.toCharArray()) {  		 
   	  	    Thread.sleep(1500);
  	        String sentence = "command";
  	  		System.out.println("command");
  	  	    sendData = sentence.getBytes();
  	  	    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
  	  	    clientSocket.send(sendPacket);
  	  		      		  	     
	  	  	switch (ch) {
	        case '0': //takeoff
	        	System.out.println("takeoff");
	  	  		sentence = "takeoff";
	  	  	    sendData = sentence.getBytes();
	  	  	    sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	  	  	    clientSocket.send(sendPacket);
	            break;
	        case '2': //forward 
	        	System.out.println("forward " + CONSTANT_DISTANCE);
	  	  		sentence = "forward " + CONSTANT_DISTANCE;
	  	  	    sendData = sentence.getBytes();
	  	  	    sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	  	  	    clientSocket.send(sendPacket);
	            break;
	        case '8': //backward 
	        	System.out.println("back " + CONSTANT_DISTANCE);
	  	  		sentence = "back " + CONSTANT_DISTANCE;
	  	  	    sendData = sentence.getBytes();
	  	  	    sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	  	  	    clientSocket.send(sendPacket);
	            break;
	        case '4': //left 
	        	System.out.println("left " + CONSTANT_DISTANCE);
	  	  		sentence = "left " + CONSTANT_DISTANCE;
	  	  	    sendData = sentence.getBytes();
	  	  	    sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	  	  	    clientSocket.send(sendPacket);
	            break;
	        case '6': //right 
	        	System.out.println("right " + CONSTANT_DISTANCE);
	  	  		sentence = "right " + CONSTANT_DISTANCE;
	  	  	    sendData = sentence.getBytes();
	  	  	    sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	  	  	    clientSocket.send(sendPacket);
	            break;
	        case '5': //land
	        	System.out.println("land");
	  	  		sentence = "land";
	  	  	    sendData = sentence.getBytes();
	  	  	    sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 8889);
	  	  	    clientSocket.send(sendPacket);
	            break;
	        }
  	  	    
  	  	    
  	     }    
  	     
  	     clientSocket.close();
  	
  	    
  	    
    	 	 
 	   

    }
    
    /* Unravels stack and generates a string of directional numbers. 
     			1 = NW
     			2 = N
     			3 = NE
     			4 = W
     			6 = E
     			7 = SW
     			8 = S
     			9 = SE
   */
    
    public String generateStringFromStack() {
    	CellObject prevObject = intStack.pop();
		CellObject currentObject = intStack.pop();
    	String toReturn = "";
    	
    	while(!intStack.isEmpty()) {
    		if(currentObject.row == prevObject.row + 1 && currentObject.col == prevObject.col + 1) {
    	    	toReturn = "1"+toReturn;
    		}else if(currentObject.row == prevObject.row + 1 && currentObject.col == prevObject.col) {
    	    	toReturn = "2"+toReturn;
    		}else if(currentObject.row == prevObject.row + 1 && currentObject.col == prevObject.col - 1) {
    	    	toReturn = "3"+toReturn;
    		}else if(currentObject.row == prevObject.row && currentObject.col == prevObject.col + 1) {
    	    	toReturn = "4"+toReturn;
    		}else if(currentObject.row == prevObject.row && currentObject.col == prevObject.col - 1) {
    	    	toReturn = "6"+toReturn;
    		}else if(currentObject.row == prevObject.row - 1 && currentObject.col == prevObject.col) {
    	    	toReturn = "8"+toReturn;
    		}else if(currentObject.row == prevObject.row - 1 && currentObject.col == prevObject.col + 1) {
    	    	toReturn = "7"+toReturn;
    		}else if(currentObject.row == prevObject.row - 1 && currentObject.col == prevObject.col - 1) {
    	    	toReturn = "9"+toReturn;
    		}
    		prevObject = currentObject;
    		currentObject = intStack.pop();
    	}
    	
    	return "0"+toReturn+"5"; //Return with takeoff and land signals 
    }
	  
    
    public class CellObject {
    	private int row; 
    	private int col;
    	
    	public CellObject(int Row, int Col) {
    		row = Row;
    		col = Col;
    	}
    	
    	public String toString() {
    		return "Row: " + row + ", Column: " + col;
    	}
    	
    	public String calculateDirection(CellObject cell) {
    		return "";
    	}
    }
    int centerRow = (int)(GRID_SIZE/2);
    int centerCol = (int)(GRID_SIZE/2);
    int prevRow = (int)(GRID_SIZE/2);
    int prevCol = (int)(GRID_SIZE/2); 
    boolean prevValid = true; 
    
    public class CellPane extends JPanel {

        private Color defaultBackground = getBackground();
        private boolean selected = false;
        private JTextField verticleTextField = new JTextField(3);
        

        public CellPane(int row, int col) {
        	 //add(verticleTextField);
        	 if(row == centerRow && col == centerCol) {
        		 setBackground(Color.green);
        	 }
        	 addMouseListener(new MouseAdapter() {
                 @Override
                 public void mouseClicked(MouseEvent e) {
                	 if(isValidSelection(row, col)) {
                		 selected = !selected; 
                         if(selected) {
                         	intStack.push(new CellObject(row, col));
                         	prevRow = row;
                         	prevCol = col;
                         }else {
                         	System.out.println(intStack.pop());
                         	prevValid = false;
                         }
                	 }
                    
                 }
             });
            addMouseListener(new MouseAdapter() {
                @Override
                public void mouseEntered(MouseEvent e) {
                    setBackground(Color.RED);
                }

                @Override
                public void mouseExited(MouseEvent e) {
                	if(row == centerRow && col == centerCol) {
                		setBackground(Color.green);
               	 	}else if(selected) {
                		setBackground(Color.BLUE);
                	}else {
                		setBackground(defaultBackground);
                	}
                }
            });
        }
        

        public boolean isValidSelection(int row, int col) {
        	return (
        			(row == prevRow && col == prevCol) ||// Only let same square selected if previous was invalid
        			(row == prevRow && col == prevCol + 1) ||
        			(row == prevRow && col == prevCol - 1) ||
        			(row == prevRow + 1 && col == prevCol) ||
        			(row == prevRow + 1 && col == prevCol + 1) ||
        			(row == prevRow + 1 && col == prevCol - 1) ||
        			(row == prevRow - 1 && col == prevCol) ||
        			(row == prevRow - 1 && col == prevCol + 1) ||
        			(row == prevRow - 1 && col == prevCol - 1) 
        			);
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(15, 15);
        }
    }
}