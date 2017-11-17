set -e

rm -rf *dat *json *nml LEMS* x86_64 *mod *hoc

echo
echo "**** Running Example 1 ****"
python Example1.py

echo
echo "**** Running Example 2 ****"
python Example2.py

echo
echo "**** Running Example 3 ****"
python Example3.py


jnml -validate *nml

jnml LEMS_SimExample3.xml -nogui

echo
echo "** All generated and tested! **"