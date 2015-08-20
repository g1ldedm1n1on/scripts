#! /bin/bash
/etc/init.d/postgresql start
/etc/init.d/metasploit start
cd /usr/share/beef-xss
printf "\nstarting metasploit..."
gnome-terminal -e "msfconsole -r /opt/msf_resources/startupbeef.rc"
printf "\nwaiting for metasploit to start..."
sleep 30s
printf "\nstarting beef...\n"
gnome-terminal -e "ruby beef" --window-with-profile=beef
