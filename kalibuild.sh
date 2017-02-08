#! /bin/bash




printf "\n\e[32m***********Installing VMwareTools************\n\e[0m"
apt-get install open-vm-tools-desktop fuse -Y




mkdir /root/git_repos
cd /root/git_repos

printf "\n\e[32m*********Cloning Git Repos********\n\e[0m"
git clone https://github.com/EmpireProject/Empire.git
git clone https://github.com/EmpireProject/EmPyre.git
git clone https://github.com/Sw4mpf0x/Kraken.git
git clone https://github.com/g1ldedm1n1on/scripts.git
git clone https://github.com/g1ldedm1n1on/Kaliupdater.git
git clone https://github.com/g1ldedm1n1on/msf_resourcefiles.git

printf “\n\e[32m*******Installing Vulscan********\n\e[0m”

cd /root/Downloads
wget http://www.computec.ch/projekte/vulscan/download/nmap_nse_vulscan-2.0.tar.gz

tar xfz nmap_nse_vulscan-2.0.tar.gz
mv vulscan/ /usr/share/nmap/scripts/

printf "\n\e[32m*********Installing Kraken*********\n\e[0m"
cd /root/git_repos/Kraken
chmod 755 ./setup.sh
./setup.sh

mkdir /root/git_repos/powershell
cd /root/git_repos/powershell

printf “\n\e[32m******Installing Powershell Repos*******\n\e[0m”
git clone https://github.com/NetSPI/PowerUpSQL.git
git clone https://github.com/samratashok/nishang.git
git clone https://github.com/Kevin-Robertson/Inveigh.git
git clone https://github.com/mattifestation/PowerShellArsenal.git
git clone https://github.com/PowerShellMafia/PowerSploit.git

cp /root/git_repos/Kailupdater/kailupdater.sh /root
rm -rf /root/git_repos/Kaliupdater
chmod +x kaliupdater.sh
./kaliupdater.sh


printf "\n\e[32m******Installing Shellter*******\n\e[0m"

apt-get install shellter veil-evasion

printf "\n\e[32m*****Installing Veil Evasion**********\n"
printf "\nPlease Click through the Defaults on WINE Installs!\e[0m"

cd /usr/share/veil-evasion/setup
./setup.sh
