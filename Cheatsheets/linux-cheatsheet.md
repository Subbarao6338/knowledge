# Linux Commands Cheatsheet

## Navigation & File Basics

```bash
pwd                          # print working directory
ls; ls -la; ls -lh              # list; long+hidden; human-readable sizes
cd /path/to/dir
cd ~; cd -                        # home; previous directory

cp file.txt dest/
cp -r dir/ dest/                    # recursive copy
mv file.txt newname.txt
rm file.txt
rm -rf dir/                            # force recursive delete (careful!)

mkdir mydir
mkdir -p a/b/c                # create nested dirs as needed
rmdir mydir                      # remove empty dir

touch file.txt                     # create empty file / update timestamp
find . -name "*.log"                  # find files by name
find . -type f -mtime -7                 # files modified in last 7 days
find . -type f -size +100M                  # files over 100MB
find . -name "*.tmp" -delete

ln -s /path/to/target linkname          # symbolic link
ln /path/to/target hardlink

file myfile                    # detect file type
stat file.txt                     # detailed file metadata
realpath file.txt                    # absolute path
basename /path/to/file.txt              # -> file.txt
dirname /path/to/file.txt                  # -> /path/to
```

## Viewing & Editing Files

```bash
cat file.txt
cat -n file.txt                # with line numbers
less file.txt                     # paginated view (q to quit, / to search)
more file.txt
head file.txt                        # first 10 lines
head -n 20 file.txt
tail file.txt                           # last 10 lines
tail -n 50 file.txt
tail -f file.txt                           # follow (live updates) — great for logs
tail -f file.txt | grep ERROR

wc file.txt                    # lines, words, bytes
wc -l file.txt                    # line count only

nano file.txt                       # simple terminal editor
vim file.txt                           # modal editor (i=insert, Esc, :wq=save+quit, :q!=quit no save)
```

## Text Processing

```bash
grep "pattern" file.txt
grep -i "pattern" file.txt              # case-insensitive
grep -r "pattern" dir/                     # recursive
grep -v "pattern" file.txt                    # invert match (lines NOT matching)
grep -c "pattern" file.txt                       # count matches
grep -n "pattern" file.txt                          # show line numbers
grep -E "pattern1|pattern2" file.txt                   # extended regex (or -P for PCRE)
grep -A 3 -B 3 "pattern" file.txt                          # 3 lines after/before match

sed 's/old/new/' file.txt                   # replace first match per line
sed 's/old/new/g' file.txt                     # replace all matches
sed -i 's/old/new/g' file.txt                     # edit in place
sed -n '5,10p' file.txt                              # print lines 5-10
sed '/pattern/d' file.txt                               # delete matching lines

awk '{print $1}' file.txt                    # print first column (whitespace-delimited)
awk -F',' '{print $2}' file.txt                 # custom delimiter
awk '{sum += $1} END {print sum}' file.txt         # sum a column
awk '$3 > 100 {print $0}' file.txt                    # filter rows by condition
awk 'NR==5' file.txt                                     # print specific line number

cut -d',' -f1,3 file.csv                    # extract columns 1 and 3
cut -c1-10 file.txt                             # extract characters 1-10

sort file.txt
sort -n file.txt                    # numeric sort
sort -r file.txt                       # reverse
sort -k2 file.txt                         # sort by 2nd field
sort -u file.txt                             # sort + dedupe
uniq file.txt                                    # dedupe adjacent lines (sort first!)
uniq -c file.txt                                    # count occurrences

tr 'a-z' 'A-Z' < file.txt         # translate characters
tr -d '\n' < file.txt                # delete newlines
tr -s ' '                               # squeeze repeated spaces

diff file1.txt file2.txt
diff -u file1.txt file2.txt              # unified diff format
comm file1.txt file2.txt                    # compare sorted files line by line

xargs                          # build/execute commands from stdin
find . -name "*.log" | xargs rm
cat urls.txt | xargs -n1 curl -O
find . -name "*.txt" -print0 | xargs -0 grep "pattern"    # handle filenames with spaces
```

## Permissions & Ownership

