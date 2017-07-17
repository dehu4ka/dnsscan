2.out will be output of:

  ``zmap -M udp -p 53 -i ens192 --probe-args=file:dns_53_queryAwww.google.com.pkt 88.0.0.0/8 -f  saddr,sport,dport -r 100000``

11.py scans 100k IP in 92 seconds. it will be 2.8 days to scan all
