#include "knapcore.h"
#include <math.h>
#include <stdlib.h>

/* flat distribution over the range [low, high] inclusive */
static int rngrandom(int low, int high) {
    int q = high - low + 1;
    return random() % q + low;
}

/*
 * w is weight [1, wm]
 * wm is max weight
 * k is exponent
 * d is -1 for more small, 1 fot more big things, 0 for does not mattter
 */
static int go(int w, int wm, double k, int dir) {
    double thr;
    switch (dir) {
        case 0:
            return 1;
        case -1:
            thr = RAND_MAX / pow(w, k);
            break;
        case 1:
            thr = RAND_MAX / pow(wm - w + 1, k);
            break;
    }
    if (thr >= random())
        return 1;
    return 0;
}

/*
 * knapcore returns total weight
 * n is total number of things
 * wmax is max generated weight
 * cmax is max cost (min cost = 1)
 * ke is exponent
 */
int knapcore(int* weights, int* costs, int n, int wmax, int cmax, double ke, int d) {
    int* issued = (int*)malloc((wmax + 1) * sizeof(int));
    int  k;
    long ttw, tw, w;

    if (!issued)
        return 0;   /* indicates memory alloc failure */

    for (k = 0; k < wmax; k++)
        issued[k] = 0;
    tw = 0;

    k = 0;
    while (k < n) {
        w = rngrandom(1, wmax);
        /* already have a thing with this weight */
        if (issued[w] > 0)
            continue;

        if (go(w, wmax, ke, d)) {
            costs[k] = issued[w] = rngrandom(1, cmax);
            weights[k] = w;
            tw += w;
            k++;
        }
    }
    free(issued);
    return tw;
}