```bash
chmod 755 file.sh                # rwxr-xr-x
chmod +x script.sh                  # add execute permission
chmod -R 644 dir/                      # recursive
chmod u+w,g-w,o=r file.txt                # symbolic mode

chown user:group file.txt
chown -R user:group dir/

# Permission digits: 4=read, 2=write, 1=execute (sum them per owner/group/other)
# rwxr-xr-x = 755:  owner=rwx(7), group=r-x(5), other=r-x(5)

umask                    # show default permission mask
umask 022                   # set default mask

sudo command                 # run as root
sudo -u otheruser command       # run as specific user
su - username                     # switch user
```

## Process Management

```bash
ps aux                       # all running processes
ps aux | grep python            # filter by name
top                                # live process viewer
htop                                  # improved live viewer (if installed)

kill <pid>                     # SIGTERM (graceful)
kill -9 <pid>                     # SIGKILL (force)
killall processname                  # kill by name
pkill -f "pattern"                      # kill matching command line

jobs                          # list background jobs in current shell
bg                              # resume a job in background
fg                                # bring job to foreground
command &                            # run in background
nohup command &                         # keep running after terminal closes
disown                                     # detach job from shell

nice -n 10 command             # run with lower priority
renice 10 -p <pid>                # change priority of running process

pgrep processname           # get PIDs matching name
pidof processname              # same, alternate tool
```

## Disk & Filesystem

```bash
df -h                    # disk free, human-readable
du -sh dir/                 # directory size summary
du -sh * | sort -rh            # size of each item in current dir, sorted
du -h --max-depth=1 dir/          # size per subdirectory, one level deep

mount                # list mounted filesystems
mount /dev/sdb1 /mnt/data
umount /mnt/data

lsblk                  # list block devices
fdisk -l                  # partition table info
mkfs.ext4 /dev/sdb1          # format a partition

fsck /dev/sdb1           # check/repair filesystem (unmounted)
```

## Networking

```bash
ip a                     # show network interfaces (modern)
ifconfig                    # legacy equivalent
ip route                       # routing table

ping google.com
ping -c 4 google.com               # 4 packets then stop
curl https://api.example.com
curl -X POST -H "Content-Type: application/json" -d '{"key":"val"}' https://api.example.com
curl -O https://example.com/file.zip           # download, keep filename
curl -I https://example.com                        # headers only
curl -s -o /dev/null -w "%{http_code}" https://example.com   # just the status code

wget https://example.com/file.zip
wget -c https://example.com/file.zip         # resume partial download

netstat -tulpn            # listening ports (legacy)
ss -tulpn                    # listening ports (modern replacement for netstat)
lsof -i :8080                   # what's using a specific port
lsof -i -P -n | grep LISTEN         # all listening processes

nslookup example.com
dig example.com
host example.com

ssh user@host
ssh -i mykey.pem user@host
ssh -L 8080:localhost:80 user@host          # local port forward
scp file.txt user@host:/path/
scp -r dir/ user@host:/path/
rsync -avz ./local/ user@host:/remote/
rsync -avz --delete ./local/ user@host:/remote/    # mirror, delete extras on remote

traceroute example.com
mtr example.com                  # continuous traceroute + ping stats
```

## Compression & Archives

```bash
tar -cvf archive.tar dir/                  # create tar
tar -xvf archive.tar                          # extract tar
tar -czvf archive.tar.gz dir/                    # create gzip-compressed tar
tar -xzvf archive.tar.gz                            # extract gzip tar
tar -tvf archive.tar                                   # list contents without extracting
tar -czvf archive.tar.gz --exclude='*.log' dir/           # exclude patterns

gzip file.txt                # compress (creates file.txt.gz, removes original)
gunzip file.txt.gz              # decompress
zip -r archive.zip dir/
unzip archive.zip
unzip -l archive.zip              # list contents without extracting

7z a archive.7z dir/           # if p7zip installed
```

## System Info

```bash
uname -a                    # kernel/system info
hostname
uptime                          # how long system has been running + load average
whoami
id                                # current user's uid/gid/groups
w                                    # who's logged in and what they're doing

free -h                    # memory usage, human-readable
vmstat 1                      # virtual memory stats, refresh every 1s
lscpu                            # CPU info
nproc                               # number of CPU cores

env                    # list environment variables
echo $PATH
export MY_VAR=value
unset MY_VAR
printenv MY_VAR

history                    # command history
!123                          # re-run history command number 123
!!                                # re-run last command
Ctrl+R                               # reverse search history

which command               # location of an executable
whereis command                # binary/source/man page locations
type command                      # how a command would be interpreted (alias/builtin/binary)
man command                          # manual page
command --help
```

