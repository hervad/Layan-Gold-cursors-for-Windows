# Uninstalls Layan Cursors (Gold). If the scheme is active, switches back to the Windows
# default cursors first, then removes the installed files and the scheme entry.
$ErrorActionPreference = 'Stop'
$scheme = 'Layan Cursors (Gold)'

$identity = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $identity.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

$key = 'HKCU:\Control Panel\Cursors'
if ((Get-ItemProperty $key).'(default)' -eq $scheme) {
    foreach ($role in 'Arrow', 'Help', 'AppStarting', 'Wait', 'Crosshair', 'IBeam', 'NWPen', 'No', 'SizeNS', 'SizeWE', 'SizeNWSE', 'SizeNESW', 'SizeAll', 'UpArrow', 'Hand') {
        Set-ItemProperty $key $role ''
    }
    Set-ItemProperty $key '(default)' 'Windows Default'
    $api = Add-Type -PassThru -Name Cursors -Namespace Win32 -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool SystemParametersInfo(uint action, uint param, System.IntPtr value, uint flags);
'@
    [void]$api::SystemParametersInfo(0x57, 0, [IntPtr]::Zero, 3)  # SPI_SETCURSORS: reload now
}

$inf = Join-Path $PSScriptRoot 'install.inf'
Start-Process rundll32.exe -Wait -ArgumentList "setupapi.dll,InstallHinfSection DefaultUninstall 132 $inf"
Write-Host "$scheme has been removed."
Read-Host 'Press Enter to close'
