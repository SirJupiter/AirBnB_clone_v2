#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment of web_static. It must:
# Install Nginx if it not already installed
# Create the folder /data/ if it doesn’t already exist
# Create the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
# Create the folder /data/web_static/shared/ if it doesn’t already exist
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist

# function to check if nginx is installed
function install_nginx() {
	if ! command -v nginx &> /dev/null; then
		echo -e "\n....		Installing Nginx	....\n"
		if sudo apt update -y && sudo apt install -y nginx; then
			echo -e "\n----      Successfully installed Nginx      ----\n"
		else
			echo -e "\nxxxx      Error: Failed to install Nginx      xxxx\n"
			exit 1
		fi
	else
		echo -e "\n----      Nginx already installed      ----\n"
	fi
}

# call the install function
install_nginx

# Start Nginx
sudo service nginx restart

# Check if Nginx is running
if ! pgrep -x "nginx" > /dev/null; then
	echo "Nginx failed to start" >&2
	exit 1
else
	echo -e "\n----		Nginx is running!      ----\n"
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
sudo echo "<html>
	<head>
  	</head>
  	<body>
    	Holberton School
  	</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/*

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static). Don’t forget to restart Nginx after updating the configuration:
# Use alias inside your Nginx configuration
nginx_config_file="/etc/nginx/sites-available/default"
new_config="\n\
	location /hbnb_static {\n\t\t\
		alias /data/web_static/current/;\n\t\
	}\n\n\
"

if ! sudo sed -i "/server_name _;/a $new_config" "$nginx_config_file"; then
	echo -e "\nxxxx    Error: Configuration unsuccessful    xxxx\n"
	exit 1
else
	echo -e "\n----      Nginx configuration successful!      ----\n"
fi

sudo service nginx restart

exit 0
