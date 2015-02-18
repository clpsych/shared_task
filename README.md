#CLPsych Shared Task Evaluation

##Publication and Presentation
Results from participation in the Shared Task will be treated differently from the workshop submissions, and be due on a different schedule.
We will create a paper describing the data, evaluation, results, score-level system combinations and some analysis and synthesis of results.
Shared task participants are invited to submit a 2-8 page paper describing their systems. These papers will be subject to a light peer review and included in the workshop proceedings.

The shared task will be presented in a similar hybrid manner to the paper: one of the organizers will give an overview description of the task, data, evaluation, system combination, and results analysis and synthesis. Some teams may be asked to talk about their system in particular, the exact details of which will be finalized as the workshop schedule solidifies.

Post-workshop, we may consider
putting together an overarching article about the shared task and its
results for submission to a top-tier journal.

##Paradigm
For a fair assessment of the systems created from the shared task, we will conduct a blind evaluation with some held-out Twitter users. These Twitter users will be distributed in the same manner as previously, but without their condition labels. 

Each system should indicate what resources were used in the creation of their models (e.g., was LIWC used? A list of medication names scraped from wikipedia?). 

The only __DISALLOWED__ data resource is the data distributed as part of the hackathon. The train/test splits for the shared task need to be respected, and some of the Twitter users included in the hackathon were removed, shuffled, or truncated. Whatever trained system that was used as part of the hackathon should be easily retrained on the designated training section here. 
	
The distributed test data has age- and gender-matched pairs of Twitter users (as the training data did), with enough noise and obfuscation to make it hard to exploit this fact (please don't try though). The Twitter users are not paired up, nor are they distributed together. Systems should rank order (and optionally score) each Twitter user in each condition, and submit those complete ranked lists. Our scoring scripts will remove all the distractor items, so the scores will only be computed on the age- and gender-matched users. Similarly, it's important that each system computes scores for all three conditions (Depression-v-Control, PTSD-v-Control and Depression-v-PTSD), to minimize the bias introduced by the data collection mechanisms. Systems that cannot successfully separate Depression and PTSD may be depending upon those artifacts to make their decisions rather than signals more deeply relevant to mental health. 

The systems will be evaluated via ranked lists, in a format indicated below.
Each system must create one ranked list for each condition (Depression-v-Control [DvC], PTSD-v-Control [PvC], and Depression-v-PTSD [DvP]). Each system may be submitted with up to 5 parameter settings (perhaps optimized to different criteria). Thus, for each system, we expect to see at least 3 and at most 15 score files (if you want to do more than this, contact me so we can discuss it).

The ranking files should be a csv file keyed with your institution (`JohnsHopkins`), a system monicker (`WhimsicalRandomnessClassifier`), designator for a parameter setting (`3`, interpretable to you), and condition contained (`PvD`), joined by `_`s.
 
 `JohnsHopkins_WhimsicalRandomnessClassifier_3_PvD.csv`

| rank | screen_name    | score |
|------|------------------------|
| 1    | anonymoususer1 | 0.83  |
| 2    | anonymoususer7 | 0.64  |
| 3    | anonymoususer9 | 0.53  |

The `score` column is optional, but will allow us to better make use of it in system combination. Bonus points (because it makes our job easier) if your scores reflect the probability your model thinks the Twitter user has the first condition in the comparison (e.g., in `PvD` higher scores indicate higher probability of `PTSD`).

We will share our evaluation code in the shared task repository: [github.com/clpsych/](https://github.com/clpsych/) shared_task so you can test your output format. Similarly, we will include an example ranking csv file so the format is entirely clear. That repository is not yet complete, but we will send out an email notification when it is complete.


##Evaluation
We will evaluate the score files according to a range of metrics that may provide insight into various aspects of system performance -- we will measure many and provide them all to the participants, but we will treat average precision (AP) as the single 'official' metric. From all parameter settings for each system we will report measures from the system with the highest AP. In addition to AP, we will also calculate precision, recall, sensitivity, specificity, precision at [5%, 10%, 20%] false positives.

Our scoring scripts will make some easily interpretable plots, as well as some more in depth analysis of the system performance, and make some appropriate raw data available to you. There is no single measure that can capture all relevant use cases and nuances, so individual teams are free to discuss other metrics more in depth.  We are willing to consider incorporating other statistics from the scoring data to enable you to make various plots upon request.


##All data distributed by March 10
- This maintains accordance with Twitter's TOS and JHU's IRB requirements.
- You have all the training data necessary already to build your systems, so the next few weeks should be used to have the system ready to produce the necessary ranking files.

##Required in Glen's inbox by March 13
- `Institution_SystemName_#_condition.csv` score files
- A `.tgz` of all these together is perfectly fine.

##Scores returned by March 20
- Your scores will be posted on the clpsych website and available for download, a link will be circulated to the page with all the downloads.
- For anonymity, we will strip the institution name when posting the data. Our example above, `JohnsHopkins_WhimsicalRandomnessClassifier_3_PvD.csv` would be posted as `WhimsicalRandomnessClassifier_3_PvD_scores.csv`


##Required in the conference submssion site by March 27
- Contributing authors from the institution.
- A 2-8 page PDF description of the system (which we put through a light peer review process).

##Notification of changes by April 3
- We will lightly peer review the papers and may request some changes.

##Required in the conference submission site by April 10
- Camera ready versions of the paper (PDF, in the format required by the workshop).

If you have any questions, please don't hesitate to contact Glen: coppersmith--at--jhu--.--edu