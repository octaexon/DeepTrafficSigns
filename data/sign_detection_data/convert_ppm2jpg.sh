#
# convert_ppm2jpg.sh
#
# author = 'James Ryan'
# copyright = 'Copyright 2018'
# credits = ['James Ryan']
# license = 'MIT'
# version = '0.1'
# maintainer = 'James Ryan' 
# email = 'octaexon@gmail.com'
# status = 'Development'


# src and dst may be overridden from the command line
script_dir="$PWD/$(dirname "$0")"
src="$script_dir/images_ppm"
dst="$script_dir/images_jpg"

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
            echo "convert_ppm2jpg.sh: transforms ppm to jpg"
            echo "options: [-s=source_directory] [--source=source_directory]"
            echo "         [-d=destination_directory] [--destination=destination_directory]"
            echo "         [-h] [--help]"
            exit
            ;;
        *)
            # unknown option
            echo unknown option $i
            exit
            ;;
    esac
done



# validate source location and ensure destination
if [ ! -d "$src" ]; then
    echo $src does not exist
    exit
fi

if [ ! -d "$dst" ]; then
    mkdir -p $dst
fi


overwrite_flag=n

for i in $src/*.ppm; do 
    # target file to be create during transformation
    target="$dst/$(basename ${i%.*}).jpg"
    convert="sips -s format jpeg $i --out $target"


    if [ -f $target ]; then # target file exists so request guidance on overwriting
        if [[ $overwrite_flag =~ ^[yn]$ ]]; then
            echo -n "$target already exists; overwrite (y/n), overwrite all/none (Y/N): "
            read overwrite_flag

            while [[ ! $overwrite_flag =~ ^[ynYN]$ ]]; do
                echo -n "Invalid key, enter one of (y/n/Y/N): "
                read overwrite_flag
            done
        fi

        if [[ $overwrite_flag =~ ^[yY]$ ]]; then
            eval $convert
        fi
    else # target file does not exist yet
        eval $convert
    fi
done
