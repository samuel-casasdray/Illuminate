#
#
# void diagonaleRow(int x, int old, int n, bool right) {
#     int j, i;
#     if (right) {
#         j = 0;
#         for (i = x; i < rowNumber && j < colNumber; i++) {
#             replaceGrille(i, j, n, old);
#             j++;
#         }
#     } else {
#         j = colNumber;
#         for (i = x; i < rowNumber && j >= 0; i++) {
#             replaceGrille(i, j, n, old);
#             j--;
#         }
#     }
# }
#
# void diagonaleCol(int x, int old, int n, bool right) {
#     int j, i;
#     if (right) {
#         j = 0;
#         for (i = x; i < colNumber && j < rowNumber; i++) {
#             replaceGrille(j, i, n, old);
#             grille[j][i] = 1;
#             j++;
#         }
#     } else {
#         j = 0;
#         for (i = x; i >= 0 && j < rowNumber; i--) {
#             replaceGrille(j, i, n, old);
#             j++;
#         }
#     }
# }
