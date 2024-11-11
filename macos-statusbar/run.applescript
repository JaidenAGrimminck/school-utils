
-- quickly make the Python check script executable
do shell script "make check"

-- Next, we need to run the install script and log the output.
do shell script "./check > ./py-check.log"

set output to do shell script "cat ./py-check.log"

if output contains "NO" then
    display dialog "Python not installed. Please run the install script to install all necessary packages!" buttons {"OK"} default button 1
    
    -- delete the makefile
    do shell script "rm ./check"
    do shell script "rm ./py-check.log"

    -- Then close the script, returning an error code.
    error "Python not installed."
else
    do shell script "rm ./check"
    do shell script "rm ./py-check.log"
    do shell script "python3 main.py"

    return "successfully finished running!"
end if