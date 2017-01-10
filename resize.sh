for f in *.jpg;  do   convert $f -resize '640' "small-$f";  done
