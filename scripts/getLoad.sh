
#!/usr/bin/env bash
#
# <xbar.title>Academy CPU</xbar.title>
# <xbar.version>v0.1.0</xbar.version>
# <xbar.author>Brad Miller</xbar.author>
# <xbar.author.github>bnmnetp</xbar.author.github>
# <xbar.desc>Continuously checks load on academy workers</xbar.desc>
# <xbar.dependencies>Bash</xbar.dependencies>
# <swiftbar.schedule>00,05,10,15,20,25,30,35,40,45,50,55 * * * *</swiftbar.schedule>
# 
# Academy Load
#
# Continuously checks if hosts are available for ssh connection on port 22

head="Academy CPU Average"
body=""
errors=0
for i in {1..5}; do
  host=server$i.runestoneacademy.org
  load=`ssh $host ps -axo 'pcpu'| awk '{s+=$1} END {print s "  " s/4}'`
  body="$body\n$host\t$load" 
done
  host=db.runestoneacademy.org
  load=`ssh $host ps -axo 'pcpu'| awk '{s+=$1} END {print s "  " s/4}'`
  body="$body\n$host\t\t$load" 
  host=balance.runestoneacademy.org
  load=`ssh root@$host ps -axo 'pcpu'| awk '{s+=$1} END {print s "  " s/2}'`
  body="$body\n$host\t$load" 

echo -n "$head"
echo -e "\n---"
echo -e "$body"
