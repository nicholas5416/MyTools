#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char Global_Options[128];
void pwnit(){
    char buf[128];
    puts("Input Your Name: ");
    read(0, buf , 0x500);
    puts(buf);
}
int main() {
    char temp[21];
    puts("Very Secret System .");
    puts("Pwn It");
    pwnit();
} 