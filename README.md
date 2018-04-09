# Weblogic-Weakpassword-Scnner
pip install requests

You can use masscan to scan ip range with CIDR format<br>
<pre>
masscan -iL ip.txt -oL 7001.txt -p 7001 --max-rate=80000<br>
awk '{print $4,$3}' 7001.txt|sed 's/ /:/g' >> scanned.txt<br>
</pre>
For more information about masscan:https://github.com/robertdavidgraham/masscan

About new version:Will use first 5 passwords to test all url in once, 30 min later,use next 5 passwords to do it again.More efficient than previous

1.python spider.py scanned.txt

2.python brute.py

Also can use with https://github.com/dc3l1ne/Weblogic_Automatical_Attacker to deploy war package automatically
