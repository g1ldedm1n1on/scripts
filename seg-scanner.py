#!/usr/bin/python
########################################################################################
#
#  Segmentation Scanner and Parser
#  Created: Matt Molda
#  Date: 5/1/2016
#  Description:
#  Used to scan a secure enclave and then produce spreadsheet of findings
#  and table that can be imported into a report.
#
# Requirements:  xlsxwriter and python-libnmap
# pip install xlsxwriter
# pip install python-libnmap
#########################################################################################


import xlsxwriter
import datetime
import sys
import os
import subprocess
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

#set common values
finding = "PENT-0066"
vulnstate = "validated"
status = "open"
title = "PCI-DSS and/or SOC2 violation of Segmentation Controls"
desc = "Inadequate Network Segmentation Controls in Place Allowing Traffic Between an Unsecured Network Enclave and a Secured Network Enclave"
risk = "High"
brisk = "High"
cvss = "4.3"
cve = "N/A"
recommend = "Provide sufficient controls by either moving identified hosts into a secure enclave or setting up firewall rules in order to prevent disallowed traffic."
notes = "https://www.pcisecuritystandards.org/documents/Penetration_Testing_Guidance_March_2015.pdf"
sysname = None
ip = None
port = None
host = None

#get date and format
now = datetime.datetime.now()
info = now.strftime("%m_%d_%Y_%H_%M")


#read in scope list
try:
        file_name = sys.argv[1]
        fp = open(file_name)
        ips = fp.read()
        ips = ips.rstrip("\r\n")

except:
        print "Must include path to  file containing scope  and project name. sudo ./seg-scanner.py scope.txt myproject1"
        exit(1)

try:
        projectname = sys.argv[2]

except:
        print "Must pass in project name as second argument.  sudo ./seg-scanner.py scope.txt myprojectname"

#get info on where to store results
homedir = os.environ['HOME']
localname = os.getenv("SUDO_USER")
userhome = "/home/" + localname
output = userhome
#print "Home Variable = " + homedir
#print projectname
projectdir = userhome + "/segmentation_scan_results"
outpath = projectdir + "/" + projectname
print outpath
print "Creating project directory at: " + outpath
outfile = outpath + "/" + projectname




#try and create the directory
try:
        if not os.path.exists(outpath):
                os.makedirs(outpath)


except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
                        print "An error occured while trying to create the output directory"
                        exit(1)

#setup worksheet
name = outpath + "/" + "Segmentation_Results_"+ info + ".xlsx"
print "workbook name is: " + name
workbook = xlsxwriter.Workbook(name)
worksheet = workbook.add_worksheet('Vuln List')
worksheet2 = workbook.add_worksheet('Report Table')
bold = workbook.add_format({'bold': True})
bold_clr=workbook.add_format({'bold': True})
bold_clr.set_bg_color('#6495ED')
wrap = workbook.add_format({'bold': True})
wrap.set_text_wrap()

#set default starting places
row = 1
col = 0

#set some column widths
worksheet.set_column('A:A', 15)
worksheet.set_column('B:B', 15)
worksheet.set_column('C:C', 15)
worksheet.set_column('D:D', 20)
worksheet.set_column('E:E', 20)
worksheet.set_column('F:F', 20)
worksheet.set_column('G:G', 10)
worksheet.set_column('H:H', 20)
worksheet.set_column('I:I', 20)
worksheet.set_column('J:J', 20)
worksheet.set_column('K:K', 15)
worksheet.set_column('L:L', 30)
worksheet.set_column('M:M', 30)
worksheet.set_column('N:N', 20)


# write column headers for worksheet
worksheet.write('A1', 'Finding #', bold)
worksheet.write('B1', 'State', bold)
worksheet.write('C1', 'Status', bold)
worksheet.write('D1', 'Finding Title', bold)
worksheet.write('E1', 'System Name', bold)
worksheet.write('F1', 'System IP', bold)
worksheet.write('G1', 'Port', bold)
worksheet.write('H1', 'Technical Risk', bold)
worksheet.write('I1', 'Business Risk', bold)
worksheet.write('J1', 'CVSS Base Score', bold)
worksheet.write('K1', 'CVE', bold)
worksheet.write('L1', 'Description', wrap)
worksheet.write('M1', 'Recommendations', wrap)
worksheet.write('N1', 'Notes', wrap)
worksheet.write('N1', 'Detail', wrap)


#wire column headers and width for worksheet1
worksheet2.write('A1', "System Name", bold_clr)
worksheet2.write('B1', "IP Address", bold_clr)
worksheet2.write('C1', "Open Ports", bold_clr)

worksheet2.set_column('A:A', 20)
worksheet2.set_column('B:B', 20)
worksheet2.set_column('C:C', 20)



#set nmap command
nmap_cmd = "nmap -sS -p1-65535 --min-hostgroup 10 -iL " + file_name + " -vv --open -oA " + outfile + "_%T_%D"
print nmap_cmd
print "..............Starting Nmap Segmentation Scan..............."

try:
 subprocess.call(nmap_cmd, shell=True)

except:
        print "Error Running Nmap! Are you running as root?"
        exit(1)


#read in xml output from nmap scan
try:
 #print outpath
 nmapxml = outfile + ".xml"
 print nmapxml
 if not os.path.isfile(nmapxml):
        print "No Output From Nmap Scan Found. Possible No Open Ports!"
        exit(1)
 else:

        nmap_report = NmapParser.parse_fromfile(nmapxml)
        total = nmap_report.hosts_total
        #print total
        hosts = nmap_report.hosts
        hosts = str(hosts)
        #print hosts
        #print dir(nmap_report)
        if hosts == '[]':
                print "No hosts found in Nmap File. Likely no open ports were found!"
                exit(1)
        else:
                for host in nmap_report.hosts:
                        for service in host.services:
                                sysname = host.hostnames
                                sysname = str(sysname)
                                sysname = sysname.strip('[\']')
                                ip = host.address
                                proto = service.protocol
                                p = service.port
                                p = str(p)
                                state = service.state
                                port = (p + "/" + proto)
                                ip = str(ip)
                                print("Exporting: " + " " + sysname + " " + ip + " " + port + " " + state)
                                # output data to xlsx

                                worksheet.write(row, col,finding)
                                worksheet.write(row, col + 1, vulnstate)
                                worksheet.write(row, col + 2, status)
                                worksheet.write(row, col + 3, title)
                                worksheet.write(row, col + 4, sysname)
                                worksheet.write(row, col + 5, ip)
                                worksheet.write(row, col + 6, port)
                                worksheet.write(row, col + 7, risk)
                                worksheet.write(row, col + 8, brisk)
                                worksheet.write(row, col + 9, cvss)
                                worksheet.write(row, col + 10, cve)
                                worksheet.write(row, col + 11, desc)
                                worksheet.write(row, col + 12, recommend)
                                worksheet.write(row, col + 13, notes)

                                worksheet2.write(row, col, sysname)
                                worksheet2.write(row, col + 1, ip)
                                worksheet2.write(row, col + 2, port)

                                row += 1


except:
 print "There was an error reading in or parsing the XML file. If no hosts were reported in the XML this expected!"
 exit(1)







workbook.close()

#set user as owner of directory and files
chown = "chown -R " + localname + " " + outpath

try:
 subprocess.call(chown)

except:
        print "Unable to chown " + outpath + " for user " + localname
        exit(1)