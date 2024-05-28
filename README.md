<img width="592" alt="image" src="https://github.com/greeeenmouth/LRDWWS/assets/31959671/6eed548f-b029-4b26-99e3-59510013f414"><img width="592" alt="image" src="https://github.com/greeeenmouth/LRDWWS/assets/31959671/a9739f49-ed8a-4a13-87cf-93056dadd154"># SLT2024 LRDWWS Challenge Baseline

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

### Results of test-a set

In the testing code provided with the baseline, an audio sample can be predicted as multiple wake words.  However, in the evaluation for the challenge system, only a single prediction is allowed for each audio sample, which may result in a decrease in FAR (False Alarm Rate) and an increase in FRR (False Reject Rate).  We provide the results obtained using the baseline testing script, as well as the results obtained using the challenge testing script. 

Evaluated by the testing script of the baseline:

| **Model**  | **Test set**     | **Intelligibility** | **Threshold** | **FAR** | **FRR** | **Score** |
| ---------- | ---------------- | ------------------- | ------------- | ------- | ------- | --------- |
| SDD_DF0023 | test/eval/DF0023 | 49.91               | 0.002         | 0.1668  | 0.3250  | 0.4918    |
| SDD_DF0026 | test/eval/DF0026 | 77.53               | 0.033         | 0.0144  | 0.0000  | 0.0144    |
| SDD_DF0028 | test/eval/DF0028 | 91.10               | 0.001         | 0.0741  | 0.0750  | 0.1491    |
| SDD_DF0030 | test/eval/DF0030 | 90.50               | 0.284         | 0.0036  | 0.0000  | 0.0036    |
| SDD_DM0022 | test/eval/DM0022 | 57.58               | 0.005         | 0.0929  | 0.2250  | 0.3179    |
| SDD_DM0024 | test/eval/DM0024 | 38.90               | 0.001         | 0.1127  | 0.3500  | 0.4627    |
| SDD_DM0025 | test/eval/DM0025 | 78.13               | 0.023         | 0.0311  | 0.1000  | 0.1311    |
| SDD_DM0027 | test/eval/DM0027 | 67.40               | 0.002         | 0.1095  | 0.1500  | 0.2595    |
| SDD_DM0029 | test/eval/DM0029 | 45.80               | 0.001         | 0.1338  | 0.1750  | 0.3088    |
| SDD_DM0031 | test/eval/DM0031 | 89.73               | 0.017         | 0.0259  | 0.0500  | 0.0759    |

Evaluated by the testing script of the challenge system:

| **Model**   | **Test set**     | **Intelligibility** | **Threshold** | **FAR** | **FRR** | **Score**  |
| ----------- | ---------------- | ------------------- | ------------- | ------- | ------- | ---------- |
| SDD_DF0023  | test/eval/DF0023 | 49.91               | 0.002         | 0.0736  | 0.5000  | 0.5736     |
| SDD_DF0026  | test/eval/DF0026 | 77.53               | 0.033         | 0.0116  | 0.0250  | 0.0366     |
| SDD_DF0028  | test/eval/DF0028 | 91.10               | 0.001         | 0.0351  | 0.4000  | 0.4351     |
| SDD_DF0030  | test/eval/DF0030 | 90.50               | 0.284         | 0.0033  | 0.0000  | 0.0033     |
| SDD_DM0022  | test/eval/DM0022 | 57.58               | 0.005         | 0.0497  | 0.3750  | 0.4247     |
| SDD_DM0024  | test/eval/DM0024 | 38.90               | 0.001         | 0.0562  | 0.5500  | 0.6062     |
| SDD_DM0025  | test/eval/DM0025 | 78.13               | 0.023         | 0.0234  | 0.1750  | 0.1984     |
| SDD_DM0027  | test/eval/DM0027 | 67.40               | 0.002         | 0.0574  | 0.1750  | 0.2324     |
| SDD_DM0029  | test/eval/DM0029 | 45.80               | 0.001         | 0.0597  | 0.4500  | 0.5097     |
| SDD_DM0031  | test/eval/DM0031 | 89.73               | 0.017         | 0.0164  | 0.0750  | 0.0914     |
| **average** |                  |                     |               | 0.0387  | 0.2725  | **0.3112** |

