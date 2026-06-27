@echo off
:: Layan Gold Cursors - uninstaller
:: Removes the scheme registration and resets the per-role cursor settings
:: that the installer set.
::
:: Files in C:\Windows\Cursors\Layan Gold Cursors\ are NOT deleted automatically
:: (would require admin). Remove that folder manually after running this script.

REG DELETE "HKCU\Control Panel\Cursors\Schemes" /v "Layan Gold Cursors" /f >nul 2>&1

for %%R in (Arrow Help AppStarting Wait Crosshair IBeam NWPen No SizeNS SizeWE SizeNWSE SizeNESW SizeAll UpArrow Hand) do (
    REG DELETE "HKCU\Control Panel\Cursors" /v %%R /f >nul 2>&1
)
REG DELETE "HKCU\Control Panel\Cursors" /ve /f >nul 2>&1

echo x=msgbox("Layan Gold Cursors uninstalled." & vbCrLf & vbCrLf & "Sign out and back in (or restart Explorer) to fully clear cached cursors." & vbCrLf & vbCrLf & "To remove the files, manually delete:" & vbCrLf & "C:\Windows\Cursors\Layan Gold Cursors\\", 0+64, "Layan Gold Cursors") > "%tmp%\layan_gold_uninstall.vbs"
wscript "%tmp%\layan_gold_uninstall.vbs"
del "%tmp%\layan_gold_uninstall.vbs"
