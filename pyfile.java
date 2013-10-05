import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.IOException;
public class pyfile extends JFrame
{
public pyfile()
{
JPanel panel=new JPanel();
setContentPane(panel);
panel.setLayout(null);
final JTextArea text= new JTextArea();
text.setLineWrap(true);
text.setBounds(30,30,450,450);
JButton postbtn=new JButton("Post");
postbtn.setBounds(380,505,100,40);
panel.add(postbtn);
getRootPane().setDefaultButton(postbtn);

postbtn.addActionListener(new ActionListener()
{
@Override
public void actionPerformed(ActionEvent event) 
{
    		String data = text.getText();
 
    		try{ 
			File file =new File("paragraphs.py");
	 
	    		if(!file.exists())
			{
	    				file.createNewFile();
					FileWriter fileWritter = new FileWriter(file.getName(),true);
			    	        BufferedWriter bufferWritter = new BufferedWriter(fileWritter);
					bufferWritter.write("class paralist:");
					bufferWritter.write("\n\tdef __init__(self):");
					bufferWritter.write("\n\t\tself.para=[]");
			    	        bufferWritter.write(("\n\t\tself.para.append(\"")+(data)+("\")"));
			    	        bufferWritter.close();
					text.setText("");
				        System.out.println("New file created");
	    		}
	 		else
			{
		    		FileWriter fileWritter = new FileWriter(file.getName(),true);
		    	        BufferedWriter bufferWritter = new BufferedWriter(fileWritter);
		    	        bufferWritter.write("\n\t\tself.para.append(\""+data+"\")");
		    	        bufferWritter.close();
				text.setText("");
			        System.out.println("New paragraph created");
 			}

			text.requestFocus();
		}catch(IOException e){ System.out.println("Error"); }
 	
}
});
panel.add(text);
setTitle("Post");
setSize(515,610);
setResizable(false);
setLocationRelativeTo(null);
setDefaultCloseOperation(EXIT_ON_CLOSE);

}

public static void main(String[] args)
{
pyfile myui=new pyfile();
myui.setVisible(true);
}
}
