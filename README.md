# SEI activity summary


## Purpose

This is a casual research project aiming to gauge user activity across environments for the SEI network.
The main goal is to educate and to engage developers, community and users in exploring data in interesting and useful ways.


## Methods

The methods used are fairly simple, purely number of contract interactions on several dates ordered by interactions, descending.
Data is pulled from [Flipside](https://flipsidecrypto.xyz) which is free to access.
Most of this can be done by anyone including those with very little or no experience, with some assistance from an openAI tool like [chatGPT](https://chat.openai.com/chat) or [Claude](https://claude.ai).


### Gathering Data

<details>

<summary>SQL</summary>

This SQL query fetches data from both environments over several staggered dates to ensure a fair comparison:

1. **`relevant_dates` CTE:**
   - This Common Table Expression (CTE) defines a list of specific dates, representing every second Monday over the past three months.

2. **`evm_data` CTE:**
   - This CTE selects data from the `sei.core_evm.fact_transactions` table, focusing on transactions where the `to_address` (contract address) is not null. It filters records to include only those with a `block_timestamp` matching the dates listed in `relevant_dates`. The data is grouped by day and contract address, counting the number of interactions (`COUNT(*)`). The results are ordered by the number of interactions in descending order and limited to 1000 records for manageability.

3. **`cosmwasm_data` CTE:**
   - Similar to `evm_data`, this CTE selects data from the `sei.core.fact_msgs` table, using `tx_id` as the identifier for interactions (assuming it relates to contract interactions). It also filters by the specified dates, groups by day and `tx_id`, counts the interactions, and orders and limits the results similarly to `evm_data`.

4. **Final `SELECT` Statement:**
   - This statement combines the results from the `evm_data` and `cosmwasm_data` CTEs using `UNION ALL`, ensuring that all records from both environments are included. It selects the day, environment (either 'EVM' or 'CosmWasm'), contract address, and the number of interactions, ordering the combined results by day and interactions in ascending order.

5. **The final `ORDER BY` clause:**
   - Sorts the combined results by interactions in descending order `(DESC)`, followed by day in ascending order `(ASC)`.

</details>

## Data Analysis

<details>

<summary>python</summary>

Here's an updated summary of the Python script following your style:

---

### Python Script Overview

**Intake CSV Data:**
- Reads data from the specified CSV file using `pd.read_csv()`.

**Data Processing:**
- Converts the 'DAY' column to datetime format with `pd.to_datetime()`, handling errors by coercing invalid entries to `NaT`.
- Removes rows where 'DAY' couldn't be converted to datetime (`NaT` values).

**Plotting Functions:**
1. **plot_top20_by_environment(data, environment, output_file):** Creates a horizontal bar chart of the top 20 contracts by interactions for each environment (EVM or CosmWasm), sorted in descending order.
2. **plot_top10_overall(data, output_file):** Creates a bar chart for the top 10 most interacted contracts across all environments.
3. **plot_interactions_by_environment(data, output_file):** Creates a bar chart showing total interactions by environment (EVM and CosmWasm).
4. **plot_top20_excluding_top5(data, environment, output_file):** Generates a chart excluding the top 5 most interacted contracts in the specified environment, showing the next top 20. 
The reasoning for this was that the extreme outliers seen on the top end of the EVM environment are indicative of script/bot activity, or some other automated action which is not directly relevant to this study and potentially heavily skews the final result. **[to be re-asssessed upon further discovery]**

**Generates Visual Charts:**
- Utilizes the plotting functions to generate visual data representations, saving the charts as PNG files.

</details>


## Additional Notes

In order to give context to what types of activity this data is indicating, we will attempt to identify specifically what each of the contracts is being used for, and by whhat or by whom. 
This is very important to consider when drawing any conclusions from the presented data. 

This [reference sheet](https://github.com/cordt-sei/sei-env-activity/blob/main/data/labels.md) will be populated and updated as information arrives.
