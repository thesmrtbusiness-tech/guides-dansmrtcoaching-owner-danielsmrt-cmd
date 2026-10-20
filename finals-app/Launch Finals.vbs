' Starts the Finals app with no console window and opens it in the browser.
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
script = """" & dir & "\server.py"""

If sh.Run("cmd /c where pyw >nul 2>nul", 0, True) = 0 Then
  sh.Run "pyw " & script, 0, False
ElseIf sh.Run("cmd /c where pythonw >nul 2>nul", 0, True) = 0 Then
  sh.Run "pythonw " & script, 0, False
Else
  MsgBox "Finals needs Python, which isn't installed yet." & vbCrLf & vbCrLf & _
         "1. Go to python.org/downloads and install it." & vbCrLf & _
         "2. Then double-click the Finals shortcut again.", vbExclamation, "Finals"
End If
