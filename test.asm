// test.asm – Programme minimal sans aucun symbole
// Met la valeur 1 dans D, la stocke dans RAM[0], puis boucle infinie.
@1      // A = 1 (constante décimale)
D=A     // D = A  (donc D = 1)
@0      // A = 0 (adresse de RAM[0])
M=D     // RAM[0] = D
@6      // A = 6 (adresse de l'instruction suivante pour saut)
0;JMP   // saut inconditionnel à l'adresse contenue dans A (6), boucle infinie