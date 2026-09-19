-- 1. Total number of companies
SELECT COUNT(*) AS total_companies FROM companies;

-- 2. Top 10 companies by latest year sales
SELECT company_id, sales, year
FROM profitandloss
WHERE year = (SELECT MAX(year) FROM profitandloss)
ORDER BY sales DESC
LIMIT 10;

-- 3. Average operating profit margin by year
SELECT year, AVG(opm_percentage) AS avg_opm
FROM profitandloss
GROUP BY year
ORDER BY year;

-- 4. Companies with negative net profit in the latest year
SELECT company_id, net_profit, year
FROM profitandloss
WHERE year = (SELECT MAX(year) FROM profitandloss)
AND net_profit < 0;

-- 5. Sector-wise company count
SELECT broad_sector, COUNT(*) AS num_companies
FROM sectors
GROUP BY broad_sector
ORDER BY num_companies DESC;

-- 6. Companies with highest debt-to-equity ratio
SELECT company_id, debt_to_equity, year
FROM financial_ratios
WHERE year = (SELECT MAX(year) FROM financial_ratios)
ORDER BY debt_to_equity DESC
LIMIT 10;

-- 7. Average market cap by sector
SELECT s.broad_sector, AVG(m.market_cap_crore) AS avg_market_cap
FROM market_cap m
JOIN sectors s ON m.company_id = s.company_id
GROUP BY s.broad_sector
ORDER BY avg_market_cap DESC;

-- 8. Companies with balance sheet imbalance (>1% mismatch)
SELECT company_id, year, total_assets, total_liabilities,
       ROUND(ABS(total_assets - total_liabilities) * 100.0 / total_liabilities, 2) AS pct_diff
FROM balancesheet
WHERE total_liabilities != 0
AND ABS(total_assets - total_liabilities) / total_liabilities > 0.01
ORDER BY pct_diff DESC
LIMIT 10;

-- 9. Year-over-year sales growth for a specific company (RELIANCE)
SELECT year, sales,
       LAG(sales) OVER (ORDER BY year) AS prev_year_sales,
       ROUND((sales - LAG(sales) OVER (ORDER BY year)) * 100.0 / LAG(sales) OVER (ORDER BY year), 2) AS yoy_growth_pct
FROM profitandloss
WHERE company_id = 'RELIANCE'
ORDER BY year;

-- 10. Companies present in peer_groups but with FK count check
SELECT peer_group_name, COUNT(*) AS num_members
FROM peer_groups
GROUP BY peer_group_name
ORDER BY num_members DESC;