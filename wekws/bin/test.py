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
    parser = argparse.ArgumentParser(description='test with fixed threshold')
    parser.add_argument('--keyword', type=int, default=0, help='keyword label')
    parser.add_argument('--score_file', required=True, help='score file')
    parser.add_argument('--threshold', type=float, default=0.5,
                        help='threshold step')
    parser.add_argument('--res_dir',
                        required=False,
                        default=None,
                        help='false reject/alarm stats dir, '
                             'default in score_file')
    args = parser.parse_args()
    threshold = args.threshold
    res={}

    with open(args.score_file, 'r', encoding='utf8') as fin:
        max_score = threshold
        max_score_keyword = -1
        for line in fin:
            arr = line.strip().split()
            key = arr[0]
            current_keyword = int(arr[1])
            score_list = arr[2:]
            score = float(max(score_list))
            if score >= max_score:
                max_score = score
                max_score_keyword = current_keyword
            if current_keyword == int(args.keyword) - 1:
                res[arr[0]] = max_score_keyword
                max_score = threshold
                max_score_keyword = -1

    if not os.path.exists(args.res_dir):
        os.makedirs(args.res_dir)
    res_file = os.path.join(args.res_dir, 'res.txt')

    with open(res_file, 'w', encoding='utf8') as fout:
        for k,v in res.items():
            fout.write('{} {}\n'.format(k,v))
