
#include <stdio.h>
#include <stdlib.h>

/// \param n le nombre de cinémas
/// \param redirection le lieu de redirection de chaque cinéma
void trajets_retour(int n, int *redirection)
{
    int cnt;
    int cinema;
    int nouveau_cinema;
    int chemin[n];
    for (int i = 0; i < n; i++)
    {
        cnt = 1;
        cinema = i + 1;
        chemin[0] = cinema;
        nouveau_cinema = redirection[cinema - 1];
        while (!appartient(chemin, nouveau_cinema, cnt))
        {
            cinema = nouveau_cinema;
            chemin[cnt] = cinema;
            cnt++;
            nouveau_cinema = redirection[cinema - 1];
        }
        printf("%d ", cnt);
    }
}

int appartient(int *tab, int elem, int n)
{
    for (int i = 0; i < n; i++)
    {
        if (tab[i] == elem)
        {
            return 1;
        }
    }
    return 0;
}

int main()
{
    int n;
    scanf("%d", &n);
    int *redirection = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; ++i)
        scanf("%d", &redirection[i]);
    trajets_retour(n, redirection);

    return 0;
}
