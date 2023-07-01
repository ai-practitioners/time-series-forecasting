1. `pip install kaggle` in terminal
1. from your profile page on kaggle, `Create API`
1. download the json file
1. copy+paste (from download folder) to `~/.kaggle/`
1. change permissions so your user (in windows or WSL or MacOS)  can run the file: `chmod 600 ~/.kaggle/kaggle.json`
1. change to data directory where you want the date to live: `cd data/raw`
1. in terminal: `kaggle competitions download -c m5-forecasting-accuracy`
1. in terminal: `unzip m5-forecasting-accuracy.zip`
1. in terminal: `python src/convert_csv.py` to import 3 csv files we're going to use for EDA and training into a single database file `forecasting.db` in same location as CSVs. Just to practice our 'SQL-fu'. If your _data path_ is different than `data/raw`, edit the code accordingly.

If just want to use CSV files, above step (9) can be skipped.
