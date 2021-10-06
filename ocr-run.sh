for N in {1..17}; do
pushd "$N"
~/git/MIDA-scene-detection/ocr-conversion.sh "data/en$N.mp4" 20211005-1-en eng 0.8 0.2
popd
done

parallel echo ::: {2..17}
parallel -j 3 'pushd "{}"; ~/git/MIDA-scene-detection/ocr-conversion.sh "data/en{}.mp4" 20211005-2-en eng 0.8 0.2 852x480 30; popd' ::: {2..17}

for N in {2..17}; do
pushd "$N"
~/git/MIDA-scene-detection/ocr-conversion.sh "data/en$N.mp4" 20210930-1-en
popd
done
ffplay -ss 350000ms -vf "crop=in_w:in_h*0.2:0:in_h*0.8,scale=w=iw/2:h=ih/2" -i 1/data/en1.mp4