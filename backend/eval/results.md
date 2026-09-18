# SQM-Guard Evaluation Results

## 1. Injection Defense

- Total test cases: 11
- Malicious cases: 7
- Caught: 7/7
- Catch rate: 100.0%
- False positives: 0

The injection-defense evaluation successfully detected all malicious test cases while producing no false positives in the tested safe cases.

## 2. Query Generation & Self-Repair

- Total alerts tested: 15
- First-try executable rate: 73.33%
- Final executable rate with repair: 80.0%
- Improvement from repair: 6.67 percentage points
- Total repair attempts: 4

The self-repair mechanism improved the final executable-query rate from 73.33% to 80.0% on the 15 tested alerts.

## 3. Campaign Correlation

- Multi-stage attack correctly grouped: Yes
- Unrelated alerts correctly excluded: Yes
- Total campaigns detected: 1

The campaign-correlation test successfully grouped the related multi-stage alerts while excluding the unrelated alerts in the tested scenario.

## 4. Honest Limitations

- The injection-defense evaluation currently contains 11 test cases, so the sample size is relatively small.
- Query validation is based on the project's structural validator and does not represent execution against a live Microsoft Sentinel environment.
- Query generation depends on the locally hosted LLM and may produce different results for different runs.
- Campaign correlation was tested with synthetic scenarios and should be evaluated with additional scenarios for stronger evidence.