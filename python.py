import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data (assuming your dataset is 'university_student_dashboard_data.csv')
df = pd.read_csv('university_student_dashboard_data.csv')

# 1. Total Applications, Admissions, and Enrollments per Term
term_data = df.groupby('Term').agg({
    'Applications': 'sum',
    'Admitted': 'sum',
    'Enrolled': 'sum'
}).reset_index()

fig1 = px.line(term_data, x='Term', y=['Applications', 'Admitted', 'Enrolled'],
               title="Total Applications, Admissions, and Enrollments per Term",
               labels={'Term': 'Term', 'value': 'Count'},
               line_shape='linear')

fig1.update_traces(mode='markers+lines')
st.plotly_chart(fig1)

# 2. Retention Rate Trends Over Time
fig2 = px.line(df, x='Term', y='Retention Rate (%)', 
               title="Retention Rate Trends Over Time",
               labels={'Term': 'Term', 'Retention Rate (%)': 'Retention Rate (%)'},
               line_shape='linear')

fig2.update_traces(mode='markers+lines')
st.plotly_chart(fig2)

# 3. Student Satisfaction Scores Over the Years
yearly_satisfaction = df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

fig3 = px.line(yearly_satisfaction, x='Year', y='Student Satisfaction (%)',
               title="Student Satisfaction Scores Over the Years",
               labels={'Year': 'Year', 'Student Satisfaction (%)': 'Student Satisfaction (%)'},
               line_shape='linear')

fig3.update_traces(mode='markers+lines')
st.plotly_chart(fig3)

# 4. Enrollment Breakdown by Department (Engineering, Business, Arts, Science)
department_enrollment = df[['Term', 'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].melt(id_vars=['Term'], var_name='Department', value_name='Enrollments')

fig4 = px.line(department_enrollment, x='Term', y='Enrollments', color='Department',
               title="Enrollment Breakdown by Department",
               labels={'Term': 'Term', 'Enrollments': 'Enrollments'},
               line_shape='linear')

fig4.update_traces(mode='markers+lines')
st.plotly_chart(fig4)

# 5. Comparison Between Spring vs. Fall Term Trends
spring_fall_data = df[df['Term'].isin(['Spring', 'Fall'])]

fig5 = px.line(spring_fall_data, x='Year', y=['Applications', 'Admitted', 'Enrolled'], 
               color='Term',
               title="Comparison Between Spring vs. Fall Term Trends",
               labels={'Year': 'Year', 'value': 'Count', 'Term': 'Term'},
               line_shape='linear')

fig5.update_traces(mode='markers+lines')
st.plotly_chart(fig5)

# 6. Comparison Between Departments, Retention Rates, and Satisfaction Levels
# Prepare data for comparison (reshaping)
enrollment_data = df[['Term', 'Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].melt(id_vars=['Term'], var_name='Department', value_name='Enrollments')
retention_data = df[['Term', 'Retention Rate (%)']].copy()
retention_data['Metric'] = 'Retention Rate'

satisfaction_data = df[['Term', 'Student Satisfaction (%)']].copy()
satisfaction_data['Metric'] = 'Student Satisfaction'

# Combine all data into a single dataframe
combined_data = pd.concat([enrollment_data, retention_data[['Term', 'Retention Rate (%)', 'Metric']], satisfaction_data[['Term', 'Student Satisfaction (%)', 'Metric']]], ignore_index=True)

fig6 = px.line(combined_data, x='Term', y=combined_data.columns[1], color='Metric', line_group='Metric',
               title="Departmental Enrollment, Retention Rates, and Satisfaction Trends",
               labels={'Term': 'Term', 'value': 'Percentage/Enrollments'})

fig6.update_traces(mode='markers+lines')
st.plotly_chart(fig6)
