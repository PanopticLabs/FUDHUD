# Instructions

Download the TrendViz folder. 

In terminal, navigate to the TrendViz directory. 

Create a viz by running trendviz.py with two arguments:

   1) timescale (e.g. day, week, month, quarter, year)
   2) coin (e.g. bitcoin, ethereum, monero, bitcoin-cash)


For example, to get a viz of Bitcoin over the last year, type the following: 

      python trendviz.py year bitcoin


# Requirements

pip install pandas

pip install plotly


# Troubleshooting

I only tested this on a Linux machine, so there may be unforseen issues on other devices. You may have to change the filepaths to work for your system, e.g. change '/' to '\'
