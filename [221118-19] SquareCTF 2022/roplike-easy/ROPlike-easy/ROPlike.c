#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include <time.h>
#include <stdint.h>
#ifdef DEBUG
#include <errno.h>
#endif

/*
- hard mode should tighten up the vulnerable functions, no more print file, make the price of key gadgets way higher,
remove syscall gadget 20.s, or maybe seccomp execve? also reduce TOTAL_ROP_GADGETS by 1 to remove the syscall gadget
from the pool, but don't remove the gadget for the big brains who realize its gadget #61
- current vulnerable functions:
    - print_file() can be reused to print flag
    - gadget selection in main() can be abused to buy unavailable gadget IDs
*/

#define TOTAL_ROP_GADGETS 62
#define GADGETS_PER_ROUND 5
#define MAX_ROUNDS 100
#define ROP_PAYLOAD_SIZE 256

int available_gadgets[5];
char gadgets_dir[16] = "./gadgets/";

char *current_page = (char *)0x100000;

void timed_scroll(int iters)
{
    for (int i = 0; i < iters; i++) {
        sleep(1);
        puts("\n");
    }
}

char *get_gadget_fname(int gadget_id, char fname[])
{
    sprintf(fname, "./gadgets/%i", gadget_id);
    return fname;
}

void wipe_arr(char *arr, int size)
{
    for (int i = 0; i < size; i++)
    {
        arr[i] = 0;
    }
}

void hex_string_to_byte_array(char *hex_str, char *byte_arr, int size)
{
    int byte_ind = 0;
    for (int count = 0; count < size; count += 2)
    {
        sscanf(&hex_str[count], "%2hhx", &byte_arr[byte_ind]);
        byte_ind++;
    }
}

// this can also easily be used for memory leaks
void print_buf(unsigned char *buf, int sz)
{
    for (int i = 0; i < sz; i++)
    {
        printf("%02X", buf[i]);
    }
}

// this can totally be used to print out the flag file for anyone who notices
void print_file(char fname[])
{
    char raw_file[256];
    FILE *fp = fopen(fname, "r");
    struct stat st_info;
    stat(fname, &st_info);
    fread(raw_file, st_info.st_size, 1, fp);
    print_buf(raw_file, st_info.st_size);
    printf("\n");
    fclose(fp);
}

void print_gadget(int gadget_id)
{
#ifdef DEBUG
    printf("gadget ID: %i\n\t", gadget_id);
#endif
    char fname[16];
    get_gadget_fname(gadget_id, fname);
    print_file(fname);
}

FILE *read_gadget(int gadget_id)
{
}

void *load_gadget(int gadget_id)
{
    char fname[16];
    char raw_gadget[256];

    get_gadget_fname(gadget_id, fname);
    int fd = open(fname, O_RDONLY);
#ifdef DEBUG
    printf("load gadget fd %i\n", fd);
#endif
    void *mapping = mmap(current_page, 0x1000, PROT_EXEC | PROT_READ, MAP_PRIVATE | MAP_FIXED, fd, 0);

#ifdef DEBUG
    printf("Mapped gadget ID %i, to %p, errno %s\n", gadget_id, mapping, strerror(errno));
#endif
    current_page += 0x1000;

    close(fd);
    return mapping;
}

int get_gadget_price(int gadget_id)
{
    char fname[16];
    get_gadget_fname(gadget_id, fname);

    int price;
    FILE *fp = fopen(fname, "r");
    struct stat st_info;
    stat(fname, &st_info);
    fread((void *)&price, 4, 1, fp);
    return price;
}

