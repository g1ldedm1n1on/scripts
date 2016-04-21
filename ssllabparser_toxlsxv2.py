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
import datetime
from pprint import pprint


now = datetime.datetime.now()
info = now.strftime("%m_%d_%Y_%H_%M")


with sys.stdin as json_data:
        try:
                data = json.load(json_data)
        except:
                print "Error: no JSON data received!"
                exit(1)
#setup XLSX
name = "SSLLabsScanResults" + "_" + info + ".xlsx"
workbook = xlsxwriter.Workbook(name)
worksheet = workbook.add_worksheet('Results')
worksheet2 = workbook.add_worksheet('Stats')
bold = workbook.add_format({'bold': True})

#set some column widths
worksheet.set_column('A:A', 35)
worksheet.set_column('C:C', 13)
worksheet.set_column('E:E', 45)
worksheet.set_column('F:F', 22)
worksheet.set_column('G:G', 31)
worksheet.set_column('T:T', 33)
worksheet.set_column('U:U', 81)
worksheet.set_column('M:M', 22)
worksheet.set_column('O:O', 14)
worksheet.set_column('S:S', 19)
worksheet.set_column('AA:AA', 14)
worksheet.set_column('AB:AB', 15)
worksheet.set_column('AC:AC', 16)
worksheet.set_column('AD:AD', 15)


# write column headers
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
worksheet.write('M1', 'OpenSSL CCS Vulnerable', bold)
worksheet.write('N1', 'Poodle', bold)
worksheet.write('O1', 'Fallback SCSV', bold)
worksheet.write('P1', 'Freak', bold)
worksheet.write('Q1', 'Logjam', bold)
worksheet.write('R1', 'Supports RC4', bold)
worksheet.write('S1', 'Vulnerable to BEAST', bold)
worksheet.write('T1', 'Insecure Renegotiation', bold)
worksheet.write('U1', 'Server Signature', bold)
worksheet.write('V1', 'SSL v2', bold)
worksheet.write('W1', 'SSL v3', bold)
worksheet.write('X1', 'TLS 1.0', bold)
worksheet.write('Y1', 'TLS 1.1', bold)
worksheet.write('Z1', 'TLS 1.2', bold)
worksheet.write('AA1', 'HSTS Enabled', bold)
worksheet.write('AB1', 'HSTS Max_Age', bold)
worksheet.write('AC1', 'STS Subdomains', bold)
worksheet.write('AD1', 'STS PreEnabled', bold)
worksheet.freeze_panes(1, 0)
worksheet.autofilter('A1:AD1')
#set default starting places
row = 1
col = 0

# make sure the site contains appropiate data to SSL stuff

#build out worksheet for stats and charts


blue = workbook.add_format({'bold': True})
worksheet2.set_column('A:A', 20)
blue.set_pattern(1)  # This is optional when using a solid fill.
blue.set_bg_color('#6495ED')
blue.set_font_color("#F0FFFF")

#setup Grades Table
worksheet2.write('A1', 'Grades', blue)
worksheet2.write('B1', 'Count', blue)
worksheet2.write('A2', 'A+')
worksheet2.write('A3', 'A')
worksheet2.write('A4', 'A-')
worksheet2.write('A5', 'B')
worksheet2.write('A6', 'C')
worksheet2.write('A7', 'F')
worksheet2.write('A8', 'T')
worksheet2.write('A9', 'M')

#setup SSL Supported Versions

worksheet2.write('A11', 'SSL Version Supported', blue)
worksheet2.write('B11', 'Count', blue)
worksheet2.write('A12', 'SSLv2')
worksheet2.write('A13', 'SSLv3')
worksheet2.write('A14', 'TLS1')
worksheet2.write('A15', 'TLS1.1')
worksheet2.write('A16', 'TLS1.2')


#setup HSTS Table
worksheet2.write('A18', 'HSTS Value', blue)
worksheet2.write('B18', 'Count', blue)
worksheet2.write('A19', 'Absent')
worksheet2.write('A20', 'Present')
worksheet2.write('A21', 'Invalid')
worksheet2.write('A22', 'Unknown')


