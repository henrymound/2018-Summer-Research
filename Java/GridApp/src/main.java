import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.*;
import java.util.*;

public class main {
	
	int GRID_SIZE = 21;
	
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
                		    deployCodeButtonPressed();
                		  } 
                		} 
                );
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                frame.setLayout(new BorderLayout());
                frame.add(new TestPane());
                frame.add(deployCodeButton, BorderLayout.SOUTH);
                frame.pack();
                frame.setLocationRelativeTo(null);
                frame.setVisible(true);
            }
        });
    }

    public void deployCodeButtonPressed() {
    	 System.out.println("DEPLOYING CODE");

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
    }
    
    public class CellPane extends JPanel {

        private Color defaultBackground = getBackground();
        private boolean selected = false;

        public CellPane(int row, int col) {
        	 addMouseListener(new MouseAdapter() {
                 @Override
                 public void mouseClicked(MouseEvent e) {
                    selected = !selected; 
                    if(selected) {
                    	intStack.push(new CellObject(row, col));
                    }else {
                    	System.out.println(intStack.pop());
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
                	if(selected) {
                		setBackground(Color.BLUE);
                	}else {
                		setBackground(defaultBackground);
                	}
                }
            });
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(30, 30);
        }
    }
}