void open_shop(int32_t *wallet)
{
    int gadgets_in_store[GADGETS_PER_ROUND];

    for (int gadget_num = 0; gadget_num < GADGETS_PER_ROUND; gadget_num++)
    {
        printf("Gadget %i:", gadget_num);
        int random_gadget_id = rand() % TOTAL_ROP_GADGETS;
        print_gadget(random_gadget_id);
        gadgets_in_store[gadget_num] = random_gadget_id;
    }
    while (1)
    {
        printf("\n\nFunds available: %i\nSelect a gadget to purchase or enter 'c' to continue\n", *wallet);
        char selection[4];
        fgets(selection, 4, stdin);
        if (selection[0] == 'c')
        {
            break;
        }
        else // this means we're purchasing a gadget
        {
            if (selection[0] < 0x30 || selection[0] > 0x39)
            {
                puts("Please input a valid selection");
                continue;
            }
            int selected_gadget = selection[0] & 0xcf;

            // this should be exploitable to pick gadgets that aren't actually available in the store,
            // most likely gadget 0 but it can probably be massaged
            int selected_gadget_id = gadgets_in_store[selected_gadget];
            int gadget_price = get_gadget_price(selected_gadget_id);
            printf("price %i\n", gadget_price);
            if (gadget_price <= *wallet)
            {
                *wallet = *wallet - gadget_price;
                load_gadget(selected_gadget_id);
                printf("Gadget purchased!\n");
            }
            else
            {
                puts("Sorry, please get more Roppis.\n");
            }
        }
    }
}

int rop_time(char *hex_str, int bytes_read)
{
    puts("Loading ROP payload...");
    timed_scroll(3);
    // this looks pointless but its to convince the compiler to put local copies of these variables BEFORE the input_buf
    struct {
    char input_buf[ROP_PAYLOAD_SIZE];
    char *local_hex_str;
    int local_bytes_read;
    } locals;
    locals.local_bytes_read = bytes_read;
    locals.local_hex_str = hex_str;
    
    //char input_buf[ROP_PAYLOAD_SIZE];
    // char *local_hex_str = hex_str;
    // int local_bytes_read = bytes_read;

    wipe_arr(locals.input_buf, ROP_PAYLOAD_SIZE);
    hex_string_to_byte_array(locals.local_hex_str, locals.input_buf, locals.local_bytes_read);

    // place a "return pointer" at the end of the payload so that players don't NEED an ASLR leak to survive
    *(size_t **)(&(locals.input_buf[locals.local_bytes_read / 2])) = &&after_ret;

    asm volatile("mov %0, %%rdx" : : "r"((locals.local_bytes_read / 2) + sizeof(size_t)));
    asm volatile("ret");
after_ret:
    // fix up the stack after all those rets
    asm volatile("sub %rdx, %rsp");
}



int main()
{
    puts("welcome to my new roguelike, ROPlike!\n\
    The rules are simple: you may purchase gadgets using your Roppi points.\n\
    Your goal is to survive as long as possible! thats it.\n\
    there definitely arent any flags in the binary directory or anything.\n\
    Nope.\n\
    Just wholesome roguelite fun.\n");
    timed_scroll(3);

    int32_t wallet = 2;
    char rop_payload_hex[ROP_PAYLOAD_SIZE * 2];
    srand(time(0));

    for (int round_counter = 1; round_counter <= MAX_ROUNDS; round_counter++)
    {
        wipe_arr(rop_payload_hex, sizeof(rop_payload_hex));
        printf("Starting round %i!\nAvailable gadgets:\n", round_counter);

        open_shop(&wallet);

        puts("Beginning the ROP phase! time to set up your stack:\n");
        int input_bytes = read(0, rop_payload_hex, sizeof(rop_payload_hex));
        if (rop_payload_hex[input_bytes - 1] == 0x0a)
        {
            rop_payload_hex[input_bytes - 1] = 0;
            input_bytes -= 1;
        }

        puts("Lets take a look at your payload...");
        timed_scroll(1);
        printf("hmmm, that payload looks like its worth just about %li Roppis! Lets give it a whirl.\n", (input_bytes / 2) / sizeof(size_t));
        wallet += (input_bytes / 2) / sizeof(size_t);

        rop_time(rop_payload_hex, input_bytes);
        puts("Round survived!\n");
    }
}
