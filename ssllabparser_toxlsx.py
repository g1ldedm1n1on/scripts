#!/usr/bin/python
#  Created by Matt Molda, base code from https://github.com/xme/toolbox/blob/master/ssllabs-scan-parse.py
# run ssllabs-scan and output file to json then pipe through this or cat output and pipe through this to create spreadsheet
# sample cat myscan.json | ./ssllabparser_toxslx.py
#sample ssllabs-scan --host-file=mydomains.txt --quiet > mydomains.json && cat mydomains.json | ./ssllabparser_toxslx.py


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
workbook = xlsxwriter.Workbook('SSL_Data.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1', 'Site Name', bold)
worksheet.write('B1', 'Port', bold)
worksheet.write('C1', 'SSL Labs Grade', bold)
worksheet.write('D1', 'Certificate Issuer', bold)
worksheet.write('E1', 'Certificate Expiration', bold)
worksheet.write('F1', 'Certificate MD5 Hash', bold)
worksheet.write('G1', 'Certificate Size', bold)
worksheet.write('H1', 'Certificate Strength', bold)
worksheet.write('I1', 'HeartBleed', bold)
worksheet.write('J1', 'HeartBeat', bold)
worksheet.write('K1', 'OpenSSL CCS', bold)
worksheet.write('L1', 'Poodle', bold)
worksheet.write('M1', 'Fallback SCSV', bold)
worksheet.write('N1', 'Freak', bold)
worksheet.write('O1', 'Logjam', bold)
worksheet.write('P1', 'Supports RC4', bold)
#workbook.close()

row = 1
col = 0
for site in data:
	if site:
		endpoints = site['endpoints']
        	certExp = time.ctime(int(endpoints[0]['details']['cert']['notAfter']/1000))
        	certRaw = endpoints[0]['details']['chain']['certs'][0]['raw']
		cert5 = md5.new(certRaw).hexdigest()

		domain = site['host']
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
		fallback = endpoints[0]['details']['fallbackScsv']
		freak = endpoints[0]['details']['freak']
		logjam = endpoints[0]['details']['logjam']
		rc4 = endpoints[0]['details']['supportsRc4']
		print domain, port, grade, issuer, date, size, alg
# output data to xlsx
		worksheet.write(row, col, domain)
		worksheet.write(row, col + 1,  port)
		worksheet.write(row, col + 2, grade)
		worksheet.write(row, col + 3, issuer)
		worksheet.write(row, col + 4, date)
		worksheet.write(row, col + 5, size)
		worksheet.write(row, col + 6, alg)
		worksheet.write(row, col + 7, strength)
		worksheet.write(row, col + 8, heartbled)
		worksheet.write(row, col + 9, heartbeat)
		worksheet.write(row, col + 10, opensslccs)
		worksheet.write(row, col + 11, poodle)
		worksheet.write(row, col + 12, fallback)
		worksheet.write(row, col + 13, freak)
		worksheet.write(row, col + 14, logjam)
		worksheet.write(row, col + 15, rc4)
		row += 1
	else:
		break
workbook.close()
