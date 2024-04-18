#!/bin/bash
# Copyright 2021  Binbin Zhang(binbzha@qq.com)

. ./path.sh

stage=$1
stop_stage=$2
num_keywords=10

norm_mean=true
norm_var=true
gpus="2"

checkpoint=/train20/intern/permanent/minggao5/Code/lrdwws/examples/lrd/s0/exp/control/avg_30.pt # your checkpoint dir of Control
config=conf/ds_tcn.yaml
download_dir=/train20/intern/permanent/minggao5/datasets/lrdwws/train # your data dir
data=data_uncontrol
tools=../../../tools
dir=exp/uncontrol

. ../../../tools/parse_options.sh || exit 1;
window_shift=50

# generate "wav.scp"
if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
  echo "Preparing datasets..."
  for folder in train dev test; do
    text_path=$data/$folder/text
    $tools/prepare_data.py $download_dir/Uncontrol/wav ${text_path} $data/$folder/wav.scp
  done
fi

# compute CMVN, generate "data.list" and "wav.dur"
if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
  echo "Compute CMVN and Format datasets"
  ${tools}/compute_cmvn_stats.py --num_workers 16 --train_config $config \
    --in_scp $data/train/wav.scp \
    --out_cmvn $data/train/global_cmvn

  for x in train dev test; do
    ${tools}/wav_to_duration.sh --nj 8 $data/$x/wav.scp $data/$x/wav.dur
    ${tools}/make_list.py $data/$x/wav.scp $data/$x/text \
      $data/$x/wav.dur $data/$x/data.list $data/dict/words.txt
  done
fi

# training
if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
  echo "Start training ..."
  mkdir -p $dir
  cmvn_opts=
  $norm_mean && cmvn_opts="--cmvn_file $data/train/global_cmvn"
  $norm_var && cmvn_opts="$cmvn_opts --norm_var"
  num_gpus=$(echo $gpus | awk -F ',' '{print NF}')
  torchrun --standalone --nnodes=1 --nproc_per_node=$num_gpus \
    ../../../wekws/bin/train.py --gpus $gpus \
      --config $config \
      --train_data $data/train/data.list \
      --cv_data $data/dev/data.list \
      --model_dir $dir \
      --num_workers 8 \
      --num_keywords $num_keywords \
      --min_duration 50 \
      --seed 666 \
      --tensorboard_dir tensorboard/uncontrol \
      $cmvn_opts \
      ${checkpoint:+--checkpoint $checkpoint}
fi

# testing
if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
  echo "Compute FRR/FAR ..."
  average_model=false
  num_average=30
  if $average_model ;then
    score_checkpoint=$dir/avg_${num_average}.pt
  else
    score_checkpoint=$dir/final.pt
  fi
  result_dir=$dir/test_$(basename $score_checkpoint)
  mkdir -p $result_dir

  if $average_model ;then
    python ../../../wekws/bin/average_model.py \
      --dst_model $score_checkpoint \
      --src_path $dir  \
      --num ${num_average} \
      --val_best
  fi

  python ../../../wekws/bin/max_score.py \
    --config $dir/config.yaml \
    --test_data $data/test/data.list \
    --gpu 0 \
    --batch_size 64 \
    --checkpoint $score_checkpoint \
    --score_file $result_dir/score.txt  \
    --num_workers 8

  python ../../../wekws/bin/compute_det.py \
      --keyword 10 \
      --test_data $data/test/data.list \
      --window_shift $window_shift \
      --step 0.001  \
      --score_file $result_dir/score.txt \
      --stats_dir $result_dir
fi