#! /bin/bash
# a users file contains a username list (one per line): istXXXXXX
# gcc -o mkpass mkpass.c
# gcc -o combine combine.c
# N=`wc -l < users` # count the number of users
# ./mkpass N 12 # create N passwds with 12 chars each
# ./combine users pass out # merge usernames with passwords
# ./doit.sh < out # use this file to create directories and permissions
read a b
while [ $? -eq 0 ]; do
	mkdir $a
	sed -e "s/XXX/$a/" < htaccess > $a/.htaccess
	htpasswd -cb $a/.htpasswd $a $b
	chmod 644 $a/.htaccess $a/.htpasswd
	read a b
done
