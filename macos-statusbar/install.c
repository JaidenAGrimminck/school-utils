#include <stdio.h>
#include <stdlib.h>

int checkScript() {
    printf("INFO - Checking if everything is OK...\n");
    int check = system("python3 main.py test > /dev/null 2>&1");

    if (check == 0) {
        printf("INFO - Everything is OK!\n");
        printf("SUCCESS - Installation complete!\n");

        return 0;
    } else {
        printf("FAIL - Something went wrong!\n");
    }

    return 1;
}

int installPackages() {
    printf("INFO - Attempting to install required packages...\n");
    // first, check if we're in the right directory (should have requirements.txt)
    int check = system("ls requirements.txt > /dev/null 2>&1");

    if (check == 0) {
        // install the required packages
        int install = system("pip3 install -r requirements.txt");

        if (install == 0) {
            printf("INFO - Required packages installed!\n");
            return checkScript();
        } else {
            printf("FAIL - Required packages failed to install!\n");
        }
    } else {
        printf("FAIL - requirements.txt not found!\n");
    }

    return 1;
}

int main() {
    int check = system("python3 --version > /dev/null 2>&1");

    if (check == 0) {
        printf("INFO - Python3 installed!\n");
        return installPackages();
    } else {
        printf("INFO - Python3 not installed! Attempting to install...\n");

        #ifdef __linux__
            printf("FAIL - This program only works on MacOS!\n");
        #elif __APPLE__
            int install = system("brew install python3");

            if (install == 0) {
                printf("INFO - Python3 installed!\n");
                return installPackages();
            } else {
                printf("FAIL - Python3 failed to install!\n");
            }
        #else
            printf("FAIL - This program only works on MacOS!\n");
        #endif
    }

    return 1;
}

