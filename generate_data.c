#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define TOTAL_ROWS 15200000

const char *products[] = {"Laptop", "Mouse", "Keyboard", "Monitor", "Headset"};
double prices[]        = {999.99,    29.99,    79.99,      349.99,    89.99};
const char *regions[]  = {"North", "South", "East", "West"};

void make_uuid(char *out) {
    const char *hex = "0123456789abcdef";
    for (int i = 0; i < 36; i++) {
        if (i == 8 || i == 13 || i == 18 || i == 23) out[i] = '-';
        else if (i == 14) out[i] = '4';
        else if (i == 19) out[i] = hex[8 + rand() % 4];
        else out[i] = hex[rand() % 16];
    }
    out[36] = '\0';
}

int main() {
    srand(time(NULL));

    FILE *f = fopen("sales.csv", "w");
    fprintf(f, "transaction_id,date,product,region,quantity,unit_price\n");

    struct tm start = {0};
    start.tm_year = 2024 - 1900;
    start.tm_mon = 0;
    start.tm_mday = 1;
    start.tm_hour = 12;
    time_t start_time = mktime(&start);

    char uuid[37];
    char datestr[11];

    for (int i = 0; i < TOTAL_ROWS; i++) {
        make_uuid(uuid);

        int days = rand() % 365;
        time_t t = start_time + (time_t)days * 86400;
        struct tm *d = gmtime(&t);
        strftime(datestr, sizeof(datestr), "%Y-%m-%d", d);

        int pidx = rand() % 5;
        int ridx = rand() % 4;
        int quantity = rand() % 5 + 1;

        fprintf(f, "%s,%s,%s,%s,%d,%.2f\n",
                uuid, datestr, products[pidx], regions[ridx], quantity, prices[pidx]);
    }

    fclose(f);
    return 0;
}
