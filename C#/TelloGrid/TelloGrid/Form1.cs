using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Collections;
using TelloLib;

namespace TelloGrid
{
    public partial class TelloFrame : Form
    {

        bool[,] checkArray = new bool[7, 7] { {false, false, false, false, false, false, false},
                                              {false, false, false, false, false, false, false},
                                              {false, false, false, false, false, false, false},
                                              {false, false, false, false, false, false, false},
                                              {false, false, false, false, false, false, false},
                                              {false, false, false, false, false, false, false},
                                              {false, false, false, false, false, false, false}};

        public TelloFrame()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private bool isInBounds(int row, int col) {
            return (row >= 0 && row <= 6 && col >= 0 && col <= 6);
        }

        private void DeployCodeButton_Click(object sender, EventArgs e)
        {
            int row = 3;
            int col = 3;
            bool validConfig = true;
            ArrayList instructionList = new ArrayList();
            while (validConfig)
            {
                row -= 1;
                if (isInBounds(row, col) && checkArray[row, col])
                {
                    // Up 
                    instructionList.Add(2);
                    Console.WriteLine("2");
                    checkArray[row, col] = false;
                }
                else {
                    col -= 1;
                    if (isInBounds(row, col) && checkArray[row, col])
                    {
                        // NorthWest
                        instructionList.Add(1);
                        Console.WriteLine("1");
                        checkArray[row, col] = false;
                    }
                    else {
                        col += 2;
                        if (isInBounds(row, col) && checkArray[row, col])
                        {
                            // NorthEast
                            instructionList.Add(3);
                            Console.WriteLine("3");
                            checkArray[row, col] = false;
                        }
                        else {
                            col -= 2;
                            row += 1;
                            if (isInBounds(row, col) && checkArray[row, col])
                            {
                                // West
                                instructionList.Add(4);
                                Console.WriteLine("4");
                                checkArray[row, col] = false;
                            }
                            else {
                                col += 2;
                                if (isInBounds(row, col) && checkArray[row, col])
                                {
                                    // East
                                    instructionList.Add(6);
                                    Console.WriteLine("6");
                                    checkArray[row, col] = false;
                                }
                                else {
                                    col -= 2;
                                    row += 1;
                                    if (isInBounds(row, col) && checkArray[row, col])
                                    {
                                        // SouthWest
                                        instructionList.Add(7);
                                        Console.WriteLine("7");
                                        checkArray[row, col] = false;
                                    }
                                    else {
                                        col += 1;
                                        if (isInBounds(row, col) && checkArray[row, col])
                                        {
                                            // South
                                            instructionList.Add(8);
                                            Console.WriteLine("8");
                                            checkArray[row, col] = false;
                                        }
                                        else{
                                            col += 1;
                                            if (isInBounds(row, col) && checkArray[row, col])
                                            {
                                                // SouthEast
                                                instructionList.Add(9);
                                                Console.WriteLine("9");
                                                checkArray[row, col] = false;
                                            }
                                            else {
                                                validConfig = false;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

            }
            Console.WriteLine(instructionList);
           // else {
           //     Console.WriteLine("Invalid Configuration");
           // }
        }

        private void checkBox1_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 0] = !checkArray[0, 0];
        }

        private void checkBox1_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 1] = !checkArray[0, 1];
        }

        private void checkBox1_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 2] = !checkArray[0, 2];
        }

        private void checkBox1_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 3] = !checkArray[0, 3];
        }

        private void checkBox1_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 4] = !checkArray[0, 4];
        }

        private void checkBox1_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 5] = !checkArray[0, 5];
        }

        private void checkBox1_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[0, 6] = !checkArray[0, 6];
        }

        private void checkBox2_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 0] = !checkArray[1, 0];
        }

        private void checkBox2_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 1] = !checkArray[1, 1];
        }

        private void checkBox2_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 2] = !checkArray[1, 2];
        }

        private void checkBox2_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 3] = !checkArray[1, 3];
        }

        private void checkBox2_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 4] = !checkArray[1, 4];
        }

        private void checkBox2_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 5] = !checkArray[1, 5];
        }

        private void checkBox2_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 6] = !checkArray[1, 6];
        }

        private void checkBox3_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 0] = !checkArray[2, 0];
        }

        private void checkBox3_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 1] = !checkArray[2, 1];
        }

        private void checkBox3_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 2] = !checkArray[2, 2];
        }

        private void checkBox3_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 3] = !checkArray[2, 3];
        }

        private void checkBox3_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 4] = !checkArray[2, 4];
        }

        private void checkBox3_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 5] = !checkArray[2, 5];
        }

        private void checkBox3_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 6] = !checkArray[2, 6];
        }

        private void checkBox4_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 0] = !checkArray[3, 0];
        }

        private void checkBox4_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 1] = !checkArray[3, 1];
        }

        private void checkBox4_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 2] = !checkArray[3, 2];
        }

        private void checkBox4_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 3] = !checkArray[3, 3];
        }

        private void checkBox4_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 4] = !checkArray[3, 4];
        }

        private void checkBox4_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 5] = !checkArray[3, 5];
        }

        private void checkBox4_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 6] = !checkArray[3, 6];
        }

        private void checkBox5_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 0] = !checkArray[4, 0];
        }

        private void checkBox5_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 1] = !checkArray[4, 1];
        }

        private void checkBox5_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 2] = !checkArray[4, 2];
        }

        private void checkBox5_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 3] = !checkArray[4, 3];
        }

        private void checkBox5_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 4] = !checkArray[4, 4];
        }

        private void checkBox5_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 5] = !checkArray[4, 5];
        }

        private void checkBox5_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 6] = !checkArray[4, 6];
        }

        private void checkBox6_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 0] = !checkArray[5, 0];
        }

        private void checkBox6_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 1] = !checkArray[5, 1];
        }

        private void checkBox6_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 2] = !checkArray[5, 2];
        }

        private void checkBox6_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 3] = !checkArray[5, 3];
        }

        private void checkBox6_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 4] = !checkArray[5, 4];
        }

        private void checkBox6_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 5] = !checkArray[5, 5];
        }
   
        private void checkBox6_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[5, 6] = !checkArray[5, 6];
        }

        private void checkBox7_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 0] = !checkArray[6, 0];
        }

        private void checkBox7_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 1] = !checkArray[6, 1];
        }

        private void checkBox7_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 2] = !checkArray[6, 2];
        }

        private void checkBox7_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 3] = !checkArray[6, 3];
        }

        private void checkBox7_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 4] = !checkArray[6, 4];
        }

        private void checkBox7_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 5] = !checkArray[6, 5];
        }

        private void checkBox7_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[6, 6] = !checkArray[6, 6];
        }
    }
}
