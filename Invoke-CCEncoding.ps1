function Invoke-CCEncoding {
<#
  .SYNOPSIS
  Encodes Credit Card numbers into different encoding formats
  .DESCRIPTION
  Invoke-CCEncoding takes three arguments, the file to read that contains the credit card numbers to encode one per line, the encoding to use, and the output file
  .EXAMPLE
  Invoke-CCEncoding -File C:\path-to-file -Encoding base64 -Outfile C:\path-to-write-encoded-files
  .EXAMPLE
  Invoke-CCEncoding -File C:\path-to-file -Encoding binary -Outfile C:\path-to-write-encoded-files
  .PARAMETER File
  The path to the file containing credit cards to encode one per line
  .PARAMETER Encoding
  The encoding format to use
  .PARAMETER Outfile
  The path to the file to write encoded numbers to
  #>
  [CmdletBinding()]
  param
  (
    [Parameter(Position = 0, Mandatory=$True)]
    [string]$File,
		
    [Parameter(Position = 1, Mandatory = $True)]
    [ValidateSet(“binary”,”hex”,”base64”)]
    [string]$Encoding,

    [Parameter(Position = 2, Mandatory = $True)]
    [string]$Outfile

    )

begin {
    write-verbose "Starting to Encode..."
  }

 process {

    #declare variables
    $cc = @()
    $bytes = ""
    $encodedc = @()
    $encodedlist = @()

    Try {
    Write-Verbose "Getting Content from $File"
    $cc = Get-Content $File
    }

    Catch {
    Write-host -ForegroundColor Red "Unable to get file contents"
    }

    Try {
    if ($Encoding -eq 'base64') {
    Write-Verbose "Encoding Credit Cards in Base64"

        Foreach ($c in $cc) {
        $bytes = [System.Text.Encoding]::Unicode.GetBytes($c)
        $encodedc =[Convert]::ToBase64String($bytes)
        write-verbose $encodedc
        $encodedlist += $encodedc
        }
    }

    elseif ($Encoding -eq 'binary') {
    Write-Verbose "Encoding Credit Cards to Binary"
    Foreach ($c in $cc) {
        $c = $c.Replace("-","")
        $encodedc = [convert]::ToString($c, 2)
        Write-Verbose $encodedc
        $encodedlist += $encodedc
        }
    }

    elseif ($Encoding -eq 'hex') {
    Write-Verbose "Encoding Credit Cards to Hex"
    Foreach ($c in $cc) {
        $c = $c.Replace("-","")
        $encodedc = [convert]::ToString($c,16)
        $encodedc = "0x" + $encodedc
        Write-Verbose $encodedc
        $encodedlist += $encodedc
        }
    }

    }

    Catch {
        Write-Host -ForegroundColor Red "Unable to Encode. Something went wrong!"
          }


    Try {
        Write-Verbose "Writing Encoded Credit Cards to File..."
        #$outcontent = $encodedlist.ToString()
        $encodedlist | Out-File -Encoding ascii $Outfile
        }

    Catch {
        write-host -ForegroundColor Red "Failed to Output Encoded Credit Cards to OutFile. Check Path exists!"
        $ErrorMessage = $_.Exception.Message
        $FailedItem = $_.Exception.ItemName
        Write-Host $ErrorMessage
        Write-Host $FailedItemimport
        }

    write-verbose "Completed!"
}

}


function Invoke-CCDecoding {
<#
  .SYNOPSIS
  Decodes Credit Card numbers that were encoded using Invoke-CCEncoding
  .DESCRIPTION
  Invoke-CCDecoding takes three arguments, the file to read that contains the encoded credit card numbers to decode one per line, the encoding used to encode the credit cards, and the output file
  .EXAMPLE
  Invoke-CCDecoding -File C:\path-to-file -Encoding base64 -Outfile C:\path-to-write-decoded-files
  .EXAMPLE
  Invoke-CCDecoding -File C:\path-to-file -Encoding binary -Outfile C:\path-to-write-decoded-files
  .PARAMETER File
  The path to the file containing credit cards to encode one per line
  .PARAMETER Encoding
  The encoding format to was used to encode the credit card numbers
  .PARAMETER Outfile
  The path to the file to write decoded numbers to
  #>
  [CmdletBinding()]
  param
  (
    [Parameter(Position = 0, Mandatory=$True)]
    [string]$File,
		
    [Parameter(Position = 1, Mandatory = $True)]
    [ValidateSet(“binary”,”hex”,”base64”)]
    [string]$Encoding,

    [Parameter(Position = 2, Mandatory = $True)]
    [string]$Outfile

    )

begin {
    write-verbose "Starting to Decode..."
  }

 process {

    #declare variables
    $cc = @()
    $bytes = ""
    $decodedc = @()
    $decodedlist = @()

    Try {
    Write-Verbose "Getting Content from $File"
    $cc = Get-Content $File
    }

    Catch {
    Write-host -ForegroundColor Red "Unable to get file contents"
    }

    Try {
 
    if ($Encoding -eq 'base64') {
    Write-Verbose "Decoding Credit Cards from Base64"

        Foreach ($c in $cc) {
        $decodedc = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($c))
        write-verbose $decodedc
        $decodedlist += $decodedc

        }
    }

    elseif ($Encoding -eq 'binary') {
        Write-Verbose "Decoding Credit Cards from Binary"
        Foreach ($c in $cc) {
        $decodedc = [System.Convert]::ToInt64($c,2)
        $decodedc = $decodedc.ToString()
        $decodedc = $decodedc.Insert(4,'-')
        $decodedc = $decodedc.Insert(9,'-')
        $decodedc = $decodedc.Insert(14,'-')
        $decodedlist += $decodedc
        write-verbose $decodedc
            }
       
   
        }

    elseif ($Encoding -eq 'hex') {
    Write-Verbose "Decoding Credit Cards from Hex"
    Foreach ($c in $cc) {
        $decodedc = [int64[]]$c
        $decodedc = [string]$decodedc
        $decodedc = $decodedc.Insert(4,'-')
        $decodedc = $decodedc.Insert(9,'-')
        $decodedc = $decodedc.Insert(14,'-')
        Write-Verbose $decodedc
        $decodedlist += $decodedc
        }
    }

    }

    Catch {
        Write-Host -ForegroundColor Red "Unable to Decode. Something went wrong!"
          }


    Try {
        Write-Verbose "Writing Encoded Credit Cards to File..."
        $decodedlist | Out-File -Encoding ascii $Outfile
    }

    Catch {
        write-host -ForegroundColor Red "Failed to Output Decoded Credit Cards to OutFile. Check Path exists!"
        $ErrorMessage = $_.Exception.Message
        $FailedItem = $_.Exception.ItemName
        Write-Host $ErrorMessage
        Write-Host $FailedItemimport
    }

    write-verbose "Completed!"
}

}