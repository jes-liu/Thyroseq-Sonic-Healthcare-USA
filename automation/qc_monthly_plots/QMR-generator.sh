# shell script to call R script and run it with varying variable names

filename=$(date -d "`date +%Y%m01` -1 month" '+%b%Y')
start_date_range=$(date -d "`date +%Y%m01` -1 month" '+%m-%d-%Y')
end_date_range=$(date '+%m-01-%Y')