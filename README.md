#Traffic stats server for AX88U

snmpd crashes the Asus AX88U, and mini_snmpd as has been suggested in the forums as an alternative, does not appear to support 64-bit counters.

I created this to get around all that.  It's a simple Flask application that will read interface counters from /sys and return them in an MRTG compatible format.

To install it, after enabling custom scripts, enabling entware, installing python3, python3-pip and git, I'd suggest the following -

`cd /jffs
git clone https://github.com/hyacin75/ax88u_traffic_stats_server`

then run the following for a one-time run, and add it to your services-start file in /jffs/scripts -

`gunicorn --bind 0.0.0.0:5000 --chdir /jffs/ax88u_traffic_stats_server wsgi:app --daemon`


It will run on port 5000 on the router, and does not appear to be accessible via the WAN.

I'm sure it's not the most secure or well written thing in the world, but it does the job!


On the MRTG end, you have to install curl and html2text, and then set targets like so -

`Target[192.168.0.1_8]: `curl -s http://192.168.0.1:5000/bond0 | sed -e s/\"//g | html2text``


That's it!  Then you get graphs with support for throughput higher than what 32-bit counters support -

![Sample Graph](/graph.jpg)
