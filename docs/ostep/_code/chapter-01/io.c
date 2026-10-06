#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>
#include <fcntl.h>
#include <sys/types.h>

int main(void) {
    int fd = open("/tmp/file", O_WRONLY | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    assert(fd > -1);
    const char *msg = "hello world\n";
    ssize_t rc = write(fd, msg, strlen(msg));   // 12 bytes, no '\0'
    assert(rc == (ssize_t) strlen(msg));
    rc = fsync(fd);                              // ask the OS to push it to the device
    assert(rc == 0);
    close(fd);
    return 0;
}
