#!/bin/bash

if [ $# -lt 6 ]; then
  echo "Example: sh Bulkdbf2mysql.sh <directory_where_files_are> <host> <database> <password> <user> <table_prefix>"
  echo "Example: sh Bulkdbf2mysql.sh /home/german/Documents/ localhost escuela root root dbf"
  exit
fi

ast="*"
dir=$1
host=$2
database=$3
password=$4
user=$5
table_prefix=$6
underscore="_"

for file in $dir$ast
  do
    if [ -f "$file" ];then
      var=$(echo $file | awk -F"$dir$ast" '{print $1,$2}')   
      set -- $var
      file_name=$1
      var=$(echo $file_name | awk -F".DBF" '{print $1,$2}')   
      set -- $var
      uppercase=$1
      var=$(echo $uppercase | awk -F".dbf" '{print $1,$2}')   
      set -- $var
      table_name=$(echo $1 | tr '[:upper:]' '[:lower:]')
      table=$table_prefix$underscore$table_name
      dbf2mysql -h "$host" -d "$database" -t "$table" -c -vv -P "$password" -U "$user" "$file"
    fi
  done