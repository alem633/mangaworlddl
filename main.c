#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void make_chapters_list(char*);
void download_chapters();

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("missing argouments\n"
               "%s [manga link]", argv[0]);
        return -1;
    }
    make_chapters_list(argv[1]);
    download_chapters();

    return 0;
}

void make_chapters_list(char *link) {
    char *command = malloc(strlen("python3 chapfinder.py ") + strlen(link) + 1);  
    if (command == NULL) 
        exit(EXIT_FAILURE);
    
    snprintf(command, strlen("python3 chapfinder.py ") + strlen(link) + 1, "python3 chapfinder.py %s", link);
    system(command);

    free(command);
}

void download_chapters() {
    FILE *chapter_list = fopen("chapters.txt", "r");
    if (chapter_list == NULL) {
        perror("Error opening chapters.txt");
        exit(EXIT_FAILURE);
    }

    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), chapter_list) != NULL) {
        buffer[strcspn(buffer, "\n")] = '\0';

        char *chapter = malloc(strlen(buffer) + 1);
        if (chapter == NULL) {
            perror("Memory allocation for chapter failed");
            exit(EXIT_FAILURE);
        }
        strcpy(chapter, buffer);

        char *command = malloc(strlen("python3 chapdl.py ") + strlen(chapter) + 1);
        if (command == NULL) {
            perror("Memory allocation for command failed");
            free(chapter);
            exit(EXIT_FAILURE);
        }

        snprintf(command, strlen("python3 chapdl.py ") + strlen(chapter) + 1, "python3 chapdl.py %s", chapter);

        system(command);

        free(command);
        free(chapter);
    }

    fclose(chapter_list);
}

