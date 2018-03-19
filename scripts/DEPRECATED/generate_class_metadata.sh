#
# generate_class_metadata.sh
#
# author = 'James Ryan'
# copyright = 'Copyright 2018'
# credits = ['James Ryan']
# license = 'MIT'
# version = '0.1'
# maintainer = 'James Ryan' 
# email = 'octaexon@gmail.com'
# status = 'Development'
#
# converts class metadata downloaded in README.txt to csv format
#
# a typical line of interest has the form:
#
# 12 = speed limit 30 (prohibitory)
# <id> = <description> (<category>)
#
# note the special character  at the end, which is a representation
# of the carriage return (file probably written on a windows system)


script_dir="$PWD/$(dirname "$0")"
src="$script_dir/metadata/README.txt"
dst="$script_dir/metadata/class_metadata.csv"

# scan command line options
for i in "$@"; do
    case $i in
        -s=*|--source=*)
            src="${i#*=}"
            shift
            ;;
        -d=*|--destination=*)
            dst="${i#*=}"
            shift
            ;;
        -h|--help)
            echo "generate_class_metadata.sh: greps class id descriptions from README.txt"
            echo "options:    [-s=readme_file] [--source=readme_file]"
            echo "            [-d=destination_file] [--destination=destination_file]"
            echo "            [-h] [--help]"
            exit
            ;;
        *)
            # unknown option
            echo unknown option $i
            exit
            ;;
    esac
done

# check for existence of source file
if [ ! -f $src ]; then
    echo $src does not exist
    exit
fi

# ensure existence of destination directory
if [ ! -d $(dirname $dst) ]; then
    mkdir -p $(dirname $dst)
fi

# check for existence of destination file and overwrite permission
overwrite_flag=""

if [ -f $dst ]; then
    while [[ ! $overwrite_flag =~ ^[yn]$ ]]; do
        echo -n "$dst exists; overwrite (y/n): "
        read overwrite_flag
    done

    if [[ $overwrite_flag =~ ^y$ ]]; then
        rm $dst
    else
        exit
    fi
fi


# column names for csv
echo class_id,category,description > $dst


while read line; do
    # filter out lines that do not begin with a 1-2 digit etc
    line=$(echo $line | grep '^\d\{1,2\}\ =')

    # extract <id> and the rest of the metadata
    if [ ! "$line" = "" ]; then
        read class_id features << EXTRACT
            $(echo $line | awk 'BEGIN { FS="="; OFS=" " } { print $1,$2 }')
EXTRACT

        # split features into <description> and <category>
        # strip out brackets
        description=${features%\ \(*}
        description=${description//[\(\)]}
        category=${features##*\ }
        category=${category//[\(\)]}

        # append to file
        echo $class_id,$category,\"$description\" >> $dst
    fi
done < $src # source README.txt
