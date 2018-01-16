#!/bin/bash
/usr/bin/expect <<-EOF
spawn ssh  192.168.40.188 
expect {
"*yes/no" { send "yes\r"; exp_continue }
"*password:" { send "bjjs64130088\r" }
}
expect "*#"
send "free\r"
expect "*#"
send "w\r"
expect "*#"
send "exit\r"
interact
expect eof
EOF
