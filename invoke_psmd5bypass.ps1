<#
Invoke-PSMD5Bypass

This script was built to bypass MD5 signatures used by AV for potentially unwanted PowerShell scripts.
This can be used to quickly modify powershell scripts in a directory to change MD5 sum values.
Appends a commented area with random data at the end of the .ps1 file.

Created:Matt Molda

#>


function Invoke-PSMD5Bypass {

<#

    .SYNOPSIS
    Modifies all PS1 files in a directory path to change MD5 value to bypass AV

    .DESCRIPTION
    This function will append to the end of each PS1 file a comment section of random data to change
    the MD5 Hash of the File.

    .PARAMETER DIR
    The parent directory to search in for .ps1 files

    .OUTPUTS
    Modified PS1 File

    .EXAMPLE
    Invoke-PSMD5Bypass -dir C:\powershell
        Modifying File:  C:\pstest\Invoke-NinjaCopy.ps1
        Current MD5 Hash  62309A2F61F5C8CF67187EA750406DF1
        New MD5 Hash : 482475183656CD842F3701FB298B54FD
        Modifying File:  C:\pstest\Invoke-TokenManipulation.ps1
        Current MD5 Hash  413C73870443C6BA7AA8685D0FDD7EBF
        New MD5 Hash : 600963A46C5C28A3947D25AA7D670C90
    #>


param(
     [Parameter(Mandatory=$true, Position=0)]
 [Alias('path')]
 [System.String]
 ${dir})

 begin
 {


#declare
 $psfiles = @()
 $files = ""

 # Get the path to PS1 files in the directory provided
 $psfiles += get-childitem $dir -Filter *.ps1 -Recurse | Foreach-Object {$_.FullName}




# Loop through each file to get hash
foreach ( $files in $psfiles ) 
    {
        Write-Host "Modifying File: " $files
        $hash = (Get-FileHash $files -Algorithm MD5).hash
        write-host "Current MD5 Hash " $hash -ForegroundColor Yellow
        $rand = -join ((1..200) | %{(65..90) + (97..122) | Get-Random} | % {[char]$_})

        # append comment characters to random data
        $t = "<#"
        $u = "#>"
        $rand = $t + $rand
        $rand = $rand + $u

        # Append random data to file
        $rand | Out-File -FilePath $files -Append -Encoding ascii

        # Compute new hash
        $newhash = (Get-FileHash $files -Algorithm MD5).hash
        write-host "New MD5 Hash :" $newhash -ForegroundColor Green
    }
}
}

