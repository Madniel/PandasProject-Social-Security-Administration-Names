# PandasProject-Social-Security-Administration-Names
The Social Security Administration website has posted data listing names and their frequency of occurrence from 1880 to 2019. CSV format data files are available https://www.ssa.gov/oact/babynames/names.zip.

1. Load the data from all files into a single table (using Pandas).
2. It will determine how many different (unique) names were given during that time.
3. Determine how many different (unique) names were given during this time period, distinguishing between male and female names.
4. Create new columns frequency_male and frequency_female and determine the popularity of each name in each year by dividing the number of times the name was given by the total number of births for that gender.
5. Determine and display a graph consisting of two subgraphs, where the x-axis is the time scale and the y-axis represents:
the number of births in a given year (graph at top)
the ratio of the number of births of girls to the number of births of boys (bottom graph) In which year was the difference in the number of births between boys and girls the smallest and the largest?
6. Determine the 1000 most popular names for each gender over the entire time range, the method should be to determine the 1000 most popular names for each year and for each gender and then add them up to determine the top 1000 ranking for each gender.
7. Display graphs of change for the names Harry and Marilin and the first name in the female and male rankings:
on the Y-axis on the left the number of times the name was given in each year (note how many times the name was given in 1940, 1980, and 2019)?
On the Y-axis on the right, the popularity of these names in each year
8. Plot a graph by year and gender showing what percentage of the top1000 ranked names were given in each year. This graph describes the diversity of names, note the year in which the greatest difference in diversity was observed between male and female names.
9. Verify the hypothesis whether it is true that the distribution of the last letters of male names changed significantly during the observed period? In order to do so
aggregate all births in the full data set by year and sex and last letter,
extract data for the years 1910, 1960, 2015
normalize the data to the total number of births in a given year
display the letter popularity data for each gender as a bar chart containing each year and where the bars are grouped by letter. Note for which letter there was the greatest increase/decrease between 1910 and 2015)
For the 3 letters for which the greatest change was observed, display the popularity trend over time
10. Find names that were given to both girls and boys (note the most popular male and female name)
11. Try to find the most popular names that were female/male names for a while and then became male/female names.
try to calculate for each name the ratio in which it was given to boys and girls
then calculate the aggregated value of this ratio in the period 1880-1920 and in the period 2000-2020 and on this basis select the names for which the observed change is the greatest (note the two most popular names)
Plot the course of the trend for these names
12. Load data from the database describing mortality in the period 1959-2018 in individual age groups: USA_ltper_1x1.sqlite, description: https://www.mortality.org/Public/ExplanatoryNotes.php. Try to aggregate the data already at the SQL query stage.
13. Determine the birth rate for the period being analyzed
14. Determine and display the survival rate of children in the first year of life
15. Determine the survival rate of children in the first 5 years of life on the graph in (14) (remember that for birth year x, consider mortality in age group 0 years in year x, 1 year in year x+1, etc.).
