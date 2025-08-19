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

# Enhanced enterprise-grade CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 50%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .enterprise-badge {
        background: linear-gradient(135deg, #1e40af 0%, #6366f1 50%, #8b5cf6 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        margin: 1.5rem auto;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        max-width: fit-content;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        border-color: #6366f1;
    }
    
    .operational-metrics {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .operational-metrics:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.4);
    }
    
    .operational-metrics h4 {
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .operational-metrics h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Section Styles */
    .section-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .compliance-section {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #3b82f6;
        border-left: 5px solid #2563eb;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
    }
    
    .governance-section {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
        border: 1px solid #f59e0b;
        border-left: 5px solid #d97706;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.1);
    }
    
    /* Risk Assessment Styles */
    .risk-critical {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #ef4444;
        border-left: 5px solid #dc2626;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #f59e0b;
        border-left: 5px solid #d97706;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.1);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #22c55e;
        border-left: 5px solid #16a34a;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.1);
    }
    
    /* Benchmark Styles */
    .benchmark-excellent {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #22c55e;
        border-left: 5px solid #16a34a;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(34, 197, 94, 0.1);
        transition: all 0.3s ease;
    }
    
    .benchmark-good {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #f59e0b;
        border-left: 5px solid #d97706;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
        transition: all 0.3s ease;
    }
    
    .benchmark-needs-improvement {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #ef4444;
        border-left: 5px solid #dc2626;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
        transition: all 0.3s ease;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    .css-1d391kg .css-1lsmgbg {
        color: #f1f5f9;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 15px rgba(99, 102, 241, 0.4);
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
    }
    
    /* Data Frame Styles */
    .dataframe {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric Display Enhancement */
    .metric-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress Indicators */
    .progress-container {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* Status Indicators */
    .status-excellent {
        color: #059669;
        font-weight: 600;
    }
    
    .status-good {
        color: #d97706;
        font-weight: 600;
    }
    
    .status-needs-work {
        color: #dc2626;
        font-weight: 600;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #6366f1;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Enhanced Card Layout */
    .info-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: #6366f1;
    }
    
    /* Custom Alert Styles */
    .alert-success {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 1px solid #10b981;
        border-left: 5px solid #059669;
        color: #065f46;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #f59e0b;
        border-left: 5px solid #d97706;
        color: #92400e;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #ef4444;
        border-left: 5px solid #dc2626;
        color: #991b1b;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Typography Enhancements */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b;
        font-weight: 600;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Footer Styles */
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 3rem;
        border: 1px solid #475569;
    }
    
    /* Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .enterprise-badge {
            font-size: 0.8rem;
            padding: 0.5rem 1rem;
        }
        
        .operational-metrics h3 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced title section with enterprise branding
st.markdown("""
<div class="fade-in">
    <h1 class="main-header">🏢 Enterprise SQL AlwaysOn Scaling Planner</h1>
    <div class="enterprise-badge">
        ✨ ENTERPRISE GRADE • ITIL 4 ALIGNED • INDUSTRY BENCHMARK COMPLIANT • GOVERNANCE READY ✨
    </div>
    <p class="subtitle">Strategic infrastructure scaling with automated compliance and governance frameworks</p>
</div>
""", unsafe_allow_html=True)

# Global certification mapping - focused on operations roles
skills_certifications = {
    'SQL Server DBA Expert': 'Microsoft Certified: Azure Database Administrator', 
    'Infrastructure Automation': 'Terraform Associate',
    'ITIL Service Manager': 'ITIL 4 Managing Professional'
}

# Global skills requirements calculation function  
def calculate_skills_requirements(clusters, automation_level, support_24x7, compliance_frameworks_count):
    """Calculate required skills based on scaling parameters - focused on operations roles"""
    
    # Base calculations per cluster ranges - operations focused
    base_requirements = {
        'SQL Server DBA Expert': max(2, math.ceil(clusters / 15)),   # 1 per 15 clusters  
        'Infrastructure Automation': max(1, math.ceil(clusters / 30)), # 1 per 30 clusters
        'ITIL Service Manager': max(1, math.ceil(clusters / 35)),     # 1 per 35 clusters
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
    # Compliance frameworks
    if 'compliance_requirements' not in st.session_state:
        st.session_state.compliance_requirements = {
            'sox_compliance': False,
            'gdpr_compliance': False,
            'hipaa_compliance': False,
            'pci_dss_compliance': False,
            'iso_27001_compliance': False,
            'fedramp_compliance': False,
            'nist_cybersecurity': False,
            'cobit_5': False
        }
    
    # Skills matrix - current staffing (user configurable) - operations focused
    # Always reset to ensure consistency with operations focus
    st.session_state.current_skills = {
        'SQL Server DBA Expert': st.session_state.get('current_skills', {}).get('SQL Server DBA Expert', 3), 
        'Infrastructure Automation': st.session_state.get('current_skills', {}).get('Infrastructure Automation', 1),
        'ITIL Service Manager': st.session_state.get('current_skills', {}).get('ITIL Service Manager', 2)
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
            'compliance_audit_program': False,
            'business_continuity_plan': False
        }

initialize_enterprise_state()

# Enhanced automation components with compliance mapping
if 'automation_components' not in st.session_state:
    st.session_state.automation_components = {
        # Infrastructure & Cloud (Enhanced)
        'Infrastructure as Code': {
            'enabled': False, 'weight': 8, 'effort': 150, 'category': 'Infrastructure',
            'description': 'Terraform for VPC, subnets, security groups, EC2 instances',
            'compliance_frameworks': ['SOX', 'ISO 27001', 'COBIT 5'],
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        'Multi-AZ High Availability': {
            'enabled': False, 'weight': 9, 'effort': 120, 'category': 'Infrastructure',
            'description': 'Automated failover across availability zones',
            'compliance_frameworks': ['SOX', 'FedRAMP'],
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Auto Scaling & Load Balancing': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Infrastructure',
            'description': 'Dynamic resource scaling based on demand',
            'compliance_frameworks': [],
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        'Network Security Automation': {
            'enabled': False, 'weight': 8, 'effort': 90, 'category': 'Infrastructure',
            'description': 'Automated security group and NACLs management',
            'compliance_frameworks': ['PCI DSS', 'ISO 27001'],
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        
        # Database & Performance (Enhanced)
        'SQL AlwaysOn Automation': {
            'enabled': False, 'weight': 10, 'effort': 200, 'category': 'Database',
            'description': 'Automated SQL Server AlwaysOn configuration and management',
            'compliance_frameworks': ['SOX', 'HIPAA'],
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Performance Optimization Engine': {
            'enabled': False, 'weight': 6, 'effort': 120, 'category': 'Database',
            'description': 'AI-driven query optimization and index management',
            'compliance_frameworks': [],
            'business_impact': 'Medium', 'technical_complexity': 'High'
        },
        'Database Lifecycle Management': {
            'enabled': False, 'weight': 7, 'effort': 150, 'category': 'Database',
            'description': 'Automated provisioning, scaling, and decommissioning',
            'compliance_frameworks': ['SOX'],
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        
        # Security & Compliance (Enhanced)
        'Zero-Trust Security Model': {
            'enabled': False, 'weight': 9, 'effort': 180, 'category': 'Security',
            'description': 'Identity-based access controls with continuous verification',
            'compliance_frameworks': ['PCI DSS', 'FedRAMP', 'ISO 27001'],
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Automated Patch Management': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Security',
            'description': 'Orchestrated patching with rollback capabilities',
            'compliance_frameworks': ['SOX', 'PCI DSS', 'FedRAMP'],
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        'Compliance Monitoring': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Security',
            'description': 'Continuous compliance validation and reporting',
            'compliance_frameworks': ['SOX', 'GDPR', 'HIPAA', 'PCI DSS'],
            'business_impact': 'Critical', 'technical_complexity': 'Medium'
        },
        'Data Loss Prevention': {
            'enabled': False, 'weight': 8, 'effort': 120, 'category': 'Security',
            'description': 'Automated data classification and protection',
            'compliance_frameworks': ['GDPR', 'HIPAA', 'PCI DSS'],
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        
        # Operations & Monitoring (Enhanced)
        'AI-Powered Monitoring': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Operations',
            'description': 'Machine learning-based anomaly detection and prediction',
            'compliance_frameworks': [],
            'business_impact': 'High', 'technical_complexity': 'High'
        },
        'Automated Incident Response': {
            'enabled': False, 'weight': 9, 'effort': 160, 'category': 'Operations',
            'description': 'Self-healing systems with escalation workflows',
            'compliance_frameworks': ['SOX', 'ISO 27001'],
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Service Orchestration': {
            'enabled': False, 'weight': 6, 'effort': 100, 'category': 'Operations',
            'description': 'Workflow automation across enterprise systems',
            'compliance_frameworks': ['COBIT 5'],
            'business_impact': 'Medium', 'technical_complexity': 'Medium'
        },
        
        # Backup & Recovery (Enhanced)
        'Cross-Region DR Automation': {
            'enabled': False, 'weight': 9, 'effort': 200, 'category': 'Backup',
            'description': 'Automated disaster recovery across geographic regions',
            'compliance_frameworks': ['SOX', 'FedRAMP'],
            'business_impact': 'Critical', 'technical_complexity': 'High'
        },
        'Point-in-Time Recovery': {
            'enabled': False, 'weight': 7, 'effort': 120, 'category': 'Backup',
            'description': 'Granular recovery with minimal data loss',
            'compliance_frameworks': ['SOX'],
            'business_impact': 'High', 'technical_complexity': 'Medium'
        },
        
        # Governance & Integration
        'Enterprise Service Bus': {
            'enabled': False, 'weight': 6, 'effort': 180, 'category': 'Integration',
            'description': 'API gateway and service mesh integration',
            'compliance_frameworks': ['COBIT 5'],
            'business_impact': 'Medium', 'technical_complexity': 'High'
        },
        'Self-Service Portal': {
            'enabled': False, 'weight': 5, 'effort': 150, 'category': 'Portal',
            'description': 'Enterprise portal with RBAC and workflow approval',
            'compliance_frameworks': ['SOX'],
            'business_impact': 'Medium', 'technical_complexity': 'Medium'
        }
    }

# Enhanced sidebar configuration with modern styling
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%); border-radius: 12px; margin-bottom: 1rem;">
    <h2 style="color: white; margin: 0;">🎛️ Enterprise Configuration</h2>
</div>
""", unsafe_allow_html=True)

# Current State Configuration
st.sidebar.markdown("### 🏢 Current State Assessment")
current_clusters = st.sidebar.number_input("SQL AO Clusters", min_value=1, max_value=1000, value=5)
current_resources = st.sidebar.number_input("Team Size", min_value=1, max_value=50, value=6)
current_cpu_cores = st.sidebar.number_input("CPU Cores per Cluster", min_value=8, max_value=128, value=32)
current_memory_gb = st.sidebar.number_input("Memory GB per Cluster", min_value=64, max_value=1024, value=256)
current_storage_tb = st.sidebar.number_input("Storage TB per Cluster", min_value=1, max_value=100, value=10)
ec2_per_cluster = st.sidebar.number_input("EC2 Instances per Cluster", min_value=2, max_value=10, value=3)

# Target State Configuration
st.sidebar.markdown("### 🎯 Target State")
target_clusters = st.sidebar.number_input("Target Clusters", min_value=current_clusters, max_value=10000, value=100)
timeframe = st.sidebar.number_input("Timeframe (months)", min_value=6, max_value=60, value=24)

# SLA Requirements
st.sidebar.markdown("### 📊 SLA Requirements")
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
    
    # Compliance score calculation
    enabled_compliance_components = sum(
        1 for comp in st.session_state.automation_components.values() 
        if comp['enabled'] and comp['compliance_frameworks']
    )
    total_compliance_components = sum(
        1 for comp in st.session_state.automation_components.values() 
        if comp['compliance_frameworks']
    )
    compliance_readiness = (enabled_compliance_components / total_compliance_components * 100) if total_compliance_components > 0 else 0
    
    # ITIL maturity calculation
    itil_implemented = sum(1 for practice in st.session_state.itil_practices.values() if practice['implemented'])
    itil_total = len(st.session_state.itil_practices)
    itil_maturity = (itil_implemented / itil_total * 100) if itil_total > 0 else 0
    
    # Skills gap analysis with dynamic calculation
    active_frameworks_count = sum(st.session_state.compliance_requirements.values())
    required_skills = calculate_skills_requirements(
        target_clusters, 
        automation_maturity, 
        support_24x7, 
        active_frameworks_count
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
    
    # Compliance risks
    if not any(comp['enabled'] for comp in st.session_state.automation_components.values() 
               if 'SOX' in comp['compliance_frameworks']):
        risks.append({
            'category': 'Compliance',
            'risk': 'SOX compliance gap in automated controls',
            'severity': 'Critical',
            'impact': 'Regulatory violations, audit failures, financial penalties'
        })
    
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
        'compliance_readiness': compliance_readiness,
        'itil_maturity': itil_maturity,
        'total_skill_gap': total_skill_gap,
        'critical_components': critical_components,
        'high_complexity_enabled': high_complexity_enabled,
        'risks': risks
    }

metrics = calculate_enterprise_metrics()

# Enhanced Executive Dashboard with modern cards
st.markdown('<div class="section-header">📊 Executive Dashboard</div>', unsafe_allow_html=True)

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
        <h4>📋 Compliance</h4>
        <h3>{metrics['compliance_readiness']:.0f}%</h3>
        <p>Readiness Score</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="operational-metrics">
        <h4>📚 ITIL</h4>
        <h3>{metrics['itil_maturity']:.0f}%</h3>
        <p>Practice Coverage</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    availability_color = "🟢" if availability_target >= 99.9 else "🟡" if availability_target >= 99.5 else "🔴"
    st.markdown(f"""
    <div class="metric-container">
        <h4>{availability_color} Availability</h4>
        <h3>{availability_target}%</h3>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-container">
        <h4>📈 Scale Factor</h4>
        <h3>{metrics['scale_factor']:.1f}x</h3>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-container">
        <h4>👥 Skills Gap</h4>
        <h3>{metrics['total_skill_gap']} roles</h3>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Compliance Dashboard
st.markdown('<div class="section-header">📋 Enterprise Compliance & Governance</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="compliance-section">
        <h4>🏛️ Regulatory Compliance Frameworks</h4>
        <p>Select applicable compliance requirements for your organization:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compliance framework selection with enhanced layout
    compliance_cols = st.columns(4)
    frameworks = list(st.session_state.compliance_requirements.keys())
    
    for i, framework in enumerate(frameworks):
        col_idx = i % 4
        with compliance_cols[col_idx]:
            enabled = st.checkbox(
                framework.replace('_', ' ').upper(),
                value=st.session_state.compliance_requirements[framework],
                key=f"compliance_{framework}"
            )
            st.session_state.compliance_requirements[framework] = enabled

with col2:
    active_frameworks = sum(st.session_state.compliance_requirements.values())
    
    st.markdown(f"""
    <div class="info-card">
        <h4>📜 Active Frameworks</h4>
        <h2 style="color: #6366f1;">{active_frameworks}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>🛡️ Compliance Score</h4>
        <h2 style="color: #6366f1;">{metrics['compliance_readiness']:.0f}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if metrics['compliance_readiness'] >= 80:
        st.markdown('<div class="alert-success">✅ Compliance Ready</div>', unsafe_allow_html=True)
    elif metrics['compliance_readiness'] >= 60:
        st.markdown('<div class="alert-warning">⚠️ Needs Improvement</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-error">❌ Significant Gaps</div>', unsafe_allow_html=True)

# Enhanced Skills & Workforce Planning section
st.markdown('<div class="section-header">👥 Operations Team Skills & Workforce Planning</div>', unsafe_allow_html=True)

# Calculate values needed for the markdown string
active_frameworks_count = sum(st.session_state.compliance_requirements.values())

st.markdown(f"""
<div class="info-card">
<strong>📊 Operations team requirements are dynamically calculated based on your scaling parameters:</strong>
<ul>
<li><strong>Target Clusters:</strong> {target_clusters} clusters</li>
<li><strong>Automation Level:</strong> {metrics['automation_maturity']:.0f}% (reduces staffing needs by up to 30%)</li>
<li><strong>Support Model:</strong> {'24x7 Global' if support_24x7 else 'Business Hours'} (affects staffing requirements)</li>
<li><strong>Focus:</strong> Core operations roles for SQL Server and infrastructure management</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Current staffing input section with enhanced styling
st.markdown("#### 📝 Current Operations Team Composition")
st.write("Enter your current staffing levels for each operations role:")

skills_input_cols = st.columns(3)
# Only show input fields for operations roles
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
st.markdown("#### 📊 Operations Skills Gap Analysis")

required_skills = calculate_skills_requirements(
    target_clusters, 
    metrics['automation_maturity'], 
    support_24x7, 
    active_frameworks_count
)

skills_data = []
# Only iterate through roles that exist in both current_skills and required_skills
for role in required_skills.keys():
    current = st.session_state.current_skills.get(role, 0)  # Use .get() with default 0
    required = required_skills[role]
    gap = max(0, required - current)
    
    skills_data.append({
        'Role': role,
        'Current Staff': current,
        'Required for Target': required,
        'Gap': gap if gap > 0 else 0,
        'Status': '✅ Adequate' if gap == 0 else f'⚠️ Need {gap} more',
        'Certification Required': skills_certifications[role],
        'Calculation Logic': f"Based on {target_clusters} clusters" + 
                           (f" with {metrics['automation_maturity']:.0f}% automation benefit" if metrics['automation_maturity'] > 0 else "") +
                           (" + 24x7 coverage" if support_24x7 else "")
    })

skills_df = pd.DataFrame(skills_data)

col1, col2 = st.columns([3, 1])

with col1:
    # Display the skills comparison table with enhanced styling
    st.dataframe(skills_df[['Role', 'Current Staff', 'Required for Target', 'Gap', 'Status', 'Certification Required']], use_container_width=True)
    
    # Show calculation methodology
    with st.expander("📖 How Skills Requirements Are Calculated"):
        st.markdown("""
        <div class="info-card">
        <strong>Calculation Methodology (Operations Focused):</strong>
        
        <ol>
        <li><strong>Base Requirements by Role:</strong>
           <ul>
           <li>SQL Server DBA Expert: 1 per 15 clusters</li>
           <li>Infrastructure Automation: 1 per 30 clusters</li>
           <li>ITIL Service Manager: 1 per 35 clusters</li>
           </ul>
        </li>
        <li><strong>Automation Impact:</strong> Up to 30% reduction in requirements with full automation</li>
        <li><strong>24x7 Support Multiplier:</strong> 40% increase for round-the-clock coverage</li>
        <li><strong>Role-Specific Adjustments:</strong> Infrastructure Automation benefits more from automation than DBA and ITIL roles</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Summary metrics - safe calculation
    total_current = sum(st.session_state.current_skills.get(role, 0) for role in required_skills.keys())
    total_required = sum(required_skills.values())
    total_gap = sum(max(0, required_skills[role] - st.session_state.current_skills.get(role, 0)) for role in required_skills.keys())
    
    st.markdown(f"""
    <div class="info-card">
        <h4>👥 Current Team Size</h4>
        <h2 style="color: #6366f1;">{total_current}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>🎯 Required Team Size</h4>
        <h2 style="color: #6366f1;">{total_required}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>⚠️ Total Skills Gap</h4>
        <h2 style="color: #ef4444;">{total_gap}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills readiness percentage
    if total_required > 0:
        skills_readiness = max(0, 100 - (total_gap / total_required * 100))
        
        st.markdown(f"""
        <div class="info-card">
            <h4>📊 Skills Readiness</h4>
            <h2 style="color: #6366f1;">{skills_readiness:.0f}%</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if skills_readiness >= 90:
            st.markdown('<div class="alert-success">✅ Team Ready</div>', unsafe_allow_html=True)
        elif skills_readiness >= 70:
            st.markdown('<div class="alert-warning">⚠️ Minor Gaps</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-error">❌ Significant Gaps</div>', unsafe_allow_html=True)
    
    # Automation benefit explanation
    if metrics['automation_maturity'] > 30:
        st.markdown(f"""
        <div class="info-card" style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);">
            <h4>💡 Automation Benefit</h4>
            <p>Automation is reducing your staffing needs by ~{metrics['automation_maturity']/100*30:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

# Continue with the rest of the application components...
# (Due to length constraints, I'll continue with key sections)

# Monthly Forecasting System with enhanced visuals
st.markdown("---")
st.markdown('<div class="section-header">📅 Monthly Scaling Forecast & Staffing Roadmap</div>', unsafe_allow_html=True)

def calculate_monthly_forecast():
    """Calculate month-by-month scaling forecast from current to target clusters"""
    
    # Calculate scaling timeline
    cluster_growth_per_month = (target_clusters - current_clusters) / timeframe
    
    # Automation maturity growth (assuming gradual implementation)
    automation_start = metrics['automation_maturity']
    automation_target = min(85, automation_start + 40)  # Cap at realistic 85%
    automation_growth_per_month = (automation_target - automation_start) / timeframe
    
    forecast_data = []
    
    for month in range(timeframe + 1):
        month_clusters = current_clusters + (cluster_growth_per_month * month)
        month_automation = automation_start + (automation_growth_per_month * month)
        
        # Calculate staffing requirements for this month
        month_required_skills = calculate_skills_requirements(
            int(month_clusters), 
            month_automation, 
            support_24x7, 
            active_frameworks_count
        )
        
        # Calculate hiring needs (assume 2-3 months lead time for hiring/training)
        hire_lead_time = 3
        target_month_for_hiring = month + hire_lead_time
        if target_month_for_hiring <= timeframe:
            target_clusters_for_hiring = current_clusters + (cluster_growth_per_month * target_month_for_hiring)
            target_automation_for_hiring = automation_start + (automation_growth_per_month * target_month_for_hiring)
            target_skills_for_hiring = calculate_skills_requirements(
                int(target_clusters_for_hiring), 
                target_automation_for_hiring, 
                support_24x7, 
                active_frameworks_count
            )
        else:
            target_skills_for_hiring = month_required_skills
        
        # Calculate new hires needed this month
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
        
        # Calculate costs (rough estimates)
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

# Create enhanced forecast visualization
col1, col2 = st.columns([2, 1])

with col1:
    # Cluster and team growth chart with enhanced styling
    months = [f"Month {d['month']}" for d in forecast_data]
    clusters = [d['clusters'] for d in forecast_data]
    team_sizes = [d['total_team_size'] for d in forecast_data]
    automation_levels = [d['automation_maturity'] for d in forecast_data]
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Cluster Growth & Team Size', 'Automation Maturity Growth'),
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    # Enhanced color scheme
    fig.add_trace(
        go.Scatter(x=months, y=clusters, name="Clusters", 
                  line=dict(color='#6366f1', width=3),
                  fill='tonexty'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=team_sizes, name="Team Size", 
                  line=dict(color='#10b981', width=3)),
        row=1, col=1, secondary_y=True
    )
    
    # Automation maturity with gradient fill
    fig.add_trace(
        go.Scatter(x=months, y=automation_levels, name="Automation %", 
                  line=dict(color='#f59e0b', width=3), 
                  fill='tonexty',
                  fillcolor='rgba(245, 158, 11, 0.1)'),
        row=2, col=1
    )
    
    fig.update_layout(
        height=500, 
        title_text="📈 Scaling Forecast Overview",
        template="plotly_white",
        font=dict(family="Inter")
    )
    fig.update_xaxes(title_text="Timeline", row=2, col=1)
    fig.update_yaxes(title_text="Clusters", row=1, col=1)
    fig.update_yaxes(title_text="Team Members", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Automation Maturity (%)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 🎯 Key Forecast Metrics")
    
    # Calculate key metrics
    total_hires_needed = sum(d['total_new_hires'] for d in forecast_data)
    peak_monthly_hires = max(d['total_new_hires'] for d in forecast_data)
    final_team_size = forecast_data[-1]['total_team_size']
    
    st.markdown(f"""
    <div class="info-card">
        <h4>👥 Total New Hires</h4>
        <h2 style="color: #6366f1;">{total_hires_needed}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>📊 Peak Monthly Hiring</h4>
        <h2 style="color: #6366f1;">{peak_monthly_hires}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>🎯 Final Team Size</h4>
        <h2 style="color: #6366f1;">{final_team_size}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>⚡ Final Automation Level</h4>
        <h2 style="color: #6366f1;">{forecast_data[-1]['automation_maturity']:.0f}%</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced hiring timeline alerts
    urgent_months = [d for d in forecast_data if d['total_new_hires'] > 2]
    if urgent_months:
        st.markdown(f'<div class="alert-warning">⚠️ High hiring periods: {len(urgent_months)} months need 3+ hires</div>', unsafe_allow_html=True)
    
    if total_hires_needed > 8:
        st.markdown('<div class="alert-error">🚨 Consider phased approach - high hiring volume</div>', unsafe_allow_html=True)
    elif total_hires_needed > 4:
        st.markdown('<div class="alert-warning">⚠️ Moderate hiring needs - plan recruitment</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-success">✅ Manageable hiring requirements</div>', unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3>🏢 Enterprise SQL AlwaysOn AWS EC2 Scaling Planner</h3>
    <p><strong>Version 3.0</strong> • Industry Benchmark Compliant • ITIL 4 Aligned • Enterprise Governance Ready</p>
    <p>Powered by Advanced Analytics & AI-Driven Forecasting</p>
</div>
""", unsafe_allow_html=True)