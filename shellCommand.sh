#!/bin/bash
while :
do
cd /c/Users/CoCo\ Lab/Desktop/EmoDatabase
startTime=`date +%s`
for item in "twitter finagle" "openstf stf" "marko-js marko" "recharts recharts" "immutable-js immutable-js" "Moya Moya" "segmentio nightmare" "sqlitebrowser sqlitebrowser" "tesseract-ocr tesseract" "pingcap tidb" "HelloZeroNet ZeroNet" "ncw rclone" "aframevr aframe" "Alamofire Alamofire" "facebook fresco" "google guava" "facebook jest" "facebook react" "google ExoPlayer" "tensorflow tensorflow"
	do
		set -- $item		
		py -3 mainFile.py $1 $2
		cd emoTxt
		rm *.csv
		cd ..
		cp *.csv emoTxt
		cd emoTxt
		for file in *.csv
			do
				name=${file%%[.]*}
				sh classify.sh -i $name.csv -d sc -p -e anger
				sh classify.sh -i $name.csv -d sc -p -e fear
				sh classify.sh -i $name.csv -d sc -p -e joy
				sh classify.sh -i $name.csv -d sc -p -e sadness
				echo "Emotion intesity calculation succeed...."
				cd "classification_$name""_anger"
				mv predictions_anger.csv "$name""_prediction_anger.csv"
				mv "$name""_prediction_anger.csv" /c/Users/CoCo\ Lab/Desktop/EmoDatabase
				cd ..
				rm -rf "classification_$name""_anger"
				cd "classification_$name""_fear"
				mv predictions_fear.csv "$name""_prediction_fear.csv"
				mv "$name""_prediction_fear.csv" /c/Users/CoCo\ Lab/Desktop/EmoDatabase
				cd ..
				rm -rf "classification_$name""_fear"
				cd "classification_$name""_joy"
				mv predictions_joy.csv "$name""_prediction_joy.csv"
				mv "$name""_prediction_joy.csv" /c/Users/CoCo\ Lab/Desktop/EmoDatabase
				cd ..
				rm -rf "classification_$name""_joy"
				cd "classification_$name""_sadness"
				mv predictions_sadness.csv "$name""_prediction_sadness.csv"
				mv "$name""_prediction_sadness.csv" /c/Users/CoCo\ Lab/Desktop/EmoDatabase
				cd ..
				rm -rf "classification_$name""_sadness"
				cd /c/Users/CoCo\ Lab/Desktop/EmoDatabase
				echo "Intensity files are transfered to EmoD Directory...."
				py -3 nrc.py $name $2
				echo "Insertion in InfluxDB Succeed...."
				rm "$name""_prediction_fear.csv"
				rm "$name""_prediction_anger.csv"
				rm "$name""_prediction_joy.csv"
				rm "$name""_prediction_sadness.csv"
				rm $name.csv
				rm "$name""_data.txt"
				cd emoTxt
				rm $name.csv
				echo "Completion of EmoD calculation for a single Contributor....!!!"	
			done
		echo "Next Project Computation....!!!"	
	done
echo "Next Iteration....!!!"
endTime=`date +%s`
let diffTime=(endTime-startTime)
let sleepTime=86400-diffTime
echo "Sleeping for one day...."
sleep sleepTime
cd /c/Users/CoCo\ Lab/Desktop/EmoDatabase
rm *.txt
rm *.csv
done
