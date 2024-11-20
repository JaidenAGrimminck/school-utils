(*
Install script for the macos-statusbar app.
*)

-- First, we need to make the install script (using the `osascript` command) executable.
do shell script "make install"

--print
display dialog "Successfully compiled script, now installing" buttons {"OK"} default button 1

-- Next, we need to run the install script and log the output.
do shell script "./install > ./macos-statusbar-install.log"

display dialog "Finished running!" buttons {"OK"} default button 1

-- Next, we want to check if "SUCCESS" appears in the log file.
set logFile to "./macos-statusbar-install.log"
set fileRef to open for access (POSIX file logFile)
set logContents to read fileRef
close access fileRef
if logContents contains "SUCCESS" then
    display dialog "Installation successful!" buttons {"OK"} default button 1
else
    display dialog "Installation failed. Please check the log file for more information." buttons {"OK"} default button 1
    -- We want to display the log file to the user.
    do shell script "open -a 'TextEdit' " & logFile

    -- Remove the install script.
    do shell script "rm ./install"

    -- Then close the script, returning an error code.
    error "Installation failed."
end if

-- Finally, we want to clean up the log file.
do shell script "rm " & logFile

-- Remove the install script.
do shell script "rm ./install"

-- Copy "example-data" folder to a new "data" folder if it doesn't exist.
do shell script "cp -r example-data data"

-- Then, we're done!
return "SUCCESS"



