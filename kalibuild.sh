#! /bin/bash

printf "\nInstalling VMwareTools"
apt-get install open-vm-tools-desktop fuse




mkdir /root/git_repos
cd /root/git_repos

printf "\n*********Cloning Git Repos********\n"
git clone https://github.com/EmpireProject/Empire.git
git clone https://github.com/EmpireProject/EmPyre.git
git clone https://github.com/Sw4mpf0x/Kraken.git
git clone https://github.com/g1ldedm1n1on/scripts.git
git clone https://github.com/g1ldedm1n1on/Kaliupdater.git
git clone https://github.com/g1ldedm1n1on/msf_resourcefiles.git

printf “\n*******Installing Vulscan********\n”

cd /root/Downloads
wget http://www.computec.ch/projekte/vulscan/download/nmap_nse_vulscan-2.0.tar.gz

tar xfz nmap_nse_vulscan-2.0.tar.gz
mv vulscan/ /usr/share/nmap/scripts/

printf "\n*********Installing Kraken*********\n"
cd /root/git_repos/Kraken
chmod 755 ./setup.sh
./setup.sh

mkdir /root/git_repos/powershell
cd /root/git_repos/powershell

printf “\n******Installing Powershell Repos*******\n”
git clone https://github.com/NetSPI/PowerUpSQL.git
git clone https://github.com/samratashok/nishang.git
git clone https://github.com/Kevin-Robertson/Inveigh.git
git clone https://github.com/mattifestation/PowerShellArsenal.git
git clone https://github.com/PowerShellMafia/PowerSploit.git

cp /root/git_repos/Kailupdater/kailupdater.sh /root
rm -rf /root/git_repos/Kaliupdater
chmod +x kaliupdater.sh
./kaliupdater.sh




apt-get install shellter
