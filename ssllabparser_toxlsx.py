#!/usr/bin/python
# 
# Created: GildedMinion, base code XME @ https://github.com/xme/toolbox/blob/master/ssllabs-scan-parse.py
# run ssllabs-scan and output file to json then pipe through this or cat output and pipe through this to create spreadsheet
# sample 'cat myscan.json | ./ssllabparser_toxslx.py' outputs SSLLabsScanResults.xlsx
# sample ./ssllabs-scan --quiet --hostfile=mydomain.txt --ignore-mismatch=true --hostcheck=false > mydomain.json && cat mydomain.json | ./ssllabparser_toxslx.py
# scoring guide located : https://www.ssllabs.com/downloads/SSL_Server_Rating_Guide.pdf


import json
import md5
import xlsxwriter
import sys
import time
from pprint import pprint

with sys.stdin as json_data:
        try:
                data = json.load(json_data)
        except:
                print "Error: no JSON data received!"
                exit(1)
#setup XLSX
workbook = xlsxwriter.Workbook('SSLLabsScanResults.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1', 'Site Name', bold)
worksheet.write('B1', 'Port', bold)
worksheet.write('C1', 'IP Address', bold)
worksheet.write('D1', 'SSL Labs Grade', bold)
worksheet.write('E1', 'Certificate Issuer', bold)
worksheet.write('F1', 'Certificate Expiration', bold)
worksheet.write('G1', 'Certificate MD5 Hash', bold)
worksheet.write('H1', 'Certificate Size', bold)
worksheet.write('I1', 'Certificate Algorithm', bold)
worksheet.write('J1', 'Certificate Strength', bold)
worksheet.write('K1', 'HeartBleed', bold)
worksheet.write('L1', 'HeartBeat', bold)
worksheet.write('M1', 'OpenSSL CCS', bold)
worksheet.write('N1', 'Poodle', bold)
worksheet.write('O1', 'Fallback SCSV', bold)
worksheet.write('P1', 'Freak', bold)
worksheet.write('Q1', 'Logjam', bold)
worksheet.write('R1', 'Supports RC4', bold)
worksheet.write('S1', 'Vulnerable to BEAST', bold)
worksheet.write('T1', 'Insecure Renegotiation', bold)
worksheet.write('U1', 'Server Signature', bold)
worksheet.write('V1', 'SSL v3', bold)
worksheet.write('W1', 'TLS 1.0', bold)
worksheet.write('X1', 'TLS 1.1', bold)
worksheet.write('Y1', 'TLS 1.2', bold)


#set default starting places
row = 1
col = 0

# make sure the site contains appropiate data to SSL stuff


#parse through json and gather specific info

for site in data:
# make sure there are endpoints to pull data from in the site
	if "endpoints" in site:
		endpoints = site['endpoints']
		status = endpoints[0]['statusMessage']
#	If status it not ready for statusMessage there is no certificate info to be pulled from the endpoints
		if "Ready" in status:
#   Pull in all the data we want for that site to write to excel
			ip = endpoints[0]['ipAddress']
			certExp = time.ctime(int(endpoints[0]['details']['cert']['notAfter']/1000))
			certRaw = endpoints[0]['details']['chain']['certs'][0]['raw']
			certmd5 = md5.new(certRaw).hexdigest()
			domain = site['host']
			print domain
			port = site['port']
			grade = endpoints[0]['grade']
			issuer = endpoints[0]['details']['cert']['issuerLabel']
			date = time.ctime(int(endpoints[0]['details']['cert']['notAfter']/1000))
			size = endpoints[0]['details']['key']['size']
			alg = endpoints[0]['details']['key']['alg']
			strength = endpoints[0]['details']['key']['strength']
			heartbled = (endpoints[0]['details']['heartbleed'])
			heartbeat = endpoints[0]['details']['heartbeat']
			opensslccs = endpoints[0]['details']['openSslCcs']
			poodle = endpoints[0]['details']['poodle']
# Needed to validate fallbackScvs.  Json is inconsistent and doesn't always return true or false for key
			if "fallbackScsv" in endpoints[0]['details']:
				fallback = endpoints[0]['details']['fallbackScsv']
			else:
				fallback = "No Data Returned"
				pass
			freak = endpoints[0]['details']['freak']
			logjam = endpoints[0]['details']['logjam']
			rc4 = endpoints[0]['details']['supportsRc4']
			beast = endpoints[0]['details']['vulnBeast']
			
			#Loop through the protocol ids to find out what protocols are running.
			cipher = endpoints[0]['details']['protocols']
			
			# reset cipher each pass to blank
			# reset cipher each pass to blank
			tls10 = ""
			tls11 = ""
			ssl3 = ""
			tls12 = ""

			for id in cipher:

				cipher = id['name'] + " " + id['version']
				if cipher == "TLS 1.0":
					tls10 = "x"
					print "matches tls1.0"
				elif cipher == "TLS 1.1":
					tls11 = "x"
					print "matches tls1.1"
				elif cipher == "SSL 3.0":
					print "matches ssl3.0"
					ssl3 = "x"
				elif cipher == "TLS 1.2":
					print "matches TLS 1.2"
					tls12 = "x"
				print cipher
			
				#id = cipher['id']
			
			# Need to loop through the protocols and take extract from each id,  name and version and add it to array
			#foreach id in protocols:
			#	version = protocols[0]['name']
			#	print version
			#print protocols
			#version = endpoints[0]['details']['protocols'][0]['version']
			#protocols = protocols + ':' + version
			#print protocols
			if "serverSignature" in endpoints[0]['details']:
				servsig = endpoints[0]['details']['serverSignature']
			else:
				servsig = "No Server Signature"
				pass
			if servsig == "":
				servsig == "No Server Signature"

# Check Insecure Number and set value as needed
			insecure = endpoints[0]['details']['renegSupport']
			if insecure == 1:
				insecureval = "Allowed"
			elif insecure == 6:
				insecureval = "Secure Renegotiation Allowed Possible DoS"
			else:
				insecureval = "Not Allowed"

# output data to xlsx
			worksheet.write(row, col, domain)
			worksheet.write(row, col + 1,  port)
			worksheet.write(row, col + 2, ip)
			worksheet.write(row, col + 3, grade)
			worksheet.write(row, col + 4, issuer)
			worksheet.write(row, col + 5, date)
			worksheet.write(row, col + 6, certmd5)
			worksheet.write(row, col + 7, size)
			worksheet.write(row, col + 8, alg)
			worksheet.write(row, col + 9, strength)
			worksheet.write(row, col + 10, heartbled)
			worksheet.write(row, col + 11, heartbeat)
			worksheet.write(row, col + 12, opensslccs)
			worksheet.write(row, col + 13, poodle)
			worksheet.write(row, col + 14, fallback)
			worksheet.write(row, col + 15, freak)
			worksheet.write(row, col + 16, logjam)
			worksheet.write(row, col + 17, rc4)
			worksheet.write(row, col + 18, beast)
			worksheet.write(row, col + 19, insecureval)
			worksheet.write(row, col + 20, servsig)
			worksheet.write(row, col + 21, ssl3)
			worksheet.write(row, col + 22, tls10)
			worksheet.write(row, col + 23, tls11)
			worksheet.write(row, col + 24, tls12)
			row += 1
workbook.close()
