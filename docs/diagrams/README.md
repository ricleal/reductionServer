# Diagrams

Folder to store diagrams (e.g. UML).

UML diagrams can be generated from source running:

```
cd /home/leal/git/reductionServer/docs/diagrams

pyreverse -o pdf -p Pyreverse -f ALL `find ../../src/ -iname '*.py' -maxdepth 10 -print`
#or
pyreverse -o pdf -p Pyreverse -f ALL -S -A `find ../../src/ -iname '*.py' -maxdepth 10 -print`

```
