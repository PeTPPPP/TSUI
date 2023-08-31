#!/bin/bash 

for dfs in resource/*.7z
do
if [[ "$OSTYPE" == "darwin"* ]]; then
 7zz x -y $dfs -oresource/
else
  7z x -y $dfs -oresource/
fi
done

