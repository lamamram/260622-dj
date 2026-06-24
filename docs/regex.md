# expressions régulieres

## définition

> regex: chaîne de caractères qui représente un modèle de chaines de caractère
> xxx.yyy@zzz.ttt.ee => adresse email

## méta-langage de regex

* `chat`: n'importe quelle string intercepte **match** qui contient **chat**
* `ch.t`: => chat chbt chct ch!t .... ch4t ... => `.`: n'inmporte quel caractère
* `^chat`:  //                                         qui débute avec chat
* `chat$`: //   qui termine avec chat
* `^chat$`: exactement chat
* années du 21ème siècle: `2(00[1-9]|0[1-9][0-9]|100)` : **(|)** alternatives, **[]**: choix possible pour *un catactère donné* de la cible
* `[^!]`: tout sauf `!`
* date du 21ème (presque bonne): `2(00[1-9]|0[1-9][0-9]|100)[/ -](0[1-9]|1[0-2])[/ -](0[1-9]|1[0-9]|2[0-9]|3[0-1]))`
* email

* quantificateur:
  + `?`: 0 ou 1 fois
  + `+`: 1 ou plusieurs fois
  + `*`: 0 ou plusieurs fois
  + `{n}`: exactement n fois
  + `{n,}`: au - n fois
  + `{n,m}`: entre n et m fois
               (-----groupe-----)
`[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*@...`

> truc@...
> truc-bidule33.machin9@...