The average Score will be used as the ranking basis.

### Results of test-b set

Evaluated by the testing script of the baseline:

| **Model**      | **Test set**       | **Threshold** | **FAR**  | **FRR**  | **Score** |
| -------------- | ------------------ | ------------- | -------- | -------- | --------- |
| **SDD_DF0037** | test-b/eval/DF0037 | 0.01          | 0.034293 | 0.000000 | 0.034293  |
| **SDD_DM0032** | test-b/eval/DM0032 | 0.021         | 0.025128 | 0.000000 | 0.025128  |
| **SDD_DM0033** | test-b/eval/DM0033 | 0.007         | 0.118462 | 0.050000 | 0.168462  |
| **SDD_DM0034** | test-b/eval/DM0034 | 0.242         | 0.003807 | 0.020000 | 0.023807  |
| **SDD_DM0035** | test-b/eval/DM0035 | 0.001         | 0.075915 | 0.090000 | 0.165915  |
| **SDD_DM0036** | test-b/eval/DM0036 | 0.011         | 0.034099 | 0.045000 | 0.079099  |
| **SDD_DM0038** | test-b/eval/DM0038 | 0.009         | 0.011282 | 0.025000 | 0.036282  |
| **SDD_DM0039** | test-b/eval/DM0039 | 0.711         | 0.002564 | 0.000000 | 0.002564  |
| **SDD_DM0040** | test-b/eval/DM0040 | 0.003         | 0.045128 | 0.150000 | 0.195128  |
| **SDD_DM0041** | test-b/eval/DM0041 | 0.005         | 0.051795 | 0.050000 | 0.101795  |

Evaluated by the testing script of the challenge system:

| **Model**      | **Test set**       | **Threshold** | **FAR**  | **FRR**  | **Score** |
| -------------- | ------------------ | ------------- | -------- | -------- | --------- |
| **SDD_DF0037** | test-b/eval/DF0037 | 0.01          | 0.025654 | 0.025000 | 0.050654  |
| **SDD_DM0032** | test-b/eval/DM0032 | 0.021         | 0.016154 | 0.050000 | 0.066154  |
| **SDD_DM0033** | test-b/eval/DM0033 | 0.007         | 0.068718 | 0.175000 | 0.243718  |
| **SDD_DM0034** | test-b/eval/DM0034 | 0.242         | 0.003807 | 0.020000 | 0.023807  |
| **SDD_DM0035** | test-b/eval/DM0035 | 0.001         | 0.048987 | 0.251667 | 0.300654  |
| **SDD_DM0036** | test-b/eval/DM0036 | 0.011         | 0.021279 | 0.070000 | 0.091279  |
| **SDD_DM0038** | test-b/eval/DM0038 | 0.009         | 0.033846 | 0.025000 | 0.058846  |
| **SDD_DM0039** | test-b/eval/DM0039 | 0.711         | 0.002564 | 0.000000 | 0.002564  |
| **SDD_DM0040** | test-b/eval/DM0040 | 0.003         | 0.030000 | 0.275000 | 0.305000  |
| **SDD_DM0041** | test-b/eval/DM0041 | 0.005         | 0.035385 | 0.125000 | 0.160385  |
| **average**    |                    |               | 0.028639 | 0.101667 | **0.130306**  |

## Notice

- The baseline code we provided will output FAR and FRR under different thresholds during the test phase (stage 3). However, in the test phase of the challenge, participants are only allowed to submit a final wake-up result for each speech clip. Also, during the test phase, we will not provide annotations for eval in the test set. This means that participants need to think about how to choose the appropriate threshold.
- Participants may use all methods to improve the final results, including the use of pre-trained models and other open-source datasets, provided that this is explicitly stated in the final paper or system report submitted.
- If the scores of the two teams on the test data set are the same, the system with lower computation complexity will be judged as the superior one. In this case, participants will be asked to provide proof of computational complexity. Therefore, participants are strongly advised to retain their code for verification purposes.

## License

It is noted that the code can only be used for comparative or benchmarking purposes.  Users can only use code supplied under a License for non-commercial purposes.

## Contact

Please contact e-mail [lrdwws_challenge@aishelldata.com](mailto:lrdwws_challenge@aishelldata.com) if you have any queries.
