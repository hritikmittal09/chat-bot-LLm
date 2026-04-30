' Silent launcher for Chat-Bot LLM
' This runs the .bat file without showing a CMD window on startup
' Place this .vbs file in E:\chat-bot-LLm\ alongside run_chatbot.bat

Dim WShell
Set WShell = CreateObject("WScript.Shell")

' Run the batch file - change path if needed
WShell.Run """E:\chat-bot-LLm\run_chatbot.bat""", 1, False

Set WShell = Nothing
