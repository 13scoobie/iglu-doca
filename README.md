# iglu-doca

Note that there is a `'localhost:8080'` hard-coded into `src/server/html.js` for some 
reason. There is an open issue on github in the parent project, but they aren't planning to fix it. 
This has to be changed to the domain of the EC2 server in order for it to work, and 
the port 8080 needs to be exposed through the security group. 

# server configuration  

The web server and document server are running on systemctl files, configuration is explained in the 
`server` folder. 
