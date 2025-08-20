import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import math

# Page configuration
st.set_page_config(
    page_title="Enterprise SQL AlwaysOn Scaling Planner",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .enterprise-badge {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    .governance-section {
        background-color: #fefce8;
        border-left: 4px solid #ca8a04;
        padding: 1rem;
        margin: 1rem 0;
    }
    .operational-metrics {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .risk-critical {
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .risk-high {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .risk-medium {
        background-color: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .benchmark-excellent {
        background-color: #dcfce7;
        border-left: 4px solid #16a34a;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    .benchmark-good {
        background-color: #fef3c7;
        border-left: 4px solid #d97706;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    .benchmark-needs-improvement {
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and enterprise badge
st.markdown('<h1 class="main-header">🏢 Enterprise SQL AlwaysOn Scaling Planner</h1>', unsafe_allow_html=True)
st.markdown('<div class="enterprise-badge">ENTERPRISE GRADE • ITIL 4 ALIGNED • INDUSTRY BENCHMARK COMPLIANT • GOVERNANCE READY</div>', unsafe_allow_html=True)

# Global certification mapping - focused on operations roles
skills_certifications = {
    'SQL Server DBA Expert': 'Microsoft Certified: Azure Database Administrator', 
    'Infrastructure Automation': 'Terraform Associate',
    'ITIL Service Manager': 'ITIL 4 Managing Professional'
}

# Global skills requirements calculation function  
def calculate_skills_requirements(clusters, automation_level, support_24x7):
    """Calculate required skills based on scaling parameters - focused on operations roles"""
    
    # Base calculations per cluster ranges - operations focused
    base_requirements = {
        'SQL Server DBA Expert': max(2, math.ceil(clusters / 15)),   # 1 per 15 clusters  
        'Infrastructure Automation': max(1, math.ceil(clusters / 30)), # 1 per 30 clusters
        'ITIL Service Manager': max(1, math.ceil(clusters / 50)),     # 1 per 50 clusters (optimized)
    }
    
    # Adjustments based on automation level
    automation_multiplier = 1.0 - (automation_level / 100 * 0.3)  # Up to 30% reduction with full automation
    
    # 24x7 support multiplier
    support_multiplier = 1.4 if support_24x7 else 1.0
    
    # Apply multipliers
    adjusted_requirements = {}
    for role, base_req in base_requirements.items():
        if role in ['SQL Server DBA Expert', 'ITIL Service Manager']:
            # These roles are more affected by 24x7 and less by automation
            adjusted_req = math.ceil(base_req * support_multiplier * max(0.7, automation_multiplier))
        else:
            # Infrastructure Automation benefits more from automation
            adjusted_req = math.ceil(base_req * support_multiplier * automation_multiplier)
        
        adjusted_requirements[role] = max(1, adjusted_req) if base_req > 0 else 0
    
    return adjusted_requirements

# Initialize comprehensive enterprise state
def initialize_enterprise_state():
    # Skills matrix - current staffing (user configurable) - operations focused
    if 'current_skills' not in st.session_state:
        st.session_state.current_skills = {
            'SQL Server DBA Expert': 3, 
            'Infrastructure Automation': 1,
            'ITIL Service Manager': 2
        }
    
    # ITIL 4 service management practices
    if 'itil_practices' not in st.session_state:
        st.session_state.itil_practices = {
            'Strategy Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'High'},
            'Service Design': {'implemented': True, 'maturity': 'Managed', 'priority': 'High'},
            'Change Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'Critical'},
            'Incident Management': {'implemented': True, 'maturity': 'Defined', 'priority': 'Critical'},
            'Problem Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'High'},
            'Service Level Management': {'implemented': True, 'maturity': 'Managed', 'priority': 'High'},
            'Capacity Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'High'},
            'Availability Management': {'implemented': True, 'maturity': 'Defined', 'priority': 'Critical'},
            'Continuity Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'Medium'},
            'Service Validation & Testing': {'implemented': False, 'maturity': 'Initial', 'priority': 'Medium'},
            'Release Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'High'},
            'Configuration Management': {'implemented': False, 'maturity': 'Initial', 'priority': 'High'}
        }
    
    # Governance and risk framework
    if 'governance_framework' not in st.session_state:
        st.session_state.governance_framework = {
            'change_approval_board': False,
            'architecture_review_board': False,
            'risk_management_committee': False,
            'security_steering_committee': False,
            'business_continuity_plan': False
        }

initialize_enterprise_state()

# Enhanced automation components
if 'automation_components' not in st.session_state:
    st.session_state.automation_components = {
        # Infrastructure & Cloud (Enhanced)
        'Infrastructure as Code': {
            'enabled': False, 'weight': 8, 'effort': 150, 'category': 'Infrastructure',
            'description': 'Terraform for VPC, subnets, security groups, EC2 instances',
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        'Multi-AZ High Availability': {
            'enabled': False, 'weight': 9, 'effort': 120, 'category': 'Infrastructure',
            'description': 'Automated failover across availability zones',
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Auto Scaling & Load Balancing': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Infrastructure',
            'description': 'Dynamic resource scaling based on demand',
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        'Network Security Automation': {
            'enabled': False, 'weight': 8, 'effort': 90, 'category': 'Infrastructure',
            'description': 'Automated security group and NACLs management',
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        
        # Database & Performance (Enhanced)
        'SQL AlwaysOn Automation': {
            'enabled': False, 'weight': 10, 'effort': 200, 'category': 'Database',
            'description': 'Automated SQL Server AlwaysOn configuration and management',
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Performance Optimization Engine': {
            'enabled': False, 'weight': 6, 'effort': 120, 'category': 'Database',
            'description': 'AI-driven query optimization and index management',
            'business_impact': 'Medium', 'technical_complexity': 'High'
        },
        'Database Lifecycle Management': {
            'enabled': False, 'weight': 7, 'effort': 150, 'category': 'Database',
            'description': 'Automated provisioning, scaling, and decommissioning',
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        
        # Security & Compliance (Enhanced)
        'Zero-Trust Security Model': {
            'enabled': False, 'weight': 9, 'effort': 180, 'category': 'Security',
            'description': 'Identity-based access controls with continuous verification',
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Automated Patch Management': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Security',
            'description': 'Orchestrated patching with rollback capabilities',
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        'Compliance Monitoring': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Security',
            'description': 'Continuous compliance validation and reporting',
            'business_impact': 'Critical', 'technical_complexity': 'Medium'
        },
        'Data Loss Prevention': {
            'enabled': False, 'weight': 8, 'effort': 120, 'category': 'Security',
            'description': 'Automated data classification and protection',
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        
        # Operations & Monitoring (Enhanced)
        'AI-Powered Monitoring': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Operations',
            'description': 'Machine learning-based anomaly detection and prediction',
            'business_impact': 'High', 'technical_complexity': 'High'
        },
        'Automated Incident Response': {
            'enabled': False, 'weight': 9, 'effort': 160, 'category': 'Operations',
            'description': 'Self-healing systems with escalation workflows',
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Service Orchestration': {
            'enabled': False, 'weight': 6, 'effort': 100, 'category': 'Operations',
            'description': 'Workflow automation across enterprise systems',
            'business_impact': 'Medium', 'technical_complexity': 'Medium'
        },
        
        # Backup & Recovery (Enhanced)
        'Cross-Region DR Automation': {
            'enabled': False, 'weight': 9, 'effort': 200, 'category': 'Backup',
            'description': 'Automated disaster recovery across geographic regions',
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Point-in-Time Recovery': {
            'enabled': False, 'weight': 7, 'effort': 120, 'category': 'Backup',
            'description': 'Granular recovery with minimal data loss',
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        
        # Governance & Integration
        'Enterprise Service Bus': {
            'enabled': False, 'weight': 6, 'effort': 180, 'category': 'Integration',
            'description': 'API gateway and service mesh integration',
            'business_impact': 'Medium', 'technical_complexity': 'High'
        },
        'Self-Service Portal': {
            'enabled': False, 'weight': 5, 'effort': 150, 'category': 'Portal',
            'description': 'Enterprise portal with RBAC and workflow approval',
            'business_impact': 'Medium', 'technical_complexity': 'Medium'
        }
    }

# Sidebar configuration
st.sidebar.header("🎛️ Enterprise Configuration")

# Current State Configuration
st.sidebar.subheader("🏢 Current State Assessment")
current_clusters = st.sidebar.number_input("SQL AO Clusters", min_value=1, max_value=1000, value=5)
current_resources = st.sidebar.number_input("Team Size", min_value=1, max_value=50, value=6)
current_cpu_cores = st.sidebar.number_input("CPU Cores per Cluster", min_value=8, max_value=128, value=32)
current_memory_gb = st.sidebar.number_input("Memory GB per Cluster", min_value=64, max_value=1024, value=256)
current_storage_tb = st.sidebar.number_input("Storage TB per Cluster", min_value=1, max_value=100, value=10)
ec2_per_cluster = st.sidebar.number_input("EC2 Instances per Cluster", min_value=2, max_value=10, value=3)

# Target State Configuration
st.sidebar.subheader("🎯 Target State")
target_clusters = st.sidebar.number_input("Target Clusters", min_value=current_clusters, max_value=10000, value=100)
timeframe = st.sidebar.number_input("Timeframe (months)", min_value=6, max_value=60, value=24)

# SLA Requirements
st.sidebar.subheader("📊 SLA Requirements")
availability_target = st.sidebar.slider("Availability Target (%)", 95.0, 99.99, 99.9, 0.01)
rpo_minutes = st.sidebar.slider("RPO (minutes)", 5, 1440, 60, 5)
rto_minutes = st.sidebar.slider("RTO (minutes)", 15, 1440, 240, 15)

# Support model
support_24x7 = st.sidebar.checkbox("24x7 Global Support", value=False)

# Calculate comprehensive enterprise metrics
def calculate_enterprise_metrics():
    """Calculate enterprise-grade operational metrics"""
    
    # Automation maturity calculation
    total_weight = sum(comp['weight'] for comp in st.session_state.automation_components.values())
    enabled_weight = sum(comp['weight'] for comp in st.session_state.automation_components.values() if comp['enabled'])
    automation_maturity = (enabled_weight / total_weight) * 100 if total_weight > 0 else 0
    
    # Infrastructure metrics
    current_ec2_instances = current_clusters * ec2_per_cluster
    target_ec2_instances = target_clusters * ec2_per_cluster
    scale_factor = target_clusters / current_clusters
    
    # ITIL maturity calculation
    itil_implemented = sum(1 for practice in st.session_state.itil_practices.values() if practice['implemented'])
    itil_total = len(st.session_state.itil_practices)
    itil_maturity = (itil_implemented / itil_total * 100) if itil_total > 0 else 0
    
    # Skills gap analysis with dynamic calculation
    required_skills = calculate_skills_requirements(
        target_clusters, 
        automation_maturity, 
        support_24x7
    )
    
    total_skill_gap = sum(
        max(0, required_skills[role] - st.session_state.current_skills.get(role, 0))
        for role in required_skills.keys()
    )
    
    # Business impact assessment
    critical_components = sum(
        1 for comp in st.session_state.automation_components.values()
        if comp['enabled'] and comp['business_impact'] == 'Critical'
    )
    
    # Technical complexity assessment
    high_complexity_enabled = sum(
        1 for comp in st.session_state.automation_components.values()
        if comp['enabled'] and comp['technical_complexity'] == 'High'
    )
    
    # Risk assessment based on enterprise factors
    risks = []
    
    # Security risks
    if not st.session_state.automation_components['Zero-Trust Security Model']['enabled']:
        risks.append({
            'category': 'Security',
            'risk': 'Inadequate security model for enterprise scale',
            'severity': 'Critical',
            'impact': 'Data breaches, unauthorized access, security incidents'
        })
    
    # Operational risks
    if not st.session_state.automation_components['AI-Powered Monitoring']['enabled'] and target_clusters > 50:
        risks.append({
            'category': 'Operations',
            'risk': 'Manual monitoring at enterprise scale',
            'severity': 'High',
            'impact': 'Delayed incident detection, performance degradation'
        })
    
    # Governance risks
    if total_skill_gap > 5:
        risks.append({
            'category': 'Workforce',
            'risk': 'Critical skills gap for enterprise operations',
            'severity': 'High',
            'impact': 'Operational failures, knowledge dependencies, staff burnout'
        })
    
    # Business continuity risks
    if not st.session_state.automation_components['Cross-Region DR Automation']['enabled']:
        risks.append({
            'category': 'Business Continuity',
            'risk': 'Manual disaster recovery procedures',
            'severity': 'Critical',
            'impact': 'Extended downtime, data loss, business disruption'
        })
    
    return {
        'automation_maturity': automation_maturity,
        'current_ec2_instances': current_ec2_instances,
        'target_ec2_instances': target_ec2_instances,
        'scale_factor': scale_factor,
        'itil_maturity': itil_maturity,
        'total_skill_gap': total_skill_gap,
        'critical_components': critical_components,
        'high_complexity_enabled': high_complexity_enabled,
        'risks': risks
    }

metrics = calculate_enterprise_metrics()

# Executive Dashboard
st.subheader("📊 Executive Dashboard")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="operational-metrics">
        <h4>🔧 Automation</h4>
        <h3>{metrics['automation_maturity']:.0f}%</h3>
        <p>Maturity Level</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="operational-metrics">
        <h4>📚 ITIL</h4>
        <h3>{metrics['itil_maturity']:.0f}%</h3>
        <p>Practice Coverage</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    availability_color = "🟢" if availability_target >= 99.9 else "🟡" if availability_target >= 99.5 else "🔴"
    st.metric(f"{availability_color} Availability", f"{availability_target}%")

with col4:
    st.metric("📈 Scale Factor", f"{metrics['scale_factor']:.1f}x")

with col5:
    st.metric("👥 Skills Gap", f"{metrics['total_skill_gap']} roles")

with col6:
    st.metric("💻 EC2 Instances", f"{metrics['target_ec2_instances']}")

# Skills & Workforce Planning - Operations Focus with Monthly Forecasting
st.subheader("👥 Operations Team Skills & Workforce Planning")

st.markdown(f"""
**📊 Operations team requirements are dynamically calculated based on your scaling parameters:**
- **Target Clusters:** {target_clusters} clusters
- **Automation Level:** {metrics['automation_maturity']:.0f}% (reduces staffing needs by up to 30%)
- **Support Model:** {'24x7 Global' if support_24x7 else 'Business Hours'} (affects staffing requirements)
- **Focus:** Core operations roles for SQL Server and infrastructure management
""")

# Current staffing input section
st.markdown("### 📝 Current Operations Team Composition")
st.write("Enter your current staffing levels for each operations role:")

skills_input_cols = st.columns(3)
operations_roles = ['SQL Server DBA Expert', 'Infrastructure Automation', 'ITIL Service Manager']
for i, role in enumerate(operations_roles):
    col_idx = i % 3
    with skills_input_cols[col_idx]:
        current_count = st.number_input(
            f"**{role}**",
            min_value=0,
            max_value=20,
            value=st.session_state.current_skills.get(role, 0),
            key=f"current_{role}"
        )
        st.session_state.current_skills[role] = current_count

# Calculate requirements and create comparison table
st.markdown("### 📊 Operations Skills Gap Analysis")

required_skills = calculate_skills_requirements(
    target_clusters, 
    metrics['automation_maturity'], 
    support_24x7
)

skills_data = []
for role in required_skills.keys():
    current = st.session_state.current_skills.get(role, 0)
    required = required_skills[role]
    gap = max(0, required - current)
    
    skills_data.append({
        'Role': role,
        'Current Staff': current,
        'Required for Target': required,
        'Gap': gap if gap > 0 else 0,
        'Status': '✅ Adequate' if gap == 0 else f'⚠️ Need {gap} more',
        'Certification Required': skills_certifications[role]
    })

skills_df = pd.DataFrame(skills_data)

col1, col2 = st.columns([3, 1])

with col1:
    st.dataframe(skills_df[['Role', 'Current Staff', 'Required for Target', 'Gap', 'Status', 'Certification Required']], use_container_width=True)
    
    with st.expander("📖 How Skills Requirements Are Calculated"):
        st.markdown("""
        **Calculation Methodology (Operations Focused):**
        
        1. **Base Requirements by Role:**
           - SQL Server DBA Expert: 1 per 15 clusters  
           - Infrastructure Automation: 1 per 30 clusters
           - ITIL Service Manager: 1 per 35 clusters
        
        2. **Automation Impact:** Up to 30% reduction in requirements with full automation
        
        3. **24x7 Support Multiplier:** 40% increase for round-the-clock coverage
        
        4. **Role-Specific Adjustments:** Infrastructure Automation benefits more from automation than DBA and ITIL roles
        """)

with col2:
    total_current = sum(st.session_state.current_skills.get(role, 0) for role in required_skills.keys())
    total_required = sum(required_skills.values())
    total_gap = sum(max(0, required_skills[role] - st.session_state.current_skills.get(role, 0)) for role in required_skills.keys())
    
    st.metric("👥 Current Team Size", f"{total_current}")
    st.metric("🎯 Required Team Size", f"{total_required}")
    st.metric("⚠️ Total Skills Gap", f"{total_gap}")
    
    if total_required > 0:
        skills_readiness = max(0, 100 - (total_gap / total_required * 100))
        st.metric("📊 Skills Readiness", f"{skills_readiness:.0f}%")
        
        if skills_readiness >= 90:
            st.success("✅ Team Ready")
        elif skills_readiness >= 70:
            st.warning("⚠️ Minor Gaps")
        else:
            st.error("❌ Significant Gaps")
    
    if metrics['automation_maturity'] > 30:
        st.info(f"💡 Automation is reducing your staffing needs by ~{metrics['automation_maturity']/100*30:.0f}%")

# Monthly Forecasting System
st.markdown("---")
st.markdown("### 📅 Monthly Scaling Forecast & Staffing Roadmap")

def calculate_monthly_forecast():
    """Calculate month-by-month scaling forecast from current to target clusters"""
    
    cluster_growth_per_month = (target_clusters - current_clusters) / timeframe
    automation_start = metrics['automation_maturity']
    automation_target = min(85, automation_start + 40)
    automation_growth_per_month = (automation_target - automation_start) / timeframe
    
    forecast_data = []
    
    for month in range(timeframe + 1):
        month_clusters = current_clusters + (cluster_growth_per_month * month)
        month_automation = automation_start + (automation_growth_per_month * month)
        
        month_required_skills = calculate_skills_requirements(
            int(month_clusters), 
            month_automation, 
            support_24x7
        )
        
        hire_lead_time = 3
        target_month_for_hiring = month + hire_lead_time
        if target_month_for_hiring <= timeframe:
            target_clusters_for_hiring = current_clusters + (cluster_growth_per_month * target_month_for_hiring)
            target_automation_for_hiring = automation_start + (automation_growth_per_month * target_month_for_hiring)
            target_skills_for_hiring = calculate_skills_requirements(
                int(target_clusters_for_hiring), 
                target_automation_for_hiring, 
                support_24x7
            )
        else:
            target_skills_for_hiring = month_required_skills
        
        current_total = sum(st.session_state.current_skills.get(role, 0) for role in month_required_skills.keys())
        if month == 0:
            previous_required = current_total
        else:
            previous_required = sum(forecast_data[-1]['required_skills'].values())
        
        new_hires_needed = {}
        total_new_hires = 0
        
        for role in month_required_skills.keys():
            current_role_staff = st.session_state.current_skills.get(role, 0)
            if month == 0:
                previous_role_required = current_role_staff
            else:
                previous_role_required = forecast_data[-1]['required_skills'].get(role, 0)
            
            target_role_required = target_skills_for_hiring.get(role, 0)
            new_hires_this_role = max(0, target_role_required - previous_role_required)
            new_hires_needed[role] = new_hires_this_role
            total_new_hires += new_hires_this_role
        
        avg_salary_by_role = {
            'SQL Server DBA Expert': 95000,
            'Infrastructure Automation': 85000,
            'ITIL Service Manager': 80000
        }
        
        monthly_cost = sum(
            month_required_skills.get(role, 0) * avg_salary_by_role[role] / 12
            for role in avg_salary_by_role.keys()
        )
        
        forecast_data.append({
            'month': month,
            'clusters': int(month_clusters),
            'automation_maturity': month_automation,
            'required_skills': month_required_skills,
            'new_hires_needed': new_hires_needed,
            'total_new_hires': total_new_hires,
            'monthly_cost': monthly_cost,
            'total_team_size': sum(month_required_skills.values())
        })
    
    return forecast_data

forecast_data = calculate_monthly_forecast()

# Create forecast visualization
col1, col2 = st.columns([2, 1])

with col1:
    months = [f"Month {d['month']}" for d in forecast_data]
    clusters = [d['clusters'] for d in forecast_data]
    team_sizes = [d['total_team_size'] for d in forecast_data]
    automation_levels = [d['automation_maturity'] for d in forecast_data]
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Cluster Growth & Team Size', 'Automation Maturity Growth'),
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Scatter(x=months, y=clusters, name="Clusters", line=dict(color='blue', width=3)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=team_sizes, name="Team Size", line=dict(color='green', width=3)),
        row=1, col=1, secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(x=months, y=automation_levels, name="Automation %", 
                  line=dict(color='orange', width=3), fill='tonexty'),
        row=2, col=1
    )
    
    fig.update_layout(height=500, title_text="📈 Scaling Forecast Overview")
    fig.update_xaxes(title_text="Timeline", row=2, col=1)
    fig.update_yaxes(title_text="Clusters", row=1, col=1)
    fig.update_yaxes(title_text="Team Members", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Automation Maturity (%)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🎯 Key Forecast Metrics")
    
    total_hires_needed = sum(d['total_new_hires'] for d in forecast_data)
    peak_monthly_hires = max(d['total_new_hires'] for d in forecast_data)
    final_team_size = forecast_data[-1]['total_team_size']
    
    st.metric("👥 Total New Hires", f"{total_hires_needed}")
    st.metric("📊 Peak Monthly Hiring", f"{peak_monthly_hires}")
    st.metric("🎯 Final Team Size", f"{final_team_size}")
    st.metric("⚡ Final Automation Level", f"{forecast_data[-1]['automation_maturity']:.0f}%")
    
    urgent_months = [d for d in forecast_data if d['total_new_hires'] > 2]
    if urgent_months:
        st.warning(f"⚠️ High hiring periods: {len(urgent_months)} months need 3+ hires")
    
    if total_hires_needed > 8:
        st.error("🚨 Consider phased approach - high hiring volume")
    elif total_hires_needed > 4:
        st.warning("⚠️ Moderate hiring needs - plan recruitment")
    else:
        st.success("✅ Manageable hiring requirements")

# Detailed monthly breakdown
st.markdown("### 📊 Detailed Monthly Roadmap")

monthly_breakdown = []
for data in forecast_data:
    if data['month'] % 3 == 0 or data['total_new_hires'] > 0:
        month_row = {
            'Month': f"Month {data['month']}",
            'Clusters': data['clusters'],
            'Team Size': data['total_team_size'],
            'New Hires': data['total_new_hires'],
            'Automation %': f"{data['automation_maturity']:.0f}%"
        }
        
        for role in ['SQL Server DBA Expert', 'Infrastructure Automation', 'ITIL Service Manager']:
            if data['new_hires_needed'].get(role, 0) > 0:
                month_row[f'{role} Hires'] = data['new_hires_needed'][role]
        
        monthly_breakdown.append(month_row)

breakdown_df = pd.DataFrame(monthly_breakdown)
st.dataframe(breakdown_df, use_container_width=True)

# Hiring recommendations
st.markdown("### 🎯 Strategic Hiring Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🥇 Priority 1: SQL Server DBA")
    dba_hires = sum(d['new_hires_needed'].get('SQL Server DBA Expert', 0) for d in forecast_data)
    st.write(f"**Total needed:** {dba_hires}")
    st.write("**Timeline:** Start immediately")
    st.write("**Lead time:** 2-3 months")
    st.write("**Focus:** SQL Server AlwaysOn expertise")

with col2:
    st.markdown("#### 🥈 Priority 2: Infrastructure Automation")
    infra_hires = sum(d['new_hires_needed'].get('Infrastructure Automation', 0) for d in forecast_data)
    st.write(f"**Total needed:** {infra_hires}")
    st.write("**Timeline:** Month 2-3")
    st.write("**Lead time:** 1-2 months")
    st.write("**Focus:** Terraform, AWS automation")

with col3:
    st.markdown("#### 🥉 Priority 3: ITIL Service Manager")
    itil_hires = sum(d['new_hires_needed'].get('ITIL Service Manager', 0) for d in forecast_data)
    st.write(f"**Total needed:** {itil_hires}")
    st.write("**Timeline:** Month 4-6")
    st.write("**Lead time:** 1-2 months") 
    st.write("**Focus:** Service operations, incident mgmt")

# Risk assessment for hiring plan
st.markdown("---")
st.markdown("### ⚠️ Hiring Plan Risk Assessment")

hiring_risks = []

if total_hires_needed > 10:
    hiring_risks.append({
        'risk': 'High volume hiring may strain recruitment and training capacity',
        'impact': 'Delayed onboarding, quality issues',
        'mitigation': 'Consider external recruiters, structured onboarding program'
    })

if peak_monthly_hires > 3:
    hiring_risks.append({
        'risk': 'Peak hiring months may overwhelm team integration',
        'impact': 'Reduced productivity, cultural integration issues',
        'mitigation': 'Stagger start dates, assign mentors, extended onboarding'
    })

skill_gaps = [role for role, gap in {
    'SQL Server DBA Expert': sum(d['new_hires_needed'].get('SQL Server DBA Expert', 0) for d in forecast_data),
    'Infrastructure Automation': sum(d['new_hires_needed'].get('Infrastructure Automation', 0) for d in forecast_data),
    'ITIL Service Manager': sum(d['new_hires_needed'].get('ITIL Service Manager', 0) for d in forecast_data)
}.items() if gap > 3]

if skill_gaps:
    hiring_risks.append({
        'risk': f'High demand for specialized roles: {", ".join(skill_gaps)}',
        'impact': 'Difficulty finding qualified candidates, salary inflation',
        'mitigation': 'Early recruitment, internal training programs, contractor bridge'
    })

if hiring_risks:
    for risk in hiring_risks:
        st.markdown(f"""
        <div class="risk-high">
            <strong>Risk:</strong> {risk['risk']}<br>
            <strong>Impact:</strong> {risk['impact']}<br>
            <strong>Mitigation:</strong> {risk['mitigation']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("🎉 Hiring plan appears manageable with standard recruitment processes!")

# Action items
st.markdown("---")
st.markdown("### ✅ Immediate Action Items")

action_items = []

immediate_hires = [d for d in forecast_data[:3] if d['total_new_hires'] > 0]
if immediate_hires:
    action_items.append(f"🎯 Start recruitment for {immediate_hires[0]['total_new_hires']} positions in next 3 months")

if metrics['automation_maturity'] < 50:
    action_items.append("📚 Develop automation training program for existing team")

if current_clusters < 20 and target_clusters > 50:
    action_items.append("🏗️ Begin infrastructure automation setup to support scaling")

if total_hires_needed > 5:
    action_items.append("👥 Establish structured onboarding and mentorship program")

for i, item in enumerate(action_items, 1):
    st.write(f"{i}. {item}")

if not action_items:
    st.info("✅ Current planning appears well-structured. Monitor progress quarterly.")

# ITIL 4 Service Management Framework
st.subheader("📚 ITIL 4 Service Management Practices")

itil_cols = st.columns(4)
for i, (practice, data) in enumerate(st.session_state.itil_practices.items()):
    col_idx = i % 4
    with itil_cols[col_idx]:
        implemented = st.checkbox(
            f"**{practice}**",
            value=data['implemented'],
            key=f"itil_{practice}"
        )
        
        if implemented:
            maturity = st.selectbox(
                "Maturity Level",
                ["Initial", "Defined", "Managed", "Optimized"],
                index=["Initial", "Defined", "Managed", "Optimized"].index(data['maturity']),
                key=f"maturity_{practice}"
            )
            st.session_state.itil_practices[practice]['maturity'] = maturity
        
        priority_color = {
            'Critical': '🔴',
            'High': '🟡', 
            'Medium': '🟢'
        }
        st.caption(f"{priority_color[data['priority']]} {data['priority']} Priority")
        
        st.session_state.itil_practices[practice]['implemented'] = implemented

# Enhanced Automation Components
st.subheader("⚡ Enterprise Automation Framework")

categories = {
    'Infrastructure': '🏗️',
    'Database': '🗄️',
    'Security': '🔒',
    'Operations': '⚙️',
    'Backup': '💾',
    'Integration': '🔗',
    'Portal': '📱'
}

tabs = st.tabs([f"{icon} {cat}" for cat, icon in categories.items()])

for tab, (category, icon) in zip(tabs, categories.items()):
    with tab:
        category_components = [
            (name, comp) for name, comp in st.session_state.automation_components.items()
            if comp['category'] == category
        ]
        
        for comp_name, comp_data in category_components:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                enabled = st.checkbox(
                    f"**{comp_name}**",
                    value=comp_data['enabled'],
                    key=f"auto_{comp_name}"
                )
                
                st.caption(comp_data['description'])
                
                impact_color = {'Critical': '🔴', 'High': '🟡', 'Medium': '🟢'}
                complexity_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                
                st.caption(f"**Impact:** {impact_color[comp_data['business_impact']]} {comp_data['business_impact']} | "
                          f"**Complexity:** {complexity_color[comp_data['technical_complexity']]} {comp_data['technical_complexity']}")
                
                st.session_state.automation_components[comp_name]['enabled'] = enabled
            
            with col2:
                st.write(f"**Weight:** {comp_data['weight']}%")
                st.write(f"**Effort:** {comp_data['effort']}h")
            
            st.markdown("---")

# Enterprise Risk Assessment
st.subheader("🛡️ Enterprise Risk Assessment & Governance")

if metrics['risks']:
    for risk in metrics['risks']:
        severity_class = f"risk-{risk['severity'].lower()}"
        st.markdown(f"""
        <div class="{severity_class}">
            <strong>{risk['category']} Risk - {risk['severity']}: {risk['risk']}</strong><br>
            <em>Business Impact:</em> {risk['impact']}<br>
            <em>Governance Action Required:</em> Implement corresponding automation and governance controls
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("🎉 Enterprise risk profile is well-managed with current automation strategy!")

# Industry Benchmark Comparison
st.subheader("📈 Industry Benchmark Assessment")

benchmark_scores = {
    'Database Availability': {
        'our_score': availability_target,
        'industry_avg': 99.5,
        'industry_leader': 99.99,
        'unit': '%'
    },
    'Automation Maturity': {
        'our_score': metrics['automation_maturity'],
        'industry_avg': 45,
        'industry_leader': 85,
        'unit': '%'
    },
    'ITIL Practice Coverage': {
        'our_score': metrics['itil_maturity'],
        'industry_avg': 60,
        'industry_leader': 90,
        'unit': '%'
    },
    'RTO Performance': {
        'our_score': rto_minutes,
        'industry_avg': 240,
        'industry_leader': 60,
        'unit': 'min',
        'lower_is_better': True
    }
}

for metric_name, scores in benchmark_scores.items():
    lower_is_better = scores.get('lower_is_better', False)
    
    if lower_is_better:
        if scores['our_score'] <= scores['industry_leader']:
            benchmark_class = "benchmark-excellent"
            status = "🏆 Industry Leading"
        elif scores['our_score'] <= scores['industry_avg']:
            benchmark_class = "benchmark-good"
            status = "✅ Above Average"
        else:
            benchmark_class = "benchmark-needs-improvement"
            status = "⚠️ Needs Improvement"
    else:
        if scores['our_score'] >= scores['industry_leader']:
            benchmark_class = "benchmark-excellent"
            status = "🏆 Industry Leading"
        elif scores['our_score'] >= scores['industry_avg']:
            benchmark_class = "benchmark-good"
            status = "✅ Above Average"
        else:
            benchmark_class = "benchmark-needs-improvement"
            status = "⚠️ Needs Improvement"
    
    st.markdown(f"""
    <div class="{benchmark_class}">
        <strong>{metric_name}:</strong> {scores['our_score']}{scores['unit']} | 
        Industry Avg: {scores['industry_avg']}{scores['unit']} | 
        Leader: {scores['industry_leader']}{scores['unit']} | 
        <em>{status}</em>
    </div>
    """, unsafe_allow_html=True)

# Enterprise Governance Framework
st.subheader("🏛️ Enterprise Governance Framework")

st.markdown("""
<div class="governance-section">
    <h4>📊 Governance Bodies & Committees</h4>
    <p>Essential governance structures for enterprise-scale SQL Server operations:</p>
</div>
""", unsafe_allow_html=True)

governance_cols = st.columns(3)
governance_items = list(st.session_state.governance_framework.keys())

for i, item in enumerate(governance_items):
    col_idx = i % 3
    with governance_cols[col_idx]:
        enabled = st.checkbox(
            item.replace('_', ' ').title(),
            value=st.session_state.governance_framework[item],
            key=f"governance_{item}"
        )
        st.session_state.governance_framework[item] = enabled

governance_maturity = sum(st.session_state.governance_framework.values()) / len(st.session_state.governance_framework) * 100
st.metric("🏛️ Governance Maturity", f"{governance_maturity:.0f}%")

# Executive Summary
st.subheader("📊 Executive Summary & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Current Maturity Assessment")
    st.write(f"**Automation Maturity:** {metrics['automation_maturity']:.0f}% ({'Advanced' if metrics['automation_maturity'] >= 70 else 'Developing' if metrics['automation_maturity'] >= 40 else 'Initial'})")
    st.write(f"**ITIL Practice Coverage:** {metrics['itil_maturity']:.0f}% ({'Mature' if metrics['itil_maturity'] >= 70 else 'Developing'})")
    st.write(f"**Governance Framework:** {governance_maturity:.0f}% ({'Established' if governance_maturity >= 70 else 'Needs Development'})")

with col2:
    st.markdown("### 🚀 Strategic Recommendations")
    
    recommendations = []
    
    if metrics['automation_maturity'] < 60:
        recommendations.append("🔧 Prioritize automation components with high business impact")
    
    if metrics['total_skill_gap'] > 3:
        recommendations.append("👥 Develop comprehensive skills development program")
    
    if metrics['itil_maturity'] < 70:
        recommendations.append("📚 Establish ITIL 4 service management practices")
    
    if governance_maturity < 70:
        recommendations.append("🏛️ Implement enterprise governance framework")
    
    if not recommendations:
        recommendations.append("✅ Continue execution of current strategy")
        recommendations.append("📈 Focus on operational excellence and continuous improvement")
    
    for rec in recommendations:
        st.write(f"• {rec}")

# Certification Status
st.markdown("---")
st.markdown("### 🏆 Enterprise Certification Status")

if (metrics['automation_maturity'] >= 70 and 
    metrics['itil_maturity'] >= 70 and 
    governance_maturity >= 70):
    st.success("🏆 **ENTERPRISE GRADE CERTIFIED** - This solution meets industry benchmark standards for enterprise SQL Server scaling")
elif (metrics['automation_maturity'] >= 50):
    st.warning("⚠️ **ENTERPRISE READY** - Solution has strong foundation, recommended improvements identified")
else:
    st.error("❌ **DEVELOPMENT REQUIRED** - Significant gaps exist, not yet enterprise-grade")

# Footer
st.markdown("---")
st.markdown("*Enterprise SQL AlwaysOn AWS EC2 Scaling Planner v3.0 - Industry Benchmark Compliant | ITIL 4 Aligned | Enterprise Governance Ready*")