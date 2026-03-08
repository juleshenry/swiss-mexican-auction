#!/bin/bash

# Simple script to mock getting Kaggle eBay data
# We'll download a sample auction dataset from UCI or use a public CSV
curl -s "https://raw.githubusercontent.com/juliencohen/Ebay-Auction-Data/master/auction.csv" > ebay_real_data.csv
echo "Downloaded sample real eBay auction data"
head -n 5 ebay_real_data.csv
