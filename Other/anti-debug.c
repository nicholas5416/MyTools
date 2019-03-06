#include <signal.h>

int main()
{
	if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) 
	{
		printf("DEBUGGING... Bye\n");
		return 1;
	}
	printf("Hello\n");
	return 0;
}