## Users & Groups

```bash
useradd newuser
useradd -m -s /bin/bash newuser        # with home dir + shell
passwd newuser
userdel newuser
userdel -r newuser              # also remove home directory

groupadd mygroup
usermod -aG mygroup newuser        # add user to group (append, don't replace)
groups newuser                        # list a user's groups
gpasswd -d newuser mygroup               # remove user from group

cat /etc/passwd                # list all users
cat /etc/group                    # list all groups
```

## Scripting Essentials (Bash)

```bash
#!/bin/bash
set -e                      # exit immediately on any error
set -u                         # error on unset variables
set -o pipefail                   # fail if any command in a pipeline fails
set -x                                # print each command before running (debug)

VAR="value"
echo "$VAR"
echo "${VAR}_suffix"

if [ "$VAR" == "value" ]; then
    echo "match"
elif [ -z "$VAR" ]; then
    echo "empty"
else
    echo "no match"
fi

# Common test flags: -f (file exists) -d (dir exists) -z (empty string) -n (non-empty) -eq -ne -gt -lt

for f in *.txt; do
    echo "$f"
done

for i in {1..5}; do
    echo "$i"
done

while read -r line; do
    echo "$line"
done < file.txt

function greet() {
    echo "Hello, $1"
}
greet "World"

$(command)                   # command substitution
`command`                        # older command substitution syntax
$?                                    # exit code of last command
$#                                       # number of script arguments
$@                                          # all arguments
$1 $2 ...                                      # positional arguments

trap 'echo "cleanup"; exit' EXIT INT TERM      # run cleanup on exit/interrupt
```

## Cron / Scheduling

```bash
crontab -e                  # edit current user's crontab
crontab -l                     # list current crontab
crontab -r                        # remove crontab

# Format: minute hour day month weekday command
# 0 6 * * *      -> every day at 6:00 AM
# */15 * * * *   -> every 15 minutes
# 0 0 1 * *      -> midnight on the 1st of every month
# 0 9 * * 1-5    -> 9 AM on weekdays

0 6 * * * /home/user/script.sh >> /var/log/script.log 2>&1

systemctl list-timers          # systemd timers (modern cron alternative)
```

## systemd Service Management

```bash
systemctl status myservice
systemctl start myservice
systemctl stop myservice
systemctl restart myservice
systemctl enable myservice          # start on boot
systemctl disable myservice
systemctl daemon-reload                # after editing a unit file

journalctl -u myservice              # logs for a specific service
journalctl -u myservice -f              # follow live
journalctl --since "1 hour ago"
journalctl -p err                          # only error-level and above
```

## Package Management

```bash
# Debian/Ubuntu (apt)
apt update; apt upgrade
apt install package
apt remove package
apt search package
apt list --installed
dpkg -l                          # list installed packages
dpkg -i package.deb

# RHEL/CentOS/Fedora (yum/dnf)
dnf install package
dnf update
dnf remove package
dnf search package
rpm -qa                          # list installed packages
```

## Redirection & Pipes

```bash
command > file.txt              # stdout to file (overwrite)
command >> file.txt                # stdout to file (append)
command 2> error.txt                  # stderr to file
command > out.txt 2>&1                   # both stdout and stderr to same file
command &> out.txt                          # shorthand for the above (bash)
command < input.txt                            # stdin from file
command 2>/dev/null                               # discard stderr

cmd1 | cmd2                    # pipe stdout of cmd1 into stdin of cmd2
cmd1 | tee file.txt | cmd2         # write to file AND pass through to next command
```

## Useful One-Liners

```bash
# Find and kill process using a port
lsof -ti:8080 | xargs kill -9

# Top 10 largest files/dirs in current directory
du -ah . | sort -rh | head -10

# Count lines in all .py files
find . -name "*.py" | xargs wc -l | tail -1

# Watch disk usage live
watch -n 2 df -h

# Search command history for a keyword
history | grep "docker"

# Find and replace across many files
grep -rl "old_string" . | xargs sed -i 's/old_string/new_string/g'

# Monitor a log file for errors in real time
tail -f app.log | grep --line-buffered ERROR

# Check which process is holding a file open
lsof /path/to/file

# Show top memory-consuming processes
ps aux --sort=-%mem | head -10

# Show top CPU-consuming processes
ps aux --sort=-%cpu | head -10
```
