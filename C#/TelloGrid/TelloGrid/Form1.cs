using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
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


        private void DeployCodeButton_Click(object sender, EventArgs e)
        {

        }

        private void checkBox1_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 1] = !checkArray[1, 1];
        }

        private void checkBox1_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 2] = !checkArray[1, 2];
        }

        private void checkBox1_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 3] = !checkArray[1, 3];
        }

        private void checkBox1_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 4] = !checkArray[1, 4];
        }

        private void checkBox1_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 5] = !checkArray[1, 5];
        }

        private void checkBox1_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 6] = !checkArray[1, 6];
        }

        private void checkBox1_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[1, 7] = !checkArray[1, 7];
        }

        private void checkBox2_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 1] = !checkArray[2, 1];
        }

        private void checkBox2_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 2] = !checkArray[2, 2];
        }

        private void checkBox2_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 3] = !checkArray[2, 3];
        }

        private void checkBox2_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 4] = !checkArray[2, 4];
        }

        private void checkBox2_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 5] = !checkArray[2, 5];
        }

        private void checkBox2_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 6] = !checkArray[2, 6];
        }

        private void checkBox2_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[2, 7] = !checkArray[2, 7];
        }

        private void checkBox3_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 1] = !checkArray[3, 1];
        }

        private void checkBox3_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 2] = !checkArray[3, 2];
        }

        private void checkBox3_3_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 3] = !checkArray[3, 3];
        }

        private void checkBox3_4_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 4] = !checkArray[3, 4];
        }

        private void checkBox3_5_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 5] = !checkArray[3, 5];
        }

        private void checkBox3_6_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 6] = !checkArray[3, 6];
        }

        private void checkBox3_7_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[3, 7] = !checkArray[3, 7];
        }

        private void checkBox4_1_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 1] = !checkArray[4, 1];
        }

        private void checkBox4_2_CheckedChanged(object sender, EventArgs e)
        {
            checkArray[4, 2] = !checkArray[4, 2];
        }

        private void checkBox4_3_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox4_4_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox4_5_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox4_6_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox4_7_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_2_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_3_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_4_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_5_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_6_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox5_7_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_2_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_3_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_4_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_5_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_6_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox6_7_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_2_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_3_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_4_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_5_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_6_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBox7_7_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
