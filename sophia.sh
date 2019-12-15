EXT='txt'
START=1997
END=2020

for (( i=$START; i<$END; i++ )); do
    YEAR=$i
    cp speech_texts/$EXT/$YEAR/* scraped_data/$EXT/
    echo "cp speech_texts/$EXT/$YEAR/* scraped_data/$EXT/"
done
