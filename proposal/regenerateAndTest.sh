set -e

rm -rf *dat *json *nml

echo
echo "**** Running Example 1 ****"
python Example1.py

echo
echo "**** Running Example 2 ****"
python Example2.py

echo
echo "**** Running Example 3 ****"
python Example3.py


jnml LEMS_Example3.xml -nogui