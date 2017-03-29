# Nginx

Place the nginx config file in `/etc/nginx/sites-available/doca.data.generalassemb.ly`
and create a simlink to activate it: 

```
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo systemctl restart nginx
sudo systemctl status nginx
```


# Systemd

Place the two `.service` files in the `/etc/systemd/system` folder and run the following 
commands to get them up and running: 

```
systemctl enable docaweb.service
systemctl start docaweb.service
systemctl status docaweb.service
```

and 
```
systemctl enable docaserv.service
systemctl start docaserv.service
systemctl status docaserv.service
```

# Crontab

Install a crontab on the ubuntu user as follows: 

```
0 * * * * /usr/bin/python /home/(?:ec2-user|ubuntu)/iglu-doca/bin/public_schemas.py
```
This will update the schema files on the server once per hour. At some point, 
someone should install the other /bin file on the iglu server, since 
it requires access to the jsonpaths and sql files in order to update the schemas on the api. 
This could also run as part of a CI system, but it's not clear what we want that 
to look like right now. 

