^4::
run picture-crop.bat
return

#IfWinActive ahk_exe Explorer.EXE
^+c::
	Clipboard:=""
	Send, {CTRLDOWN}c{CTRLUP}
	ClipWait,1
	path:=Clipboard
    Clipboard = %path%
	if ErrorLevel
		return
return
#IfWinActive	





;############## IfanViewer copy path ; Ctrl+Shift+C 
#NoEnv ; 不检查空变量是否为环境变量(建议所有新脚本使用).
SendMode Input ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.

#IfWinActive ahk_class IrfanView
^+c::
clipboard =
DllCall("SendMessage", UInt, WinActive("A"), UInt, 80, UInt, 1, UInt, DllCall("LoadKeyboardLayout", Str,"00000409", UInt, 1))
Send, i      ; Simulate key press "i" to open image properties dialog box (ipdb).
sleep, 50
Send, {TAB 3}
Send, {CTRLDOWN}c{CTRLUP}
ClipWait,1
Send, {ALTDOWN}o{ALTUP} ; Quits the ipdb
if ErrorLevel
	return
#IfWinActive
