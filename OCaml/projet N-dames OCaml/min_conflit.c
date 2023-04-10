#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <sys/time.h>
#include <time.h>

void place_n_reines(int *reines, int n)
{
    for (int i = 0; i < n; i++)
    {
        reines[i] = rand() % n;
    }
}

int indice_min(int *array, int n)
{
    int min = array[0];
    int inds[n];
    inds[0] = 0;
    int nb_indices = 1;
    for (int i = 1; i < n; i++)
    {
        if (array[i] < min)
        {
            min = array[i];
            inds[0] = i;
            nb_indices = 1;
        }
        else if (array[i] == min)
        {
            inds[nb_indices] = i;
            nb_indices++;
        }
    }
    return inds[rand() % nb_indices];
}

void max_conflits(int *reines, int n, int *ligne, int *max)
{
    int col[n];
    int diag1[2 * n];
    int diag2[2 * n];
    int value;
    int temp;
    int inds[n];
    int nb_indices = 1;
    for (int i = 0; i < 2 * n; i++)
    {
        if (i < n)
        {
            col[i] = 0;
        }
        diag1[i] = 0;
        diag2[i] = 0;
    }
    for (int i = 0; i < n; i++)
    {
        value = reines[i];
        col[value]++;
        diag1[value + i]++;
        diag2[n - value + i]++;
    }
    for (int i = 0; i < n; i++)
    {
        value = reines[i];
        temp = col[value] + diag1[value + i] + diag2[n - value + i] - 3;
        if (temp > *max)
        {
            *max = temp;
            inds[0] = i;
            nb_indices = 1;
        }
        else if (temp == *max)
        {
            inds[nb_indices] = i;
            nb_indices++;
        }
    }
    *ligne = inds[rand() % nb_indices];
}

int min_conflits(int *reines, int ligne, int n)
{
    int conflits[n];
    int temp;
    for (int i = 0; i < n; i++)
    {
        conflits[i] = 0;
    }
    for (int i = 0; i < n; i++)
    {
        if (i != ligne)
        {
            conflits[reines[i]]++;
            temp = reines[i] - i + ligne;
            if (0 <= temp && temp < n)
            {
                conflits[temp]++;
            }
            temp = reines[i] + i - ligne;
            if (0 <= temp && temp < n)
            {
                conflits[temp]++;
            }
        }
    }
    return indice_min(conflits, n);
}

bool reparer(int *reines, int n)
{
    int ligne;
    int nb_conflits = -1;
    max_conflits(reines, n, &ligne, &nb_conflits);
    reines[ligne] = min_conflits(reines, ligne, n);
    return nb_conflits != 0;
}

int *solution(int n)
{
    int iter_max = 2 * n;
    int *reines = malloc(sizeof(int) * n);
    place_n_reines(reines, n);
    int iter_count = 0;
    while (reparer(reines, n))
    {
        iter_count++;
        if (iter_count == iter_max)
        {
            place_n_reines(reines, n);
            iter_count = 0;
        }
    }
    return reines;
}

void print_solution(int *reines, int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (j == reines[i])
            {
                printf("|x");
            }
            else
            {
                printf("| ");
            }
        }
        printf("|\n");
    }
}

int main(int argc, char **argv)
{
    srand(time(NULL));
    struct timeval stop, start;
    gettimeofday(&start, NULL);

    int *reines;
    if (argc > 1)
    {
        int n = atoi(argv[1]);
        reines = solution(n);
        // print_solution(reines, n);
    }
    else
    {
        reines = solution(8);
    }

    gettimeofday(&stop, NULL);
    printf("Temps d'exécution : %lu ms\n", ((stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec) / 1000);

    free(reines);
    return 0;
}