# Database-system-principal
Assignment 2 - This section presents an example of using the GUI of the Python application, Query Visualizer. It is important to note that the user must update the Python application with its PostgreSQL user credentials before querying the user’s input. This can be done through the GUI.  

# User Guide 

1.  Zipped the submission folder
2.  Run the dsp.exe executable file located at “Executable program\main\” to launch the Python application. 
3.  Set up the Python application by updating it with PostgreSQL’s user credentials.  
    1.  Under SETTINGS menu, select CONNECTION (CTRL + N)
   
    ![ScreenShot](/image/Picture1.png)
    
    2.  Update the user’s credential as necessary and save.  
    
    ![ScreenShot](/image/Picture2.png)
    
    3.  You are now ready to retrieve QEPs and the explanation for the selected QEP.  
    
4.  Enter a query that follows the SQL query template format, then click QUERY PLAN. 
    1.  Click on the empty textbox and input the query. 
    
    ![ScreenShot](/image/Picture3.png)
5.  Query Visualizer will be updated with an interactive operator tree and an explanation for why this plan is selected.  

![ScreenShot](/image/Picture4.png)

6.  To view alternative plans, click on the drop-down menu LIST OF PLANS 
    1.  Click on any alternative plan to view the updated interactive operator tree. 
 
 ![ScreenShot](/image/Picture5.png)