#setup Vulns Tables
worksheet2.write('A24', 'Vulnerabilities', blue)
worksheet2.write('B24', 'Count', blue)
worksheet2.write('A25', 'HeartBleed')
worksheet2.write('A26', 'HeartBeat')
worksheet2.write('A27', 'Poodle')
worksheet2.write('A28', 'fallback SCSV')
worksheet2.write('A29', 'FREAK')
worksheet2.write('A30', 'Logjam')
worksheet2.write('A31', 'Supports RC4')
worksheet2.write('A32', 'BEAST')
worksheet2.write('A33', 'Insecure Renegotiation')



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
			print "Parsing Domain: " + domain
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
			if opensslccs == 2:
				opensslccs = "Probably, but not exploitable"
			elif opensslccs == -1:
				opensslccs = "Unknown"
			elif opensslccs == 1:
				opensslccs = "No"



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

			#set default values for HSTS info and look to see if it exists in endpoint			
			hsts = ""
			hstsage = ""
			stssub = ""
			stspre = ""

			hsts = endpoints[0]['details']['stsStatus']
			

			if hsts == "present":
				hstsage = endpoints[0]['details']['stsMaxAge']
				stssub = endpoints[0]['details']['stsSubdomains']
				stspre = endpoints[0]['details']['stsPreload']
				
			else:
				hstsage = ""
				pass
			#Loop through the protocol ids to find out what protocols are running.
			cipher = endpoints[0]['details']['protocols']

			
			# reset cipher each pass to blank
			ssl2 = ""
			tls10 = ""
			tls11 = ""
			ssl3 = ""
			tls12 = ""
			

			for id in cipher:

				cipher = id['name'] + " " + id['version']
				if cipher == "TLS 1.0":
					tls10 = "X"
				elif cipher == "TLS 1.1":
					tls11 = "X"
				elif cipher == "SSL 3.0":
					ssl3 = "X"
				elif cipher == "TLS 1.2":
					tls12 = "X"
				elif cipher == "SSL 2.0":
					ssl2 = "X"
			
			# parse singature and handle where there isn't any or any returned
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
			worksheet.write(row, col + 21, ssl2)
			worksheet.write(row, col + 22, ssl3)
			worksheet.write(row, col + 23, tls10)
			worksheet.write(row, col + 24, tls11)
			worksheet.write(row, col + 25, tls12)
			worksheet.write(row, col + 26, hsts)
			worksheet.write(row, col + 27, hstsage)
			worksheet.write(row, col + 28, stssub)
			worksheet.write(row, col + 29, stspre)
			row += 1


# build tables and write to xlsx
#grades tables
		worksheet2.write_formula('B2', '=COUNTIF(Results!D2:D10000, "A+")')
		worksheet2.write_formula('B3', '=COUNTIF(Results!D2:D10000, "A")')
		worksheet2.write_formula('B4', '=COUNTIF(Results!D2:D10000, "A-")')
		worksheet2.write_formula('B5', '=COUNTIF(Results!D2:D10000, "B")')
		worksheet2.write_formula('B6', '=COUNTIF(Results!D2:D10000, "C")')
		worksheet2.write_formula('B7', '=COUNTIF(Results!D2:D10000, "F")')
		worksheet2.write_formula('B8', '=COUNTIF(Results!D2:D10000, "T")')
		worksheet2.write_formula('B9', '=COUNTIF(Results!D2:D10000, "M")')


#SSL Versions Tables
		worksheet2.write_formula('B12', '=COUNTIF(Results!V2:V10000, "X")')
		worksheet2.write_formula('B13', '=COUNTIF(Results!W2:W10000, "X")')
		worksheet2.write_formula('B14', '=COUNTIF(Results!X2:X10000, "X")')
		worksheet2.write_formula('B15', '=COUNTIF(Results!Y2:Y10000, "X")')
		worksheet2.write_formula('B16', '=COUNTIF(Results!Z2:Z10000, "X")')


#HSTS Tables
		worksheet2.write_formula('B19', '=COUNTIF(Results!AA2:AA10000, "Absent")')
		worksheet2.write_formula('B20', '=COUNTIF(Results!AA2:AA10000, "Present")')
		worksheet2.write_formula('B21', '=COUNTIF(Results!AA2:AA10000, "Invalid")')
		worksheet2.write_formula('B22', '=COUNTIF(Results!AA2:AA10000, "Unknown")')

#Vulnerabilities Table
		worksheet2.write_formula('B25', '=COUNTIF(Results!K2:K10000, "True")')
		worksheet2.write_formula('B26', '=COUNTIF(Results!L2:L10000, "True")')
		worksheet2.write_formula('B27', '=COUNTIF(Results!N2:N10000, "True")')
		worksheet2.write_formula('B28', '=COUNTIF(Results!O2:O10000, "True")')
		worksheet2.write_formula('B29', '=COUNTIF(Results!P2:P10000, "True")')
		worksheet2.write_formula('B30', '=COUNTIF(Results!Q2:Q10000, "True")')
		worksheet2.write_formula('B31', '=COUNTIF(Results!R2:R10000, "True")')
		worksheet2.write_formula('B32', '=COUNTIF(Results!S2:S10000, "True")')
		worksheet2.write_formula('B33', '=COUNTIF(Results!T2:T10000, "Secure Renegotiation Allowed Possible DoS")')



workbook.close()
