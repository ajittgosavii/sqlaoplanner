import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import math

# Optional AWS integration - gracefully handle if boto3 not installed
try:
    import boto3
    import json
    from decimal import Decimal
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Enterprise SQL Server Scaling Platform | Strategic Planning & TCO Analysis",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Corporate CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        letter-spacing: -0.025em;
    }
    .enterprise-badge {
        background: linear-gradient(135deg, #1e40af 0%, #3730a3 50%, #1e1b4b 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .executive-summary {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-left: 6px solid #1e40af;
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    .cost-summary {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    .savings-highlight {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
    .governance-framework {
        background-color: #fefce8;
        border-left: 6px solid #ca8a04;
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    .operational-metrics {
        background: linear-gradient(135deg, #1e40af 0%, #3730a3 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
    .risk-critical {
        background-color: #fef2f2;
        border-left: 6px solid #dc2626;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .risk-high {
        background-color: #fefbeb;
        border-left: 6px solid #f59e0b;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .risk-medium {
        background-color: #f0fdf4;
        border-left: 6px solid #10b981;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .benchmark-excellent {
        background-color: #f0fdf4;
        border-left: 6px solid #16a34a;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
    }
    .benchmark-good {
        background-color: #fefbeb;
        border-left: 6px solid #d97706;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
    }
    .benchmark-needs-improvement {
        background-color: #fef2f2;
        border-left: 6px solid #dc2626;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
    }
    .licensing-framework {
        background-color: #f8fafc;
        border: 2px solid #e2e8f0;
        padding: 2rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    .subsection-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .data-table {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Corporate header and branding
st.markdown('<h1 class="main-header">Enterprise SQL Server Infrastructure Planning Platform</h1>', unsafe_allow_html=True)
st.markdown('''
<div class="enterprise-badge">
Workforce-Centric Analysis | Dynamic Parameters | Infrastructure Automation | Service Management Framework | Governance & Compliance
</div>
''', unsafe_allow_html=True)

# Show AWS integration status
if not BOTO3_AVAILABLE:
    st.info("Real-time AWS pricing integration unavailable. Using representative pricing data. To enable live pricing updates, install boto3 package and configure AWS credentials.")

# AWS Pricing API Integration
@st.cache_data(ttl=3600)
def get_aws_pricing():
    """Fetch real-time AWS pricing including SQL Server License-Included costs"""
    
    if not BOTO3_AVAILABLE:
        return {
            'ec2_windows': {
                'm5.xlarge': 0.384, 'm5.2xlarge': 0.768, 'm5.4xlarge': 1.536, 'm5.8xlarge': 3.072,
                'm5.12xlarge': 4.608, 'm5.16xlarge': 6.144, 'r5.xlarge': 0.504, 'r5.2xlarge': 1.008,
                'r5.4xlarge': 2.016, 'r5.8xlarge': 4.032, 'r5.12xlarge': 6.048, 'r5.16xlarge': 8.064
            },
            'ec2_sql_web': {
                'm5.xlarge': 0.432, 'm5.2xlarge': 0.864, 'm5.4xlarge': 1.728, 'm5.8xlarge': 3.456,
                'm5.12xlarge': 5.184, 'm5.16xlarge': 6.912, 'r5.xlarge': 0.552, 'r5.2xlarge': 1.104,
                'r5.4xlarge': 2.208, 'r5.8xlarge': 4.416, 'r5.12xlarge': 6.624, 'r5.16xlarge': 8.832
            },
            'ec2_sql_standard': {
                'm5.xlarge': 0.768, 'm5.2xlarge': 1.536, 'm5.4xlarge': 3.072, 'm5.8xlarge': 6.144,
                'm5.12xlarge': 9.216, 'm5.16xlarge': 12.288, 'r5.xlarge': 1.008, 'r5.2xlarge': 2.016,
                'r5.4xlarge': 4.032, 'r5.8xlarge': 8.064, 'r5.12xlarge': 12.096, 'r5.16xlarge': 16.128
            },
            'ec2_sql_enterprise': {
                'm5.xlarge': 1.344, 'm5.2xlarge': 2.688, 'm5.4xlarge': 5.376, 'm5.8xlarge': 10.752,
                'm5.12xlarge': 16.128, 'm5.16xlarge': 21.504, 'r5.xlarge': 1.584, 'r5.2xlarge': 3.168,
                'r5.4xlarge': 6.336, 'r5.8xlarge': 12.672, 'r5.12xlarge': 19.008, 'r5.16xlarge': 25.344
            },
            'ebs': {'gp3': 0.08, 'gp2': 0.10, 'io2': 0.125, 'io1': 0.125},
            'ssm': {'patch_manager': 0.00972},
            'last_updated': 'Fallback Data (boto3 not available)'
        }
    
    try:
        if "aws" not in st.secrets:
            raise Exception("AWS secrets not configured")
            
        session = boto3.Session(
            aws_access_key_id=st.secrets["aws"]["access_key_id"],
            aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
            region_name=st.secrets["aws"].get("region", "us-east-1")
        )
        
        pricing_client = session.client('pricing', region_name='us-east-1')
        
        def get_ec2_pricing(sql_edition=None):
            filters = [
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Windows'},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'US East (N. Virginia)'}
            ]
            
            if sql_edition:
                filters.append({'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': f'SQL Server {sql_edition}'})
            else:
                filters.append({'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'})
            
            response = pricing_client.get_products(
                ServiceCode='AmazonEC2',
                Filters=filters,
                MaxResults=50
            )
            
            pricing = {}
            for product in response['PriceList']:
                product_data = json.loads(product, parse_float=Decimal)
                instance_type = product_data['product']['attributes'].get('instanceType')
                if instance_type:
                    for price_dimension in product_data['terms']['OnDemand'].values():
                        for price_detail in price_dimension['priceDimensions'].values():
                            price_per_hour = float(price_detail['pricePerUnit']['USD'])
                            pricing[instance_type] = price_per_hour
                            break
                        break
            return pricing
        
        ec2_windows = get_ec2_pricing()
        ec2_sql_web = get_ec2_pricing('Web')
        ec2_sql_standard = get_ec2_pricing('Standard') 
        ec2_sql_enterprise = get_ec2_pricing('Enterprise')
        
        ebs_pricing = {'gp3': 0.08, 'gp2': 0.10, 'io2': 0.125, 'io1': 0.125}
        ssm_pricing = {'patch_manager': 0.00972}
        
        return {
            'ec2_windows': ec2_windows,
            'ec2_sql_web': ec2_sql_web,
            'ec2_sql_standard': ec2_sql_standard,
            'ec2_sql_enterprise': ec2_sql_enterprise,
            'ebs': ebs_pricing,
            'ssm': ssm_pricing,
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return get_aws_pricing()  # Return fallback data

# Load AWS pricing
pricing_data = get_aws_pricing()

# Initialize comprehensive enterprise state
def initialize_enterprise_state():
    # Dynamic Configuration Parameters
    if 'config_params' not in st.session_state:
        st.session_state.config_params = {
            # Workforce parameters (practical enterprise ratios)
            'dba_ratio': 25,  # clusters per DBA (realistic for enterprise)
            'automation_ratio': 35,  # clusters per automation engineer
            'itil_ratio': 60,  # clusters per ITIL manager
            'max_automation_maturity': 65,  # realistic max automation level
            'max_workforce_reduction': 65,  # max workforce reduction at full automation
            'support_24x7_multiplier': 1.4,
            
            # Benchmarks
            'benchmark_availability_avg': 99.5,
            'benchmark_availability_leader': 99.99,
            'benchmark_automation_avg': 45,
            'benchmark_automation_leader': 85,
            'benchmark_itil_avg': 60,
            'benchmark_itil_leader': 90,
            'benchmark_rto_avg': 240,
            'benchmark_rto_leader': 60
        }
    
    if 'current_skills' not in st.session_state:
        st.session_state.current_skills = {
            'SQL Server DBA Expert': 3, 
            'Infrastructure Automation': 1,
            'ITIL Service Manager': 2
        }
    
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
    
    if 'governance_framework' not in st.session_state:
        st.session_state.governance_framework = {
            'change_approval_board': False,
            'architecture_review_board': False,
            'risk_management_committee': False,
            'security_steering_committee': False,
            'business_continuity_plan': False
        }

initialize_enterprise_state()

# Enhanced automation components (COMPLETE list with workforce focus)
if 'automation_components' not in st.session_state:
    st.session_state.automation_components = {
        # Infrastructure & Cloud (Enhanced)
        'Infrastructure as Code': {
            'enabled': False, 'weight': 8, 'effort': 150, 'category': 'Infrastructure',
            'description': 'Terraform for VPC, subnets, security groups, EC2 instances',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'workforce_reduction': 25
        },
        'Multi-AZ High Availability': {
            'enabled': False, 'weight': 9, 'effort': 120, 'category': 'Infrastructure',
            'description': 'Automated failover across availability zones',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'workforce_reduction': 15
        },
        'Auto Scaling & Load Balancing': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Infrastructure',
            'description': 'Dynamic resource scaling based on demand',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'workforce_reduction': 30
        },
        'Network Security Automation': {
            'enabled': False, 'weight': 8, 'effort': 90, 'category': 'Infrastructure',
            'description': 'Automated security group and NACLs management',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'workforce_reduction': 20
        },
        
        # Database & Performance (Enhanced)
        'SQL AlwaysOn Automation': {
            'enabled': False, 'weight': 10, 'effort': 200, 'category': 'Database',
            'description': 'Automated SQL Server AlwaysOn configuration and management',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'workforce_reduction': 35
        },
        'Performance Optimization Engine': {
            'enabled': False, 'weight': 6, 'effort': 120, 'category': 'Database',
            'description': 'AI-driven query optimization and index management',
            'business_impact': 'Medium', 'technical_complexity': 'High', 'workforce_reduction': 25
        },
        'Database Lifecycle Management': {
            'enabled': False, 'weight': 7, 'effort': 150, 'category': 'Database',
            'description': 'Automated provisioning, scaling, and decommissioning',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'workforce_reduction': 30
        },
        
        # Security & Compliance (Enhanced)
        'Zero-Trust Security Model': {
            'enabled': False, 'weight': 9, 'effort': 180, 'category': 'Security',
            'description': 'Identity-based access controls with continuous verification',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'workforce_reduction': 15
        },
        'Automated Patch Management': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Security',
            'description': 'Orchestrated patching with rollback capabilities',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'workforce_reduction': 40
        },
        'Compliance Monitoring': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Security',
            'description': 'Continuous compliance validation and reporting',
            'business_impact': 'Critical', 'technical_complexity': 'Medium', 'workforce_reduction': 20
        },
        'Data Loss Prevention': {
            'enabled': False, 'weight': 8, 'effort': 120, 'category': 'Security',
            'description': 'Automated data classification and protection',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'workforce_reduction': 18
        },
        
        # Operations & Monitoring (Enhanced)
        'AI-Powered Monitoring': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Operations',
            'description': 'Machine learning-based anomaly detection and prediction',
            'business_impact': 'High', 'technical_complexity': 'High', 'workforce_reduction': 45
        },
        'Automated Incident Response': {
            'enabled': False, 'weight': 9, 'effort': 160, 'category': 'Operations',
            'description': 'Self-healing systems with escalation workflows',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'workforce_reduction': 50
        },
        'Service Orchestration': {
            'enabled': False, 'weight': 6, 'effort': 100, 'category': 'Operations',
            'description': 'Workflow automation across enterprise systems',
            'business_impact': 'Medium', 'technical_complexity': 'Medium', 'workforce_reduction': 25
        },
        
        # Backup & Recovery (Enhanced)
        'Cross-Region DR Automation': {
            'enabled': False, 'weight': 9, 'effort': 200, 'category': 'Backup',
            'description': 'Automated disaster recovery across geographic regions',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'workforce_reduction': 20
        },
        'Point-in-Time Recovery': {
            'enabled': False, 'weight': 7, 'effort': 120, 'category': 'Backup',
            'description': 'Granular recovery with minimal data loss',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'workforce_reduction': 15
        },
        
        # Governance & Integration
        'Enterprise Service Bus': {
            'enabled': False, 'weight': 6, 'effort': 180, 'category': 'Integration',
            'description': 'API gateway and service mesh integration',
            'business_impact': 'Medium', 'technical_complexity': 'High', 'workforce_reduction': 12
        },
        'Self-Service Portal': {
            'enabled': False, 'weight': 5, 'effort': 150, 'category': 'Portal',
            'description': 'Enterprise portal with RBAC and workflow approval',
            'business_impact': 'Medium', 'technical_complexity': 'Medium', 'workforce_reduction': 35
        }
    }

# Sidebar configuration with dynamic parameters
st.sidebar.header("Configuration Panel")

# Configuration Parameters
st.sidebar.subheader("Dynamic Parameters")
with st.sidebar.expander("Workforce Ratios"):
    st.session_state.config_params['dba_ratio'] = st.number_input("Clusters per DBA", min_value=5, max_value=50, value=st.session_state.config_params['dba_ratio'])
    st.session_state.config_params['automation_ratio'] = st.number_input("Clusters per Automation Engineer", min_value=10, max_value=100, value=st.session_state.config_params['automation_ratio'])
    st.session_state.config_params['itil_ratio'] = st.number_input("Clusters per ITIL Manager", min_value=20, max_value=200, value=st.session_state.config_params['itil_ratio'])

with st.sidebar.expander("Salary Parameters"):
    st.session_state.config_params['dba_salary'] = st.number_input("DBA Annual Salary", min_value=50000, max_value=200000, value=st.session_state.config_params['dba_salary'], step=5000)
    st.session_state.config_params['automation_salary'] = st.number_input("Automation Engineer Salary", min_value=60000, max_value=250000, value=st.session_state.config_params['automation_salary'], step=5000)
    st.session_state.config_params['itil_salary'] = st.number_input("ITIL Manager Salary", min_value=50000, max_value=180000, value=st.session_state.config_params['itil_salary'], step=5000)
    st.session_state.config_params['benefits_percentage'] = st.number_input("Benefits Percentage", min_value=20, max_value=60, value=st.session_state.config_params['benefits_percentage'])

# Deployment Type Selection
st.sidebar.subheader("Architecture Configuration")
deployment_type = st.sidebar.selectbox(
    "Deployment Architecture",
    ["AlwaysOn Cluster", "Standalone SQL Server"],
    help="Select between SQL Server AlwaysOn high availability clusters or standalone instances"
)

# Current State Configuration
st.sidebar.subheader("Current Infrastructure Assessment")
current_clusters = st.sidebar.number_input(
    f"Current {'Clusters' if deployment_type == 'AlwaysOn Cluster' else 'Instances'}", 
    min_value=1, max_value=1000, value=5
)
current_resources = st.sidebar.number_input("Current Team Size", min_value=1, max_value=50, value=6)

# Instance Configuration
st.sidebar.subheader("Compute Configuration")
available_instances = list(set(
    list(pricing_data['ec2_windows'].keys()) + 
    list(pricing_data['ec2_sql_standard'].keys())
))
available_instances.sort()

instance_type = st.sidebar.selectbox(
    "EC2 Instance Type",
    available_instances,
    help="Select EC2 instance type optimized for SQL Server workloads"
)

current_cpu_cores = st.sidebar.number_input("CPU Cores per Instance", min_value=8, max_value=128, value=32)
current_memory_gb = st.sidebar.number_input("Memory (GB) per Instance", min_value=64, max_value=1024, value=256)
current_storage_tb = st.sidebar.number_input("Storage (TB) per Instance", min_value=1, max_value=100, value=10)

if deployment_type == "AlwaysOn Cluster":
    ec2_per_cluster = st.sidebar.number_input("EC2 Instances per Cluster", min_value=2, max_value=10, value=3)
else:
    ec2_per_cluster = 1

# SQL Server Edition
sql_edition = st.sidebar.selectbox(
    "SQL Server Edition",
    ["Standard", "Enterprise", "Web"],
    help="Select SQL Server edition for licensing and cost calculations"
)

# EBS Configuration
st.sidebar.subheader("Storage Configuration")
ebs_volume_type = st.sidebar.selectbox(
    "EBS Volume Type",
    ["gp3", "gp2", "io2", "io1"],
    help="Select Amazon EBS volume type for storage performance requirements"
)

# Patch Management
enable_ssm_patching = st.sidebar.checkbox(
    "AWS Systems Manager Patch Management",
    value=True,
    help="Enable automated patching with AWS Systems Manager for operational efficiency"
)

# Target State Configuration
st.sidebar.subheader("Target State Planning")
target_clusters = st.sidebar.number_input(
    f"Target {'Clusters' if deployment_type == 'AlwaysOn Cluster' else 'Instances'}", 
    min_value=current_clusters, max_value=10000, value=100
)
timeframe = st.sidebar.number_input("Implementation Timeframe (months)", min_value=6, max_value=60, value=24)

# Service Level Requirements
st.sidebar.subheader("Service Level Requirements")
availability_target = st.sidebar.slider("Availability Target (%)", 95.0, 99.99, 99.9, 0.01)
rpo_minutes = st.sidebar.slider("Recovery Point Objective (minutes)", 5, 1440, 60, 5)
rto_minutes = st.sidebar.slider("Recovery Time Objective (minutes)", 15, 1440, 240, 15)

# Support model
support_24x7 = st.sidebar.checkbox("24x7 Global Support Coverage", value=False)

# Skills requirements calculation with realistic automation constraints
def calculate_skills_requirements(clusters, automation_level, support_24x7):
    """Calculate required skills based on realistic enterprise constraints"""
    
    # Ensure config_params has required keys with defaults
    if 'max_automation_maturity' not in st.session_state.config_params:
        st.session_state.config_params['max_automation_maturity'] = 65
    if 'max_workforce_reduction' not in st.session_state.config_params:
        st.session_state.config_params['max_workforce_reduction'] = 65
    
    # Cap automation at realistic maximum (65%)
    effective_automation = min(automation_level, st.session_state.config_params['max_automation_maturity'])
    
    base_requirements = {
        'SQL Server DBA Expert': max(1, math.ceil(clusters / st.session_state.config_params['dba_ratio'])),
        'Infrastructure Automation': max(1, math.ceil(clusters / st.session_state.config_params['automation_ratio'])),
        'ITIL Service Manager': max(1, math.ceil(clusters / st.session_state.config_params['itil_ratio'])),
    }
    
    # Realistic automation impact: linear reduction up to max (65% reduction at 65% automation)
    automation_reduction_factor = (effective_automation / 100) * (st.session_state.config_params['max_workforce_reduction'] / 100)
    workforce_multiplier = 1.0 - automation_reduction_factor
    
    # Support coverage multiplier
    support_multiplier = st.session_state.config_params['support_24x7_multiplier'] if support_24x7 else 1.0
    
    adjusted_requirements = {}
    for role, base_req in base_requirements.items():
        
        # Account for role-specific automation limitations
        if role == 'SQL Server DBA Expert':
            # DBAs have automation constraints due to:
            # - Legacy systems without APIs (35% of operations)
            # - Complex troubleshooting requiring human judgment
            # - Critical decision-making that can't be automated
            role_automation_cap = min(effective_automation, 60)  # DBAs cap at 60% automation
            role_reduction = (role_automation_cap / 100) * 0.50  # Max 50% reduction for DBAs
            role_multiplier = 1.0 - role_reduction
            
        elif role == 'Infrastructure Automation':
            # Automation engineers benefit most from their own tools
            # But still need human oversight for complex scenarios
            role_automation_cap = effective_automation
            role_reduction = (role_automation_cap / 100) * 0.70  # Up to 70% reduction
            role_multiplier = 1.0 - role_reduction
            
        elif role == 'ITIL Service Manager':
            # Service management has some automation potential but requires human coordination
            role_automation_cap = min(effective_automation, 50)  # ITIL caps at 50% automation
            role_reduction = (role_automation_cap / 100) * 0.40  # Max 40% reduction for ITIL
            role_multiplier = 1.0 - role_reduction
        
        else:
            role_multiplier = workforce_multiplier
        
        # Apply both automation and support multipliers
        adjusted_req = math.ceil(base_req * support_multiplier * role_multiplier)
        adjusted_requirements[role] = max(1, adjusted_req) if base_req > 0 else 0
    
    return adjusted_requirements

# Microsoft SQL Server Licensing Calculator (AWS License-Included Model)
def calculate_sql_server_licensing_aws(deployment_type, instance_type, num_instances, edition="Standard"):
    """Calculate SQL Server licensing costs using AWS License-Included pricing"""
    
    edition_key_map = {
        "Web": "ec2_sql_web",
        "Standard": "ec2_sql_standard", 
        "Enterprise": "ec2_sql_enterprise"
    }
    
    edition_key = edition_key_map.get(edition, "ec2_sql_standard")
    windows_rate = pricing_data['ec2_windows'].get(instance_type, 0.384)
    sql_rate = pricing_data[edition_key].get(instance_type, windows_rate * 2)
    
    licensing_hourly_rate = sql_rate - windows_rate
    licensing_monthly_cost = licensing_hourly_rate * 24 * 30
    
    if deployment_type == "AlwaysOn Cluster":
        total_monthly_cost = licensing_monthly_cost * 3 * num_instances
    else:
        total_monthly_cost = licensing_monthly_cost * num_instances
    
    return {
        "monthly_cost": total_monthly_cost,
        "annual_cost": total_monthly_cost * 12,
        "licensing_model": "AWS License-Included", 
        "edition": edition,
        "hourly_rate_per_instance": licensing_hourly_rate,
        "notes": f"Based on AWS {edition} License-Included pricing vs Windows-only pricing"
    }

# Cost calculation functions with dynamic parameters
def calculate_infrastructure_costs(clusters, instance_type, instances_per_cluster, storage_tb, ebs_type, enable_patching, sql_edition):
    """Calculate comprehensive infrastructure costs including SQL Server licensing"""
    
    windows_rate = pricing_data['ec2_windows'].get(instance_type, 0.384)
    
    edition_key_map = {
        "Web": "ec2_sql_web",
        "Standard": "ec2_sql_standard", 
        "Enterprise": "ec2_sql_enterprise"
    }
    edition_key = edition_key_map.get(sql_edition, "ec2_sql_standard")
    sql_windows_rate = pricing_data[edition_key].get(instance_type, windows_rate * 2)
    
    total_instances = clusters * instances_per_cluster
    
    monthly_ec2_cost = sql_windows_rate * 24 * 30 * total_instances
    
    ebs_rate_per_gb = pricing_data['ebs'][ebs_type]
    storage_gb = storage_tb * 1024
    monthly_ebs_cost = ebs_rate_per_gb * storage_gb * total_instances
    
    monthly_ssm_cost = 0
    if enable_patching:
        ssm_hourly_rate = pricing_data['ssm']['patch_manager']
        monthly_ssm_cost = ssm_hourly_rate * 24 * 30 * total_instances
    
    monthly_data_transfer = clusters * 25 if deployment_type == "AlwaysOn Cluster" else clusters * 10
    
    licensing_hourly_rate = sql_windows_rate - windows_rate
    monthly_licensing_cost = licensing_hourly_rate * 24 * 30 * total_instances
    
    return {
        'ec2_compute_monthly': (windows_rate * 24 * 30 * total_instances),
        'sql_licensing_monthly': monthly_licensing_cost,
        'ebs_monthly': monthly_ebs_cost,
        'ssm_monthly': monthly_ssm_cost,
        'data_transfer_monthly': monthly_data_transfer,
        'total_monthly': monthly_ec2_cost + monthly_ebs_cost + monthly_ssm_cost + monthly_data_transfer,
        'total_instances': total_instances
    }

def calculate_workforce_requirements(skills_requirements):
    """Calculate workforce requirements in FTE (Full Time Equivalent) counts"""
    
    total_fte = sum(skills_requirements.values())
    
    return {
        'total_fte': total_fte,
        'breakdown': skills_requirements.copy()
    }

def calculate_total_cost_of_ownership(clusters, automation_level, timeframe_months):
    """Calculate infrastructure TCO and workforce FTE requirements"""
    
    # Infrastructure costs (infrastructure only - no workforce costs)
    infra_costs = calculate_infrastructure_costs(
        clusters, instance_type, ec2_per_cluster, current_storage_tb, 
        ebs_volume_type, enable_ssm_patching, sql_edition
    )
    
    # Workforce requirements (FTE counts, not costs)
    skills_needed = calculate_skills_requirements(clusters, automation_level, support_24x7)
    workforce_requirements = calculate_workforce_requirements(skills_needed)
    
    # Total infrastructure cost over timeframe
    total_infrastructure_cost = infra_costs['total_monthly'] * timeframe_months
    
    return {
        'infrastructure': infra_costs,
        'workforce_requirements': workforce_requirements,
        'skills_required': skills_needed,
        'total_infrastructure_cost': total_infrastructure_cost,
        'tco_breakdown': {
            'EC2 Compute': infra_costs['ec2_compute_monthly'] * timeframe_months,
            'SQL Licensing (AWS)': infra_costs['sql_licensing_monthly'] * timeframe_months,
            'EBS Storage': infra_costs['ebs_monthly'] * timeframe_months,
            'SSM Patching': infra_costs['ssm_monthly'] * timeframe_months,
            'Data Transfer': infra_costs['data_transfer_monthly'] * timeframe_months,
        }
    }

# Calculate comprehensive enterprise metrics
def calculate_enterprise_metrics():
    """Calculate enterprise-grade operational metrics with workforce focus"""
    
    total_weight = sum(comp['weight'] for comp in st.session_state.automation_components.values())
    enabled_weight = sum(comp['weight'] for comp in st.session_state.automation_components.values() if comp['enabled'])
    automation_maturity = (enabled_weight / total_weight) * 100 if total_weight > 0 else 0
    
    # Calculate weighted workforce reduction potential
    enabled_components = [comp for comp in st.session_state.automation_components.values() if comp['enabled']]
    if enabled_components:
        total_weight_enabled = sum(comp['weight'] for comp in enabled_components)
        weighted_workforce_reduction = sum(
            comp['workforce_reduction'] * (comp['weight'] / total_weight_enabled) 
            for comp in enabled_components
        )
    else:
        weighted_workforce_reduction = 0
    
    current_ec2_instances = current_clusters * ec2_per_cluster
    target_ec2_instances = target_clusters * ec2_per_cluster
    scale_factor = target_clusters / current_clusters
    
    itil_implemented = sum(1 for practice in st.session_state.itil_practices.values() if practice['implemented'])
    itil_total = len(st.session_state.itil_practices)
    itil_maturity = (itil_implemented / itil_total * 100) if itil_total > 0 else 0
    
    required_skills = calculate_skills_requirements(target_clusters, automation_maturity, support_24x7)
    total_skill_gap = sum(
        max(0, required_skills[role] - st.session_state.current_skills.get(role, 0))
        for role in required_skills.keys()
    )
    
    critical_components = sum(
        1 for comp in st.session_state.automation_components.values()
        if comp['enabled'] and comp['business_impact'] == 'Critical'
    )
    
    high_complexity_enabled = sum(
        1 for comp in st.session_state.automation_components.values()
        if comp['enabled'] and comp['technical_complexity'] == 'High'
    )
    
    # Risk assessment based on enterprise factors
    risks = []
    
    if not st.session_state.automation_components['Zero-Trust Security Model']['enabled']:
        risks.append({
            'category': 'Security',
            'risk': 'Inadequate security model for enterprise scale',
            'severity': 'Critical',
            'impact': 'Data breaches, unauthorized access, security incidents'
        })
    
    if not st.session_state.automation_components['AI-Powered Monitoring']['enabled'] and target_clusters > 50:
        risks.append({
            'category': 'Operations',
            'risk': 'Manual monitoring at enterprise scale',
            'severity': 'High',
            'impact': 'Delayed incident detection, performance degradation'
        })
    
    if total_skill_gap > 5:
        risks.append({
            'category': 'Workforce',
            'risk': 'Critical skills gap for enterprise operations',
            'severity': 'High',
            'impact': 'Operational failures, knowledge dependencies, staff burnout'
        })
    
    if not st.session_state.automation_components['Cross-Region DR Automation']['enabled']:
        risks.append({
            'category': 'Business Continuity',
            'risk': 'Manual disaster recovery procedures',
            'severity': 'Critical',
            'impact': 'Extended downtime, data loss, business disruption'
        })
    
    return {
        'automation_maturity': automation_maturity,
        'workforce_reduction_potential': weighted_workforce_reduction,
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

# Calculate current and target scenarios
current_tco = calculate_total_cost_of_ownership(current_clusters, metrics['automation_maturity'], timeframe)
target_tco = calculate_total_cost_of_ownership(target_clusters, metrics['automation_maturity'], timeframe)

# Executive Dashboard with Cost Metrics
st.markdown('<div class="section-header">Executive Dashboard & Financial Analysis</div>', unsafe_allow_html=True)

# Cost summary section
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="cost-summary">
        <h3>Infrastructure Cost Analysis</h3>
        <h2>${target_tco['total_infrastructure_cost']:,.0f}</h2>
        <p>{timeframe}-month infrastructure projection</p>
        <p>{target_clusters} {deployment_type.lower()}s | {target_tco['infrastructure']['total_instances']} instances</p>
        <p>Monthly Infrastructure: ${target_tco['infrastructure']['total_monthly']:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Calculate workforce savings through automation
    baseline_automation = 0  # No automation scenario
    baseline_tco = calculate_total_cost_of_ownership(target_clusters, baseline_automation, timeframe)
    fte_reduction = baseline_tco['workforce_requirements']['total_fte'] - target_tco['workforce_requirements']['total_fte']
    
    st.markdown(f"""
    <div class="savings-highlight">
        <h3>Workforce Optimization Analysis</h3>
        <h2>{target_tco['workforce_requirements']['total_fte']} FTE</h2>
        <p>Required workforce with {metrics['automation_maturity']:.0f}% automation</p>
        <p>Baseline (no automation): {baseline_tco['workforce_requirements']['total_fte']} FTE</p>
        <p>FTE Reduction: {fte_reduction} positions</p>
    </div>
    """, unsafe_allow_html=True)

# Executive metrics row
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="operational-metrics">
        <h4>Automation Maturity</h4>
        <h3>{metrics['automation_maturity']:.0f}%</h3>
        <p>Framework Coverage</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="operational-metrics">
        <h4>ITIL Compliance</h4>
        <h3>{metrics['itil_maturity']:.0f}%</h3>
        <p>Practice Implementation</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    availability_status = "Tier 4" if availability_target >= 99.99 else "Tier 3" if availability_target >= 99.9 else "Tier 2"
    st.metric("Service Availability", f"{availability_target}%", delta=availability_status)

with col4:
    st.metric("Infrastructure Scale Factor", f"{metrics['scale_factor']:.1f}x")

with col5:
    st.metric("Resource Requirements Gap", f"{metrics['total_skill_gap']} positions")

with col6:
    st.metric("Total Compute Instances", f"{metrics['target_ec2_instances']}")

# Skills & Workforce Planning
st.markdown('<div class="section-header">Workforce Planning & Resource Requirements</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="executive-summary">
<h4>Strategic Workforce Analysis</h4>
<p><strong>Infrastructure Scale:</strong> {target_clusters} {deployment_type.lower()}s planned over {timeframe} months</p>
<p><strong>Automation Impact:</strong> {metrics['automation_maturity']:.0f}% automation maturity reduces workforce requirements through operational efficiency</p>
<p><strong>Service Coverage:</strong> {'Continuous operations (24x7)' if support_24x7 else 'Standard business hours'} support model</p>
<p><strong>Focus Areas:</strong> Core operational roles for SQL Server administration and infrastructure management</p>
</div>
""", unsafe_allow_html=True)

# Current staffing input section
st.markdown('<div class="subsection-header">Current Resource Allocation</div>', unsafe_allow_html=True)
st.write("Configure current staffing levels for operational assessment:")

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
st.markdown('<div class="subsection-header">Resource Gap Analysis</div>', unsafe_allow_html=True)

required_skills = calculate_skills_requirements(target_clusters, metrics['automation_maturity'], support_24x7)

skills_certifications = {
    'SQL Server DBA Expert': 'Microsoft Certified: Azure Database Administrator', 
    'Infrastructure Automation': 'Terraform Associate',
    'ITIL Service Manager': 'ITIL 4 Managing Professional'
}

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
        'Status': 'Adequate' if gap == 0 else f'Shortfall: {gap} positions',
        'Certification Required': skills_certifications[role]
    })

skills_df = pd.DataFrame(skills_data)

col1, col2 = st.columns([3, 1])

with col1:
    st.dataframe(skills_df[['Role', 'Current Staff', 'Required for Target', 'Gap', 'Status', 'Certification Required']], use_container_width=True)
    
    with st.expander("Methodology: Resource Requirements Calculation"):
        st.markdown(f"""
        **Corrected Workforce-Centric Calculation Framework:**
        
        1. **Base Resource Requirements by Role:**
           - SQL Server DBA Expert: 1 FTE per {st.session_state.config_params['dba_ratio']} infrastructure clusters
           - Infrastructure Automation: 1 FTE per {st.session_state.config_params['automation_ratio']} infrastructure clusters  
           - ITIL Service Manager: 1 FTE per {st.session_state.config_params['itil_ratio']} infrastructure clusters
        
        2. **Realistic Automation Constraints:**
           - **Maximum Automation Maturity**: {st.session_state.config_params['max_automation_maturity']}% (not 85%)
           - **Enterprise Reality**: 35% of operations lack APIs, require human judgment
           - **Legacy System Constraints**: Cannot fully automate without major re-architecture
           
        3. **Role-Specific Automation Limitations:**
           - **DBA Roles**: Capped at 60% automation (max 50% workforce reduction)
           - **Infrastructure**: Up to 70% workforce reduction possible
           - **ITIL Managers**: Capped at 50% automation (max 40% workforce reduction)
        
        4. **Service Coverage Multiplier:** {st.session_state.config_params['support_24x7_multiplier']}x increase for continuous operations (24x7) coverage
        
        5. **Key Correction from Previous Flawed Logic:**
           - **Old Logic**: 85% automation → only 34% workforce reduction ❌
           - **New Logic**: {st.session_state.config_params['max_automation_maturity']}% automation → up to {st.session_state.config_params['max_workforce_reduction']}% workforce reduction ✅
           - **Reality Check**: Accounts for enterprise constraints and legacy limitations
        
        **Why This Model is More Realistic:**
        - Recognizes automation plateau due to legacy constraints
        - Accounts for human judgment requirements in complex scenarios  
        - Reflects actual enterprise database operation limitations
        - Avoids overly optimistic automation assumptions
        """)

with col2:
    total_current = sum(st.session_state.current_skills.get(role, 0) for role in required_skills.keys())
    total_required = sum(required_skills.values())
    total_gap = sum(max(0, required_skills[role] - st.session_state.current_skills.get(role, 0)) for role in required_skills.keys())
    
    st.metric("Current Workforce", f"{total_current} FTE")
    st.metric("Target Workforce", f"{total_required} FTE")
    st.metric("Resource Gap", f"{total_gap} positions")
    
    if total_required > 0:
        skills_readiness = max(0, 100 - (total_gap / total_required * 100))
        st.metric("Workforce Readiness", f"{skills_readiness:.0f}%")
        
        if skills_readiness >= 90:
            st.success("Workforce adequately prepared")
        elif skills_readiness >= 70:
            st.warning("Minor resource gaps identified")
        else:
            st.error("Significant resource shortfalls")
    
    if metrics['automation_maturity'] > 30:
        st.info(f"Automation framework reduces staffing requirements by approximately {metrics['workforce_reduction_potential']:.0f}%")

# Monthly Forecasting System
st.markdown("---")
st.markdown('<div class="subsection-header">Strategic Resource Planning Forecast</div>', unsafe_allow_html=True)

def calculate_monthly_forecast():
    """Calculate month-by-month scaling forecast with realistic automation constraints"""
    
    # Ensure config_params has required keys with defaults
    if 'max_automation_maturity' not in st.session_state.config_params:
        st.session_state.config_params['max_automation_maturity'] = 65
    
    cluster_growth_per_month = (target_clusters - current_clusters) / timeframe
    automation_start = metrics['automation_maturity']
    
    # Cap automation target at realistic maximum (65%)
    automation_target = min(st.session_state.config_params['max_automation_maturity'], automation_start + 40)
    automation_growth_per_month = (automation_target - automation_start) / timeframe
    
    forecast_data = []
    
    for month in range(timeframe + 1):
        month_clusters = current_clusters + (cluster_growth_per_month * month)
        month_automation = automation_start + (automation_growth_per_month * month)
        
        # Ensure automation doesn't exceed realistic maximum
        month_automation = min(month_automation, st.session_state.config_params['max_automation_maturity'])
        
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
            target_automation_for_hiring = min(target_automation_for_hiring, st.session_state.config_params['max_automation_maturity'])
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
        
        forecast_data.append({
            'month': month,
            'clusters': int(month_clusters),
            'automation_maturity': month_automation,
            'required_skills': month_required_skills,
            'new_hires_needed': new_hires_needed,
            'total_new_hires': total_new_hires,
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
        subplot_titles=('Infrastructure Scale & Team Growth', 'Automation Maturity Progression'),
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Scatter(x=months, y=clusters, name="Infrastructure Clusters", line=dict(color='#1e40af', width=3)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=team_sizes, name="Team Size", line=dict(color='#059669', width=3)),
        row=1, col=1, secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(x=months, y=automation_levels, name="Automation Maturity %", 
                  line=dict(color='#dc2626', width=3), fill='tonexty'),
        row=2, col=1
    )
    
    fig.update_layout(height=500, title_text="Strategic Scaling Forecast Overview")
    fig.update_xaxes(title_text="Implementation Timeline", row=2, col=1)
    fig.update_yaxes(title_text="Infrastructure Clusters", row=1, col=1)
    fig.update_yaxes(title_text="Team Members (FTE)", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Automation Maturity (%)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Key Forecast Metrics")
    
    total_hires_needed = sum(d['total_new_hires'] for d in forecast_data)
    peak_monthly_hires = max(d['total_new_hires'] for d in forecast_data)
    final_team_size = forecast_data[-1]['total_team_size']
    
    st.metric("Total New Positions", f"{total_hires_needed}")
    st.metric("Peak Monthly Hiring", f"{peak_monthly_hires}")
    st.metric("Final Team Size", f"{final_team_size} FTE")
    st.metric("Final Automation Level", f"{forecast_data[-1]['automation_maturity']:.0f}%")
    
    urgent_months = [d for d in forecast_data if d['total_new_hires'] > 2]
    if urgent_months:
        st.warning(f"High-intensity hiring periods: {len(urgent_months)} months require 3+ new hires")
    
    if total_hires_needed > 8:
        st.error("Consider phased implementation approach due to high hiring volume")
    elif total_hires_needed > 4:
        st.warning("Moderate hiring requirements - strategic recruitment planning needed")
    else:
        st.success("Manageable hiring requirements within normal recruitment capacity")

# Detailed monthly breakdown
st.markdown('<div class="subsection-header">Monthly Implementation Roadmap</div>', unsafe_allow_html=True)

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
                month_row[f'{role} Positions'] = data['new_hires_needed'][role]
        
        monthly_breakdown.append(month_row)

breakdown_df = pd.DataFrame(monthly_breakdown)
st.dataframe(breakdown_df, use_container_width=True)

# ITIL 4 Service Management Framework
st.markdown('<div class="section-header">ITIL 4 Service Management Framework</div>', unsafe_allow_html=True)

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
        
        priority_indicator = {
            'Critical': 'HIGH PRIORITY',
            'High': 'MEDIUM PRIORITY', 
            'Medium': 'STANDARD PRIORITY'
        }
        st.caption(f"{priority_indicator[data['priority']]}")
        
        st.session_state.itil_practices[practice]['implemented'] = implemented

# Enhanced Automation Components
st.markdown('<div class="section-header">Enterprise Automation Framework</div>', unsafe_allow_html=True)

categories = {
    'Infrastructure': 'Infrastructure & Cloud Services',
    'Database': 'Database & Performance Management',
    'Security': 'Security & Compliance',
    'Operations': 'Operations & Monitoring',
    'Backup': 'Backup & Recovery',
    'Integration': 'Integration & Connectivity',
    'Portal': 'Self-Service Portal'
}

tabs = st.tabs([f"{cat}" for cat in categories.values()])

for tab, (category, display_name) in zip(tabs, categories.items()):
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
                
                impact_levels = {'Critical': 'CRITICAL', 'High': 'HIGH', 'Medium': 'MEDIUM'}
                complexity_levels = {'High': 'HIGH', 'Medium': 'MEDIUM', 'Low': 'LOW'}
                
                st.caption(f"**Business Impact:** {impact_levels[comp_data['business_impact']]} | "
                          f"**Technical Complexity:** {complexity_levels[comp_data['technical_complexity']]} | "
                          f"**Workforce Reduction:** {comp_data['workforce_reduction']}%")
                
                st.session_state.automation_components[comp_name]['enabled'] = enabled
            
            with col2:
                st.write(f"**Priority Weight:** {comp_data['weight']}%")
                st.write(f"**Implementation Effort:** {comp_data['effort']} hours")
                st.write(f"**Workforce Reduction:** {comp_data['workforce_reduction']}%")
            
            st.markdown("---")

# Enterprise Risk Assessment
st.markdown('<div class="section-header">Enterprise Risk Assessment & Governance</div>', unsafe_allow_html=True)

if metrics['risks']:
    for risk in metrics['risks']:
        severity_class = f"risk-{risk['severity'].lower()}"
        st.markdown(f"""
        <div class="{severity_class}">
            <strong>{risk['category']} Risk - {risk['severity']} Severity: {risk['risk']}</strong><br>
            <em>Business Impact:</em> {risk['impact']}<br>
            <em>Governance Action Required:</em> Implement corresponding automation controls and governance frameworks
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("Enterprise risk profile is well-managed with current automation strategy implementation.")

# Industry Benchmark Comparison
st.markdown('<div class="section-header">Industry Benchmark Assessment</div>', unsafe_allow_html=True)

benchmark_scores = {
    'Database Availability': {
        'our_score': availability_target,
        'industry_avg': st.session_state.config_params['benchmark_availability_avg'],
        'industry_leader': st.session_state.config_params['benchmark_availability_leader'],
        'unit': '%'
    },
    'Automation Maturity': {
        'our_score': metrics['automation_maturity'],
        'industry_avg': st.session_state.config_params['benchmark_automation_avg'],
        'industry_leader': st.session_state.config_params['benchmark_automation_leader'],
        'unit': '%'
    },
    'ITIL Practice Coverage': {
        'our_score': metrics['itil_maturity'],
        'industry_avg': st.session_state.config_params['benchmark_itil_avg'],
        'industry_leader': st.session_state.config_params['benchmark_itil_leader'],
        'unit': '%'
    },
    'Recovery Time Objective': {
        'our_score': rto_minutes,
        'industry_avg': st.session_state.config_params['benchmark_rto_avg'],
        'industry_leader': st.session_state.config_params['benchmark_rto_leader'],
        'unit': 'minutes',
        'lower_is_better': True
    }
}

for metric_name, scores in benchmark_scores.items():
    lower_is_better = scores.get('lower_is_better', False)
    
    if lower_is_better:
        if scores['our_score'] <= scores['industry_leader']:
            benchmark_class = "benchmark-excellent"
            status = "INDUSTRY LEADING"
        elif scores['our_score'] <= scores['industry_avg']:
            benchmark_class = "benchmark-good"
            status = "ABOVE AVERAGE"
        else:
            benchmark_class = "benchmark-needs-improvement"
            status = "IMPROVEMENT REQUIRED"
    else:
        if scores['our_score'] >= scores['industry_leader']:
            benchmark_class = "benchmark-excellent"
            status = "INDUSTRY LEADING"
        elif scores['our_score'] >= scores['industry_avg']:
            benchmark_class = "benchmark-good"
            status = "ABOVE AVERAGE"
        else:
            benchmark_class = "benchmark-needs-improvement"
            status = "IMPROVEMENT REQUIRED"
    
    st.markdown(f"""
    <div class="{benchmark_class}">
        <strong>{metric_name}:</strong> {scores['our_score']}{scores['unit']} | 
        Industry Average: {scores['industry_avg']}{scores['unit']} | 
        Industry Leader: {scores['industry_leader']}{scores['unit']} | 
        <em>Status: {status}</em>
    </div>
    """, unsafe_allow_html=True)

# Enterprise Governance Framework
st.markdown('<div class="section-header">Enterprise Governance Framework</div>', unsafe_allow_html=True)

st.markdown("""
<div class="governance-framework">
    <h4>Governance Bodies & Committee Structure</h4>
    <p>Essential governance structures for enterprise-scale SQL Server operations management:</p>
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
st.metric("Governance Maturity Level", f"{governance_maturity:.0f}%")

# Cost Analysis Sections
st.markdown("---")
st.markdown('<div class="section-header">Comprehensive Cost Analysis</div>', unsafe_allow_html=True)

# Detailed Cost Calculation Breakdown
st.markdown("### Detailed Cost Calculation Methodology")

with st.expander("Infrastructure Cost Calculations", expanded=False):
    st.markdown("#### Infrastructure Components Breakdown")
    
    # Get current pricing for display
    windows_rate = pricing_data['ec2_windows'].get(instance_type, 0.384)
    edition_key_map = {"Web": "ec2_sql_web", "Standard": "ec2_sql_standard", "Enterprise": "ec2_sql_enterprise"}
    edition_key = edition_key_map.get(sql_edition, "ec2_sql_standard")
    sql_rate = pricing_data[edition_key].get(instance_type, windows_rate * 2)
    licensing_rate = sql_rate - windows_rate
    
    total_instances = target_clusters * ec2_per_cluster
    ebs_rate_per_gb = pricing_data['ebs'][ebs_volume_type]
    storage_gb = current_storage_tb * 1024
    
    st.markdown(f"""
    **EC2 Compute & SQL Licensing:**
    - Instance Type: {instance_type}
    - SQL Server Edition: {sql_edition}
    - Windows Base Rate: ${windows_rate:.3f}/hour
    - SQL Server Rate: ${sql_rate:.3f}/hour
    - SQL Licensing Component: ${licensing_rate:.3f}/hour
    - Total Instances: {target_clusters} clusters × {ec2_per_cluster} instances = {total_instances} instances
    - Monthly Compute Cost: ${total_instances} × ${sql_rate:.3f} × 24 × 30 = ${total_instances * sql_rate * 24 * 30:,.0f}
    - **{timeframe}-Month Total**: ${total_instances * sql_rate * 24 * 30 * timeframe:,.0f}
    
    **EBS Storage:**
    - Volume Type: {ebs_volume_type.upper()}
    - Rate: ${ebs_rate_per_gb}/GB/month
    - Storage per Instance: {current_storage_tb} TB = {storage_gb:,.0f} GB
    - Monthly Storage Cost: {total_instances} instances × {storage_gb:,.0f} GB × ${ebs_rate_per_gb} = ${total_instances * storage_gb * ebs_rate_per_gb:,.0f}
    - **{timeframe}-Month Total**: ${total_instances * storage_gb * ebs_rate_per_gb * timeframe:,.0f}
    """)
    
    if enable_ssm_patching:
        ssm_rate = pricing_data['ssm']['patch_manager']
        monthly_ssm = ssm_rate * 24 * 30 * total_instances
        st.markdown(f"""
        **Systems Manager Patching:**
        - Rate: ${ssm_rate:.5f}/instance/hour
        - Monthly Cost: {total_instances} instances × ${ssm_rate:.5f} × 24 × 30 = ${monthly_ssm:,.0f}
        - **{timeframe}-Month Total**: ${monthly_ssm * timeframe:,.0f}
        """)
    
    data_transfer_monthly = target_clusters * (25 if deployment_type == "AlwaysOn Cluster" else 10)
    st.markdown(f"""
    **Data Transfer (estimated):**
    - Rate: ${25 if deployment_type == "AlwaysOn Cluster" else 10}/cluster/month
    - Monthly Cost: {target_clusters} clusters × ${25 if deployment_type == "AlwaysOn Cluster" else 10} = ${data_transfer_monthly:,.0f}
    - **{timeframe}-Month Total**: ${data_transfer_monthly * timeframe:,.0f}
    
    **Infrastructure Grand Total**: ${target_tco['infrastructure']['total_monthly'] * timeframe:,.0f}
    """)

with st.expander("Workforce Requirements Calculations", expanded=False):
    st.markdown("#### Workforce FTE Breakdown (Realistic Automation Constraints)")
    
    # Calculate step by step with new logic
    base_dba = max(1, math.ceil(target_clusters / st.session_state.config_params['dba_ratio']))
    base_automation = max(1, math.ceil(target_clusters / st.session_state.config_params['automation_ratio']))
    base_itil = max(1, math.ceil(target_clusters / st.session_state.config_params['itil_ratio']))
    
    # Apply realistic automation constraints
    effective_automation = min(metrics['automation_maturity'], st.session_state.config_params['max_automation_maturity'])
    support_multiplier = st.session_state.config_params['support_24x7_multiplier'] if support_24x7 else 1.0
    
    # Role-specific automation calculations
    dba_automation_cap = min(effective_automation, 60)
    dba_reduction = (dba_automation_cap / 100) * 0.50
    dba_multiplier = 1.0 - dba_reduction
    
    automation_reduction = (effective_automation / 100) * 0.70
    automation_multiplier = 1.0 - automation_reduction
    
    itil_automation_cap = min(effective_automation, 50)
    itil_reduction = (itil_automation_cap / 100) * 0.40
    itil_multiplier = 1.0 - itil_reduction
    
    final_dba = math.ceil(base_dba * support_multiplier * dba_multiplier)
    final_automation = math.ceil(base_automation * support_multiplier * automation_multiplier)
    final_itil = math.ceil(base_itil * support_multiplier * itil_multiplier)
    
    st.markdown(f"""
    **Base Staffing Requirements:**
    - SQL Server DBA Expert: {target_clusters} clusters ÷ {st.session_state.config_params['dba_ratio']} = {base_dba} FTE
    - Infrastructure Automation: {target_clusters} clusters ÷ {st.session_state.config_params['automation_ratio']} = {base_automation} FTE
    - ITIL Service Manager: {target_clusters} clusters ÷ {st.session_state.config_params['itil_ratio']} = {base_itil} FTE
    - **Base Total**: {base_dba + base_automation + base_itil} FTE
    
    **Realistic Automation Constraints:**
    - Current Automation Maturity: {metrics['automation_maturity']:.1f}%
    - Effective Automation (capped at {st.session_state.config_params['max_automation_maturity']}%): {effective_automation:.1f}%
    - Support Coverage: {'24x7' if support_24x7 else 'Business Hours'} (multiplier: {support_multiplier:.1f}x)
    
    **Role-Specific Automation Impact:**
    - **DBA**: Capped at 60% automation (legacy systems, human judgment needed)
      - Automation impact: {dba_automation_cap:.1f}% × 50% max reduction = {dba_reduction*100:.1f}% reduction
      - Workforce multiplier: {dba_multiplier:.3f}
    - **Infrastructure Automation**: Up to 70% reduction possible
      - Automation impact: {effective_automation:.1f}% × 70% max reduction = {automation_reduction*100:.1f}% reduction  
      - Workforce multiplier: {automation_multiplier:.3f}
    - **ITIL Service Manager**: Capped at 50% automation (coordination requires humans)
      - Automation impact: {itil_automation_cap:.1f}% × 40% max reduction = {itil_reduction*100:.1f}% reduction
      - Workforce multiplier: {itil_multiplier:.3f}
    
    **Final FTE Requirements (Accounting for Constraints):**
    - SQL Server DBA Expert: {base_dba} × {support_multiplier:.1f} × {dba_multiplier:.3f} = **{final_dba} FTE**
    - Infrastructure Automation: {base_automation} × {support_multiplier:.1f} × {automation_multiplier:.3f} = **{final_automation} FTE**
    - ITIL Service Manager: {base_itil} × {support_multiplier:.1f} × {itil_multiplier:.3f} = **{final_itil} FTE**
    
    **Total Required Workforce**: {final_dba + final_automation + final_itil} FTE
    **Workforce Reduction**: {(base_dba + base_automation + base_itil) - (final_dba + final_automation + final_itil)} FTE ({((base_dba + base_automation + base_itil) - (final_dba + final_automation + final_itil))/(base_dba + base_automation + base_itil)*100:.1f}% reduction)
    
    **Enterprise Reality Check:**
    - 35% of operations lack APIs and require manual intervention
    - Complex troubleshooting needs human expertise and judgment
    - Critical decisions cannot be fully automated for risk management
    - Change management and stakeholder communication require human coordination
    """)

    # Compare with unrealistic automation assumptions
    st.markdown("---")
    st.markdown("**Why 85% Automation is Unrealistic:**")
    st.markdown("""
    - **Legacy Constraint**: 35% of database operations lack modern APIs
    - **Human Judgment**: Complex performance issues require expert analysis
    - **Risk Management**: Critical changes need human approval and oversight
    - **Organizational Change**: Moving from 30% to 85% automation requires years of transformation
    """)
    
    if effective_automation < metrics['automation_maturity']:
        st.warning(f"Automation maturity capped at {st.session_state.config_params['max_automation_maturity']}% due to enterprise constraints")with st.expander("Total Cost of Ownership Formula", expanded=False):
    st.markdown(f"""
    **TCO Calculation Summary:**
    
    **Infrastructure Costs** = EC2 + EBS + SSM + Data Transfer
    - Static costs based on cluster/instance count
    - Not affected by automation (infrastructure needed regardless)
    - **{timeframe}-Month Total**: ${target_tco['infrastructure']['total_monthly'] * timeframe:,.0f}
    
    **Workforce Costs** = (Base Staff × Support Multiplier × Automation Multiplier) × (Salary + Benefits)
    - Reduced by automation maturity
    - Affected by 24x7 support requirements
    - **{timeframe}-Month Total**: ${target_tco['workforce']['annual_cost'] * (timeframe / 12):,.0f}
    
    **Total Cost of Ownership** = Infrastructure + Workforce
    **Grand Total**: ${target_tco['total_tco']:,.0f}
    
    **Cost Distribution:**
    - Infrastructure: {(target_tco['infrastructure']['total_monthly'] * timeframe / target_tco['total_tco'] * 100):.1f}%
    - Workforce: {(target_tco['workforce']['annual_cost'] * (timeframe / 12) / target_tco['total_tco'] * 100):.1f}%
    """)

# TCO Breakdown Chart
fig_tco = go.Figure(data=[
    go.Bar(
        name='Cost Components',
        x=list(target_tco['tco_breakdown'].keys()),
        y=list(target_tco['tco_breakdown'].values()),
        marker_color=['#1e40af', '#dc2626', '#059669', '#f59e0b', '#7c3aed', '#be123c']
    )
])

fig_tco.update_layout(
    title=f"Total Cost of Ownership Analysis - {timeframe} Month Projection",
    xaxis_title="Cost Components",
    yaxis_title="Total Cost (USD)",
    height=400,
    font=dict(family="Arial, sans-serif", size=12),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_tco, use_container_width=True)

# Workforce vs Infrastructure Cost Analysis
st.markdown("### Workforce vs Infrastructure Cost Breakdown")

workforce_pct = (target_tco['tco_breakdown']['Workforce'] / target_tco['total_tco']) * 100
infrastructure_pct = 100 - workforce_pct

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Workforce Cost %", f"{workforce_pct:.1f}%")
    st.metric("Infrastructure Cost %", f"{infrastructure_pct:.1f}%")

with col2:
    st.metric("Annual Workforce Cost", f"${target_tco['workforce']['annual_cost']:,.0f}")
    infrastructure_annual = (target_tco['infrastructure']['total_monthly'] * 12)
    st.metric("Annual Infrastructure Cost", f"${infrastructure_annual:,.0f}")

with col3:
    if workforce_pct > 60:
        st.warning("Workforce costs dominate - automation opportunity")
    elif workforce_pct > 40:
        st.info("Balanced cost structure")
    else:
        st.success("Infrastructure-dominated costs - typical for mature automation")

# SQL Server Licensing Analysis (AWS License-Included Model)
st.markdown("### SQL Server License-Included Analysis")

aws_licensing_info = calculate_sql_server_licensing_aws(deployment_type, instance_type, target_clusters, sql_edition)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="licensing-framework">
        <h4>AWS Licensing Summary</h4>
        <p><strong>Edition:</strong> SQL Server {aws_licensing_info['edition']}</p>
        <p><strong>Model:</strong> {aws_licensing_info['licensing_model']}</p>
        <p><strong>Hourly Rate:</strong> ${aws_licensing_info['hourly_rate_per_instance']:.3f}/instance</p>
        <p><strong>Deployment:</strong> {deployment_type}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("Monthly Licensing", f"${aws_licensing_info['monthly_cost']:,.0f}")
    st.metric("Annual Licensing", f"${aws_licensing_info['annual_cost']:,.0f}")

with col3:
    if deployment_type == "AlwaysOn Cluster":
        st.info("AWS License-Included pricing automatically covers all nodes in AlwaysOn clusters. No separate licensing calculation needed.")
    else:
        st.info("AWS License-Included pricing simplifies licensing - no core counting or CAL management required.")
    
    st.caption(f"**Pricing Model:** {aws_licensing_info['notes']}")

# ROI Analysis (Updated with workforce focus)
st.markdown("### Return on Investment Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Workforce Savings", f"${workforce_savings:,.0f}")
    st.metric("Automation Maturity", f"{metrics['automation_maturity']:.0f}%")
    st.caption(f"Potential workforce reduction: {metrics['workforce_reduction_potential']:.1f}%")

with col2:
    if workforce_savings > 0:
        roi_percentage = (workforce_savings / target_tco['total_tco'] * 100)
        st.metric("Workforce ROI", f"{roi_percentage:.1f}%")
        
        annual_savings = workforce_savings / (timeframe / 12)
        st.metric("Annual Workforce Savings", f"${annual_savings:,.0f}")

with col3:
    workforce_reduction_pct = ((sum(baseline_tco['skills_required'].values()) - sum(target_tco['skills_required'].values())) / sum(baseline_tco['skills_required'].values()) * 100) if sum(baseline_tco['skills_required'].values()) > 0 else 0
    st.metric("Workforce Reduction", f"{workforce_reduction_pct:.0f}%")
    
    if workforce_reduction_pct > 25:
        st.success("Significant workforce optimization achieved")
    elif workforce_reduction_pct > 10:
        st.info("Moderate workforce optimization")
    else:
        st.warning("Limited workforce impact - consider additional automation")

# Executive Summary & Recommendations
st.subheader("Executive Summary & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Current Maturity Assessment")
    st.write(f"**Automation Maturity:** {metrics['automation_maturity']:.0f}% ({'Advanced' if metrics['automation_maturity'] >= 70 else 'Developing' if metrics['automation_maturity'] >= 40 else 'Initial'})")
    st.write(f"**ITIL Practice Coverage:** {metrics['itil_maturity']:.0f}% ({'Mature' if metrics['itil_maturity'] >= 70 else 'Developing'})")
    st.write(f"**Governance Framework:** {governance_maturity:.0f}% ({'Established' if governance_maturity >= 70 else 'Needs Development'})")
    st.write(f"**Total TCO:** ${target_tco['total_tco']:,.0f} over {timeframe} months")

with col2:
    st.markdown("### Strategic Recommendations")
    
    recommendations = []
    
    if metrics['automation_maturity'] < 60:
        recommendations.append("Prioritize automation components with high workforce reduction impact")
    
    if metrics['total_skill_gap'] > 3:
        recommendations.append("Develop comprehensive skills development program")
    
    if metrics['itil_maturity'] < 70:
        recommendations.append("Establish ITIL 4 service management practices")
    
    if governance_maturity < 70:
        recommendations.append("Implement enterprise governance framework")
    
    if workforce_pct > 60:
        recommendations.append("Focus on workforce automation - labor costs dominate TCO")
    
    if not recommendations:
        recommendations.append("Continue execution of current strategy")
        recommendations.append("Focus on operational excellence and continuous improvement")
    
    for rec in recommendations:
        st.write(f"• {rec}")

# Action items
st.markdown("---")
st.markdown("### Immediate Action Items")

action_items = []

immediate_hires = [d for d in forecast_data[:3] if d['total_new_hires'] > 0]
if immediate_hires:
    action_items.append(f"Start recruitment for {immediate_hires[0]['total_new_hires']} positions in next 3 months")

if metrics['automation_maturity'] < 50:
    action_items.append("Develop automation training program for existing team")

if current_clusters < 20 and target_clusters > 50:
    action_items.append("Begin infrastructure automation setup to support scaling")

if total_hires_needed > 5:
    action_items.append("Establish structured onboarding and mentorship program")

action_items.append("Evaluate Reserved Instance pricing for long-term cost optimization")
action_items.append("Establish monthly cost monitoring and optimization reviews")
action_items.append("Configure dynamic parameters based on organizational standards")

for i, item in enumerate(action_items, 1):
    st.write(f"{i}. {item}")

# Certification Status
st.markdown("---")
st.markdown("### Enterprise Certification Status")

if (metrics['automation_maturity'] >= 70 and 
    metrics['itil_maturity'] >= 70 and 
    governance_maturity >= 70):
    st.success("**ENTERPRISE GRADE CERTIFIED** - This solution meets industry benchmark standards for enterprise SQL Server scaling")
elif (metrics['automation_maturity'] >= 50):
    st.warning("**ENTERPRISE READY** - Solution has strong foundation, recommended improvements identified")
else:
    st.error("**DEVELOPMENT REQUIRED** - Significant gaps exist, not yet enterprise-grade")

# Configuration note
st.markdown("---")
st.markdown(f"""
### Configuration & Setup

**Current Status:**
- **AWS Real-time Pricing:** {'Available' if BOTO3_AVAILABLE else 'Unavailable (boto3 not installed)'}
- **Pricing Data Source:** {pricing_data['last_updated']}
- **Dynamic Parameters:** All workforce ratios, salaries, and benchmarks are configurable

#### Key Features:
1. **Workforce-Centric Cost Model:** Automation primarily reduces labor costs, not infrastructure costs
2. **Dynamic Configuration:** No hardcoded financial values - all parameters configurable via sidebar
3. **Industry Benchmarks:** Customizable benchmark comparisons
4. **Real-time Calculations:** All metrics update dynamically as parameters change

#### To Enable Real-Time AWS Pricing:
1. Install boto3: `pip install boto3`
2. Add AWS credentials to Streamlit secrets
3. Required permissions: `pricing:GetProducts`, `pricing:DescribeServices`

#### Dependencies:
- `boto3` - AWS real-time pricing (optional)
- `plotly` - Interactive visualizations
- `pandas` - Data analysis
- `numpy` - Numerical calculations
""")

# Footer
st.markdown("---")
st.markdown("*Enterprise SQL AlwaysOn AWS EC2 Scaling Planner v5.0 - Workforce-Centric TCO | Dynamic Parameters | Real-Time Pricing | Enterprise Governance*")