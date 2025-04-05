# ETL Pipeline Project

## Overview

The ETL pipeline collects mobile sales data from **five different sources**:

1. **Google Sheets** (Sales Data)
2. **JSON File** (Customer Reviews)
3. **CSV File** (Marketplace Sales)
4. **MongoDB** (Store Inventory Data)
5. **REST API** (Competitor Pricing)

### Steps in the ETL Pipeline:
1. **Extract**: Data is extracted from the above sources (Google Sheets, JSON, CSV, MongoDB, REST API).
2. **Transform**:
   - Data Cleaning (handling missing values, duplicates).
   - Data Normalization (converting date formats, standardizing product names).
   - Data Aggregation (total sales, average ratings, remaining stock).
   - Feature Engineering (revenue per unit, sentiment analysis).
   - Standardize measurement units (currency conversions).
3. **Load**: Transformed data is loaded into a MongoDB database.

## Setup Instructions

### 1. Clone the Repository
To get started, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/ETL_Pipeline_Mehwish_013.git
