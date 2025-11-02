Feature: Test the Orange HRM job titles

Scenario: To fetch the job titles in the job titles section of OrangeHRM website

Given The user is on the landing page of the website
When the user clicks on the Admin tab and the Jobs tab
And then the user clicks on the Job titles tab
Then the job titles are displayed to the user

