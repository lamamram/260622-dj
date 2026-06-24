# %% ------------ la méthode match ------------------------
###### "matcher une regex"
# match == détecter la regex au début de la cible
import re

pattern = "([013456789][0-9]{4}|2[0-9AB][0-9]{3})"

print("cible exacte", re.match(pattern=pattern, string="44500"))
print("au début de la cible", re.match(pattern=pattern, string="44500 est mon zipcode"))
print(re.match(pattern=pattern, string="mon zipcode est 44500"))

# %% -------------------------- exploitation des objets matches --------------------
import re

# les parenthèses sont des parenthèses capturantes
pattern = "([013456789][0-9]{4}|2[0-9AB][0-9]{3})"
m = re.match(pattern=pattern, string="2A300 est mon zipcode")
if m:
  # notion de groupes de capture: trouver un sous pattern dans le pattern détecté
  # le groupe 0 est la valeur complète
  # à partir du group 1 on a les parenthèses de catpure
  print(f"position: {m.span()}", f"groupes: {m.groups()}", f"valeur exacte: {m.group(0)}")


# astuce python : l'opérateur walrus (:= morse)
# m = ... est une instruction mais pas une EXPRESSION 
# avec le morse, m := ... devient l'expression m elle même
if m := re.match(pattern=pattern, string="2A300 est mon zipcode"):
  val = m.group(0)


# %%  --------------- méthode search ------------------------
###### chercher le pattern de 1ère occurence dans la cible
import re

pattern = "([013456789][0-9]{4}|2[0-9AB][0-9]{3})"
print("trouver le pattern dans la cible", 
      re.search(pattern=pattern, string="mon zipcode est 44500")
)
print("trouver la 1ère occurence du pattern dans la cible", 
      re.search(pattern=pattern, string="mon zipcode est 44500 non 75013")
)

# %% ------------------ la méthode findall ----------------------
####### chercher tous le match d'un pattern dans la cible
import re

pattern = "([013456789][0-9]{4}|2[0-9AB][0-9]{3})"
print("trouver toutes les occurences du pattern dans la cible", 
      re.findall(pattern=pattern, string="mon zipcode est 44500 non 75013")
)
# avec objet Match
for m in re.finditer(pattern=pattern, string="mon zipcode est 44500 non 75013"):
  print(m)

# %%  ------------------- méthode sub --------------------------
####### sub(): search & replace du pattern
import re

pattern = "([013456789][0-9]{4}|2[0-9AB][0-9]{3})"
re.sub(pattern=pattern, repl="********", string="mon zipcode est 44500 non 75013")


# %% --------------- backrefs + raw-string ---------------
import re
# r'' - désactive l'echappement du \ surnuméraire

pattern = r"([a-zA-Z0-9_]+)@(([a-zA-Z0-9_]+\.)+[a-z]{2,})"
re.sub(pattern, r"\2@\1","user@ndd.com")

# %%
