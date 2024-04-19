# SLT2024 LRDWWS Challenge Baseline

## Introduction

This repository is the baseline code for the LRDWWS (Low-Resource Dysarthria Wake-up Word Spotting) Challenge.

The code in this repository is based on the wake-up spotting toolkit WEKWS(https://github.com/wenet-e2e/wekws)

## Data Preparation

Before running this baseline, you should have downloaded and unzipped the dataset for this challenge, whose folder structure is as follows:

```
lrdwws
├── dev
│   ├── Intelligibility.xlsx
│   ├── README.txt
│   ├── enrollment
│   │   ├── transcript
│   │   └── wav
│   └── eval
│       ├── transcript
│       └── wav
└── train
    ├── Control
    │   ├── transcript
    │   └── wav
    ├── Intelligibility.xlsx
    ├── README.txt
    └── Uncontrol
        ├── transcript
        └── wav
```

### Notice

We have released the latest data of the training and development sets and fixed the issue with incorrect information that was reported by some teams. We strongly recommend you to get them from the download links in the email and replace all audio and labels from the previously downloaded training and development sets.

## Environment Setup

```
# create environment
conda create -n lrdwws python=3.8 -y
conda activate lrdwws

# install pytorch torchvision and torchaudio
conda install pytorch=1.10.0 torchaudio=0.10.0 cudatoolkit=11.1 -c pytorch -c conda-forge

# install other dependence
pip install -r requirements.txt
```

## Baseline

```
cd examples/lrd/s0
```

The baseline system consists of three stages of training:

1. Training a Speaker-Independent Control KWS model (SIC) from scratch using Control data in the train set.

   ```
   bash run_control.sh --stage 0 --stop_stage 3
   ```

2. Fine-tuning the SIC model with Uncontrol data in the train set to obtain a Speaker-Independent Dysarthria KWS model (SID).

   ```
   bash run_uncontrol.sh --stage 0 --stop_stage 3
   ```

3. Fine-tuning the SID model with enrollment data in the dev set to obtain Speaker-Dependent Dysarthria KWS systems (SDD) for each individual. The final wake-up performance is evaluated on the corresponding individual's eval set.

   ```
   bash run_enrollment.sh --stage 0 --stop_stage 3
   ```

### Results of dev set

| Model      | Test set        | Intelligibility | FAR    | FRR   | Score  |
| ---------- | --------------- | --------------- | ------ | ----- | ------ |
| SDD_DF0016 | dev/eval/DF0016 | 93.73           | 0.0534 | 0.05  | 0.1034 |
| SDD_DM0005 | dev/eval/DM0005 | 85.78           | 0.0193 | 0.125 | 0.1443 |
| SDD_DF0015 | dev/eval/DF0015 | 68.44           | 0.035  | 0.075 | 0.11   |
| SDD_DM0019 | dev/eval/DM0019 | 47.95           | 0.0688 | 0.175 | 0.2438 |

## Notice

- The baseline code we provided will output FAR and FRR under different thresholds during the test phase (stage 3). However, in the test phase of the challenge, participants are only allowed to submit a final wake-up result for each speech clip. Also, during the test phase, we will not provide annotations for eval in the test set. This means that participants need to think about how to choose the appropriate threshold.
- Participants may use all methods to improve the final results, including the use of pre-trained models and other open-source datasets, provided that this is explicitly stated in the final paper or system report submitted.
- If the scores of the two teams on the test data set are the same, the system with lower computation complexity will be judged as the superior one. In this case, participants will be asked to provide proof of computational complexity. Therefore, participants are strongly advised to retain their code for verification purposes.

## License

It is noted that the code can only be used for comparative or benchmarking purposes.  Users can only use code supplied under a License for non-commercial purposes.

## Contact

Please contact e-mail [lrdwws_challenge@aishelldata.com](mailto:lrdwws_challenge@aishelldata.com) if you have any queries.