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

The Python script does the following:

1. **Intake CSV Data:**
   - Reads from specified CSV using `pd.read_csv()`.

2. **Data Processing:**
   - Converts the 'DAY' column to a datetime format using `pd.to_datetime()` with error handling to coerce invalid entries to `NaT` (Not a Time).
   - Drops rows where the 'DAY' column could not be converted to datetime (those with `NaT` values).

3. **Plotting Functions:**
   - `plot_top_interacted(data, output_file)`: Creates a horizontal bar chart of the top 10 contracts by interactions, sorted in descending order.
   - `plot_interactions_by_environment(data, output_file)`: Creates a bar chart showing total interactions, by environment (EVM/CW).

4. **Generates Visual Charts:**
   - Uses plot data to generate visualized data and export as PNG files.

</details>


## Additional Notes

In order to give context to what types of activity this data is indicating, we will attempt to identify specifically what each of the contracts is being used for, and by whhat or by whom. 
This is very important to consider when drawing any conclusions from the presented data. 

This [reference sheet](https://github.com/cordt-sei/sei-env-activity/blob/main/labels.md) will be populated and updated as information arrives.
