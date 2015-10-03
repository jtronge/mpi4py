# Author:  Lisandro Dalcin
# Contact: dalcinl@gmail.com

$MS_DOWNLOAD_URL   = "http://download.microsoft.com/download/"
$MSMPI_HASH_URL_V5 = "3/7/6/3764A48C-5C4E-4E4D-91DA-68CED9032EDE/"
$MSMPI_HASH_URL_V6 = "6/4/A/64A7852A-A8C3-476D-908C-30501F761DF3/"
$MSMPI_BASE_URL    = $MS_DOWNLOAD_URL + $MSMPI_HASH_URL_V6

$ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
. "$ScriptDir\download.ps1"
$DOWNLOADS = "C:\Downloads\MSMPI"

function InstallMicrosoftMPISDK ($baseurl, $filename) {
    Write-Host "Installing Microsoft MPI SDK"
    $url = $baseurl + $filename
    $filepath = Download $url $filename $DOWNLOADS
    Write-Host "Installing" $filename
    $prog = "msiexec.exe"
    $args = "/quiet /qn /i $filepath"
    Write-Host "Executing:" $prog $args
    Start-Process -FilePath $prog -ArgumentList $args -Wait
    Write-Host "Microsoft MPI SDK installation complete"
}

function InstallMicrosoftMPIRuntime ($baseurl, $filename) {
    Write-Host "Installing Microsoft MPI Runtime"
    $url = $baseurl + $filename
    $filepath = Download $url $filename $DOWNLOADS
    Write-Host "Installing" $filename
    $prog = $filepath
    $args = "-unattend"
    Write-Host "Executing:" $prog $args
    Start-Process -FilePath $prog -ArgumentList $args -Wait
    Write-Host "Microsoft MPI Runtime installation complete"
}

function SaveMicrosoftMPIEnvironment ($filepath) {
    Write-Host "Saving Microsoft MPI environment variables to" $filepath
    $envlist = @("MSMPI_BIN", "MSMPI_INC", "MSMPI_LIB32", "MSMPI_LIB64")
    $stream = [IO.StreamWriter] $filepath
    foreach ($variable in $envlist) {
        $value = [Environment]::GetEnvironmentVariable($variable, "Machine")
        if ($value) { $stream.WriteLine("SET $variable=$value") }
        if ($value) { Write-Host "$variable=$value" }
    }
    $stream.Close()
}

function InstallMicrosoftMPI () {
    InstallMicrosoftMPISDK $MSMPI_BASE_URL "msmpisdk.msi"
    InstallMicrosoftMPIRuntime $MSMPI_BASE_URL "MSMpiSetup.exe"
    SaveMicrosoftMPIEnvironment "SetEnvMPI.cmd"
}

function main () {
    InstallMicrosoftMPI
}

main