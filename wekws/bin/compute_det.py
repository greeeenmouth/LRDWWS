# Copyright (c) 2021 Binbin Zhang(binbzha@qq.com)
#               2022 Shaoqing Yu(954793264@qq.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os


def load_label_and_score(keyword, label_file, score_file):
    # score_table: {uttid: [keywordlist]}
    score_table = {}
    with open(score_file, 'r', encoding='utf8') as fin:
        for line in fin:
            arr = line.strip().split()
            key = arr[0]
            current_keyword = arr[1]
            str_list = arr[2:]
            if int(current_keyword) == keyword:
                scores = list(map(float, str_list))
                if key not in score_table:
                    score_table.update({key: scores})
    keyword_table = {}
    filler_table = {}
    filler_duration = 0.0
    with open(label_file, 'r', encoding='utf8') as fin:
        for line in fin:
            obj = json.loads(line.strip())
            assert 'key' in obj
            assert 'txt' in obj
            assert 'duration' in obj
            key = obj['key']
            index = obj['txt']
            duration = obj['duration']
            assert key in score_table
            if index == keyword:
                keyword_table[key] = score_table[key]
            else:
                filler_table[key] = score_table[key]
                filler_duration += duration
    return keyword_table, filler_table, filler_duration


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='compute det curve')
    parser.add_argument('--test_data', required=True, help='label file')
    parser.add_argument('--keyword', type=int, default=0, help='keyword label')
    parser.add_argument('--score_file', required=True, help='score file')
    parser.add_argument('--step', type=float, default=0.01,
                        help='threshold step')
    parser.add_argument('--window_shift', type=int, default=50,
                        help='window_shift is used to skip the frames after triggered')
    parser.add_argument('--stats_dir',
                        required=False,
                        default=None,
                        help='false reject/alarm stats dir, '
                             'default in score_file')
    args = parser.parse_args()
    window_shift = args.window_shift

    stats = {}
    threshold = 0.0
    while threshold <= 1.0:
        stats[threshold] = [0, 0]
        threshold += args.step

    for k in range(int(args.keyword)):
        keyword_table, filler_table, filler_duration = load_label_and_score(
            k, args.test_data, args.score_file)
        print('Filler total duration Hours: {}'.format(filler_duration / 3600.0))

        stats_file = os.path.join(args.stats_dir, 'stats.'+str(k)+'.txt')
        with open(stats_file, 'w', encoding='utf8') as fout:
            keyword_index = k
            threshold = 0.0

            while threshold <= 1.0:
                num_false_reject = 0
                # transverse the all keyword_table
                for key, score_list in keyword_table.items():
                    # computer positive test sample, use the max score of list.
                    score = max(score_list)
                    if float(score) < threshold:
                        num_false_reject += 1
                num_false_alarm = 0
                # transverse the all filler_table
                for key, score_list in filler_table.items():
                    i = 0
                    while i < len(score_list):
                        if score_list[i] >= threshold:
                            num_false_alarm += 1
                            i += window_shift
                        else:
                            i += 1
                if len(keyword_table) != 0:
                    false_reject_rate = num_false_reject / len(keyword_table)

                false_alarm_rate = num_false_alarm / len(filler_table)
                stats[threshold][0] += false_alarm_rate
                stats[threshold][1] += false_reject_rate
                fout.write('{:.6f} {:.6f} {:.6f}\n'.format(threshold,
                                                           false_alarm_rate,
                                                           false_reject_rate))
                threshold += args.step

    stats_filename = os.path.join(args.stats_dir, 'stats_all.txt')
    print(stats_filename)
    with open(stats_filename, 'w', encoding='utf8') as fout:
        threshold = 0.0
        while threshold <= 1.0:
            far = stats[threshold][0] / int(args.keyword)
            frr = stats[threshold][1] / int(args.keyword)
            fout.write('{:.3f} {:.6f} {:.6f} {:.6f}\n'.format(
                threshold, far, frr, far+frr))
            threshold += args.step