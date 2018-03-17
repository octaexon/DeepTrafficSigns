#
# generate_image_metadata.sh
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

#script_dir="$PWD/$(dirname "$0")"
script_dir="."
src_images_dir="$script_dir/images_jpg"
src_raw_metadata="$script_dir/metadata/raw_metadata.txt"
dst_metadata="$script_dir/metadata/image_metadata.csv"

# scan command line options
for i in "$@"; do
    case $i in
        -s=*|--source=*)
            src_images_dir="${i#*=}"
            shift
            ;;
        -d=*|--destination=*)
            dst_metadata="${i#*=}"
            shift
            ;;
        -r=*|--raw=*)
            src_raw_metadata="${i#*=}"
            shift
            ;;
        -h|--help)
            echo "generate_image_metadata.sh: grabs specs from raw_metadata.txt and related jpeg images to produce csv"
            echo "options:    [-s=image_directory] [--source=image_directory]"
            echo "            [-r=raw_metadata_file] [--raw=raw_metadata_file]"
            echo "            [-d=destination_file] [--destination=destination_file]"
            echo "            [-h] [--help]"
            echo "notes: raw_metadata.txt has a specific line format:"
            echo "       <filename>;<x_min>;<y_max>;<x_max>;<y_min>;<class_id>"
            exit
            ;;
        *)
            # unknown option
            echo unknown option $i
            exit
            ;;
    esac
done


# validate existence of sources
if [ ! -f $src_raw_metadata ]; then
    echo $src_raw_metadata does not exist
    exit
fi

if [ ! -d $src_images_dir ]; then
    echo $src_images_dir does not exist
    exit
fi

# ensure existence of destinations
if [ ! -d $(dirname $dst_metadata) ]; then
    mkdir -p $(dirname $dst_metadata)
fi



overwrite_flag=""

if [ -f $dst_metadata ]; then # check how to deal with output
    while [[ ! $overwrite_flag =~ ^[oae]$ ]]; do
        echo -n "$dst_metadata exists; overwrite/append/exit (o/a/e): "
        read overwrite_flag
    done

    if [[ $overwrite_flag =~ ^o$ ]]; then
        rm $dst_metadata
    fi
fi

if [[ $overwrite_flag =~ ^e$ ]]; then # chose to exit
    exit
elif [[ $overwrite_flag =~ ^o?$ ]]; then # either file does not exist or chose to overwrite
    echo filename,width,height,xmin,ymin,xmax,ymax,class_id > $dst_metadata
fi



while read line; do
    # extract various fields into variables from each line
    read image_file xmin ymax xmax ymin class_id << EXTRACT
    $(echo $line | awk 'BEGIN { FS=";"; OFS=" " } { print $1,$2,$3,$4,$5,$6 }')
EXTRACT
    # path of image file and change its extension
    image_filepath="$src_images_dir/${image_file%.*}.jpg"
    # extract width and height
    read image_width image_height << EXTRACT
    $(sips -g pixelWidth -g pixelHeight "$image_filepath" | grep pixel | awk '{ print $2 }' | tr '\n' ' ')
EXTRACT

    # append current parameters to annotations file
    echo $image_filepath,$image_width,$image_height,$xmin,$ymin,$xmax,$ymax,$class_id >> $dst_metadata
    echo -n '.'
done < "$src_raw_metadata"
