import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pipeline_functions as pf

# Page configuration
st.set_page_config(
    page_title="Data Portfolio Dashboard",
    layout="wide",
    page_icon="📊"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        padding: 1rem 0;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1E3A8A;
        padding: 0.5rem 0;
        border-bottom: 2px solid #E5E7EB;
        margin-top: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .portfolio-section {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103655.png", width=100)
    st.title("Portfolio Dashboard")
    selected_page = st.radio(
        "Navigate to:",
        ["🏠 Home", "📈 Top Apps Pipeline", "📊 Data Visualizations", 
         "📁 Project Portfolio", "👤 About Me"]
    )
    
    # Contact info in sidebar
    st.divider()
    st.markdown("### 📬 Contact")
    st.markdown("""
    **Email:** portfolio@example.com  
    **LinkedIn:** [linkedin.com/in/portfolio](https://linkedin.com)  
    **GitHub:** [github.com/portfolio](https://github.com)
    """)

# ==================== HOME PAGE ====================
if selected_page == "🏠 Home":
    # Hero Section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<h1 class="main-header">📊 Data Science Portfolio Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("""
        ### Welcome to my interactive portfolio!
        
        This dashboard showcases my data engineering and analysis projects, 
        featuring interactive visualizations and real-time data pipelines.
        
        **Explore the sections:**
        - **Top Apps Pipeline**: Dynamic filtering and data processing
        - **Data Visualizations**: Interactive charts and insights
        - **Project Portfolio**: Collection of my data projects
        - **About Me**: Background and skills
        """)
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103655.png", width=200)
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Projects", "12", "+3")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Data Points", "1.2M", "↑ 15%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Categories", "15", "All")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Last Updated", "Today", "Live")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("### 🔄 Recent Activity")
    activity_data = pd.DataFrame({
        'Date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12'],
        'Activity': ['Pipeline Optimization', 'New Visualizations Added', 
                     'Data Cleaning Completed', 'Project Documentation Updated'],
        'Status': ['✅ Completed', '🔄 In Progress', '✅ Completed', '✅ Completed']
    })
    st.dataframe(activity_data, use_container_width=True, hide_index=True)

# ==================== TOP APPS PIPELINE PAGE ====================
elif selected_page == "📈 Top Apps Pipeline":
    st.markdown('<h1 class="main-header">📈 Top Apps Pipeline Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="portfolio-section">', unsafe_allow_html=True)
    
    # Category options
    CATEGORIES = [
        "ART_AND_DESIGN", "AUTO_AND_VEHICLES", "BEAUTY", "BOOKS_AND_REFERENCE",
        "BUSINESS", "COMICS", "COMMUNICATION", "DATING", "EDUCATION",
        "ENTERTAINMENT", "EVENTS", "FAMILY", "FINANCE", "FOOD_AND_DRINK", "GAME"
    ]
    
    # Controls in expander
    with st.expander("⚙️ Pipeline Controls", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category = st.selectbox(
                "Category",
                options=CATEGORIES,
                index=CATEGORIES.index("FOOD_AND_DRINK"),
                help="Select app category to analyze"
            )
        
        with col2:
            min_rating = st.slider(
                "Minimum rating",
                min_value=0.0,
                max_value=5.0,
                value=4.0,
                step=0.1,
                help="Filter apps by minimum rating"
            )
        
        with col3:
            min_reviews = st.number_input(
                "Minimum reviews",
                min_value=0,
                value=1000,
                step=100,
                help="Filter apps by minimum number of reviews"
            )
    
    # Run pipeline button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Pipeline Analysis", type="primary", use_container_width=True):
            with st.spinner("Processing data..."):
                # Run pipeline
                apps_data = pf.extract("apps_data.csv")
                reviews_data = pf.extract("review_data.csv")
                
                top_apps_data = pf.transform(
                    apps=apps_data,
                    reviews=reviews_data,
                    category=category,
                    min_rating=float(min_rating),
                    min_reviews=int(min_reviews),
                )
                
                pf.load(
                    dataframe=top_apps_data,
                    database_name="market_research",
                    table_name="top_apps"
                )
                
                st.success("✅ Pipeline completed successfully!")
                
                # Display results
                st.markdown(f"**Results:** Found **{len(top_apps_data)}** apps matching criteria")
                
                # Create two columns for data display and summary
                col_a, col_b = st.columns([3, 2])
                
                with col_a:
                    st.dataframe(
                        top_apps_data,
                        use_container_width=True,
                        height=400
                    )
                
                with col_b:
                    # Summary statistics
                    st.markdown("### 📊 Summary Statistics")
                    
                    if len(top_apps_data) > 0:
                        avg_rating = top_apps_data['rating'].mean()
                        avg_reviews = top_apps_data['reviews'].mean()
                        total_reviews = top_apps_data['reviews'].sum()
                        
                        st.metric("Average Rating", f"{avg_rating:.2f} ⭐")
                        st.metric("Average Reviews", f"{avg_reviews:,.0f}")
                        st.metric("Total Reviews", f"{total_reviews:,.0f}")
                        
                        # Top 3 apps
                        st.markdown("### 🏆 Top 3 Apps")
                        top_3 = top_apps_data.nlargest(3, 'rating')
                        for idx, row in top_3.iterrows():
                            st.markdown(f"**{row.get('app', 'N/A')}** - {row['rating']:.1f}⭐")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== DATA VISUALIZATIONS PAGE ====================
elif selected_page == "📊 Data Visualizations":
    st.markdown('<h1 class="main-header">📊 Interactive Data Visualizations</h1>', unsafe_allow_html=True)
    
    # Sample data for visualization (replace with your actual data)
    st.markdown('<div class="portfolio-section">', unsafe_allow_html=True)
    
    # Load sample data or create dummy data
    @st.cache_data
    def create_sample_data():
        categories = CATEGORIES
        data = {
            'Category': categories,
            'Avg_Rating': [4.2 + 0.1 * i for i in range(len(categories))],
            'Total_Reviews': [10000 + i * 5000 for i in range(len(categories))],
            'Number_of_Apps': [50 + i * 10 for i in range(len(categories))]
        }
        return pd.DataFrame(data)
    
    viz_data = create_sample_data()
    
    # Visualization 1: Bar Chart
    st.markdown("### 📊 Category Performance")
    fig1 = px.bar(
        viz_data,
        x='Category',
        y='Avg_Rating',
        color='Total_Reviews',
        title='Average Rating by Category',
        color_continuous_scale='viridis'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Visualization 2: Scatter Plot
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Reviews vs Rating")
        fig2 = px.scatter(
            viz_data,
            x='Total_Reviews',
            y='Avg_Rating',
            size='Number_of_Apps',
            color='Category',
            hover_name='Category',
            title='Reviews vs Rating Distribution'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Category Distribution")
        fig3 = px.pie(
            viz_data,
            values='Number_of_Apps',
            names='Category',
            title='App Distribution by Category'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PROJECT PORTFOLIO PAGE ====================
elif selected_page == "📁 Project Portfolio":
    st.markdown('<h1 class="main-header">📁 Project Portfolio</h1>', unsafe_allow_html=True)
    
    projects = [
        {
            "name": "Top Apps Analysis Pipeline",
            "description": "ETL pipeline for analyzing top mobile applications with dynamic filtering",
            "technologies": ["Python", "Streamlit", "Pandas", "SQL"],
            "status": "✅ Completed",
            "github": "https://github.com"
        },
        {
            "name": "Real-time Sentiment Analysis",
            "description": "Real-time sentiment analysis of app reviews using NLP",
            "technologies": ["TensorFlow", "NLTK", "FastAPI", "Docker"],
            "status": "🔄 In Progress",
            "github": "https://github.com"
        },
        {
            "name": "Market Trend Predictor",
            "description": "ML model predicting app market trends and success factors",
            "technologies": ["Scikit-learn", "XGBoost", "Plotly", "PostgreSQL"],
            "status": "✅ Completed",
            "github": "https://github.com"
        },
        {
            "name": "Data Quality Monitor",
            "description": "Automated data quality monitoring system with alerts",
            "technologies": ["Airflow", "Great Expectations", "Slack API", "MongoDB"],
            "status": "✅ Completed",
            "github": "https://github.com"
        },
    ]
    
    # Display projects in columns
    cols = st.columns(2)
    for idx, project in enumerate(projects):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"""
                <div style='padding: 1rem; border-radius: 10px; border: 1px solid #E5E7EB; margin: 0.5rem 0; background-color: white;'>
                    <h3>{project['name']}</h3>
                    <p>{project['description']}</p>
                    <p><strong>Technologies:</strong> {', '.join(project['technologies'])}</p>
                    <p><strong>Status:</strong> {project['status']}</p>
                    <a href="{project['github']}" target="_blank">🔗 View on GitHub</a>
                </div>
                """, unsafe_allow_html=True)

# ==================== ABOUT ME PAGE ====================
elif selected_page == "👤 About Me":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
        st.markdown("""
        ### Contact Info
        📧 email@example.com  
        🔗 linkedin.com/in/yourprofile  
        💻 github.com/yourusername  
        📱 +1 (234) 567-8900
        """)
    
    with col2:
        st.markdown('<h1 class="main-header">👤 About Me</h1>', unsafe_allow_html=True)
        st.markdown("""
        ## Data Scientist & Engineer
        
        Passionate data professional with expertise in building scalable data pipelines, 
        creating interactive dashboards, and deriving actionable insights from complex datasets.
        
        ### 🎯 Core Competencies
        - **Data Engineering**: ETL/ELT pipelines, data warehousing, workflow orchestration
        - **Data Analysis**: Statistical analysis, trend identification, business intelligence
        - **Machine Learning**: Predictive modeling, NLP, recommendation systems
        - **Data Visualization**: Interactive dashboards, data storytelling
        - **Cloud Technologies**: AWS, GCP, Azure data services
        
        ### 📚 Education
        - **MSc in Data Science** - University of Technology (2020-2022)
        - **BSc in Computer Science** - State University (2016-2020)
        
        ### 🏆 Certifications
        - AWS Certified Data Analytics
        - Google Data Engineer Professional
        - Databricks Data Engineer Associate
        """)
    
    # Skills Chart
    st.markdown("### 📊 Technical Skills")
    skills_data = pd.DataFrame({
        'Skill': ['Python', 'SQL', 'Data Visualization', 'ML/AI', 'Cloud Platforms', 'Data Pipelines'],
        'Proficiency': [95, 90, 85, 80, 75, 90]
    })
    
    fig = px.bar(
        skills_data,
        x='Proficiency',
        y='Skill',
        orientation='h',
        color='Proficiency',
        color_continuous_scale='viridis',
        title='Technical Proficiency Levels'
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 1rem;'>
    <p>📊 Data Portfolio Dashboard • Built with Streamlit • Last updated: January 2024</p>
    <p>© 2024 All rights reserved</p>
</div>
""", unsafe_allow_html=True)
