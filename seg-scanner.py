#!/usr/bin/python
########################################################################################
#
#  Segmentation Scanner and Parser
#  Created: Matt Molda
#  Date: 4/1/2016
#  Description:  
#  Used to scan a secure enclave and then produce spreadsheet of findings 
#  and table that can be imported into a report.
#
#########################################################################################


import xlsxwriter
import datetime






#get date and format
now = datetime.datetime.now()
info = now.strftime("%m_%d_%Y_%H_%M")


#set common values
state = "validated"
status = "Open"
title = "PCI-DSS and/or SOC2 violation of Segmentation Controls"
desc = "Inadequate Network Segmentation Controls  in Place Allowing Traffic Between an Unsecured Network Enclave and a Secured Network Enclave"
recommend = "Provide sufficient controls by either moving identified hosts into a secure enclave or setting up firewall rules in order to prevent disallowed traffic."
notes = "https://www.pcisecuritystandards.org/documents/Penetration_Testing_Guidance_March_2015.pdf"

#setup worksheet
name = "Segmentation_Results" + "_" + info + ".xlsx"
workbook = xlsxwriter.Workbook(name)
worksheet = workbook.add_worksheet('Vuln List')
bold = workbook.add_format({'bold': True})

# write column headers
worksheet.write('A1', 'Finding #')
worksheet.write('B1', 'State')
worksheet.write('C1', 'Status')
worksheet.write('D1', 'Finding Title')
worksheet.write('E1', 'System Name')
worksheet.write('F1', 'System IP' )
worksheet.write('G1', 'Port')
worksheet.write('H1', 'Technical Risk')
worksheet.write('I1', 'Business Risk')
worksheet.write('J1', 'CVSS Base Score')
worksheet.write('K1', 'CVE')
worksheet.write('L1', 'Description')
worksheet.write('M1', 'Recommendations')
worksheet.write('N1', 'Notes')
worksheet.write('N1', 'Detail')


