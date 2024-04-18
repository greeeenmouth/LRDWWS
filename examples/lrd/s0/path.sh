export PATH=$PWD:$PATH

# NOTE(kan-bayashi): Use UTF-8 in Python to avoid UnicodeDecodeError when LC_ALL=C
export PYTHONIOENCODING=UTF-8
export PYTHONPATH=../../../:$PYTHONPATH

# import anaconda environment
export PATH=/home4/intern/minggao5/anaconda3/envs/wenet/bin:${PATH}

# import gcc environment
export PATH=/opt/compiler/gcc-7.3.0-os7.2/bin:$PATH
export LD_LIBRARY_PATH=/opt/compiler/gcc-7.3.0-os7.2/lib64:$LD_LIBRARY_PATH

# import perl environment
export PATH=/home3/cv1/hangchen2/localperl/bin:${PATH}
