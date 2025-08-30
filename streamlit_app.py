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
    page_title="Enterprise SQL AlwaysOn Scaling Planner with Cost Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
Strategic Planning | Total Cost of Ownership Analysis | Infrastructure Automation | Service Management Framework | Governance & Compliance
</div>
''', unsafe_allow_html=True)

# Show AWS integration status
if not BOTO3_AVAILABLE:
    st.info("Real-time AWS pricing integration unavailable. Using representative pricing data. To enable live pricing updates, install boto3 package and configure AWS credentials.")

# AWS Pricing API Integration
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_aws_pricing():
    """Fetch real-time AWS pricing including SQL Server License-Included costs"""
    
    # Return fallback data if boto3 is not available
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
        # Check if AWS secrets are available
        if "aws" not in st.secrets:
            raise Exception("AWS secrets not configured")
            
        # Initialize AWS client using Streamlit secrets
        session = boto3.Session(
            aws_access_key_id=st.secrets["aws"]["access_key_id"],
            aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
            region_name=st.secrets["aws"].get("region", "us-east-1")
        )
        
        pricing_client = session.client('pricing', region_name='us-east-1')
        
        def get_ec2_pricing(sql_edition=None):
            """Get EC2 pricing for specific SQL Server edition"""
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
                    # Extract on-demand pricing
                    for price_dimension in product_data['terms']['OnDemand'].values():
                        for price_detail in price_dimension['priceDimensions'].values():
                            price_per_hour = float(price_detail['pricePerUnit']['USD'])
                            pricing[instance_type] = price_per_hour
                            break
                        break
            return pricing
        
        # Get pricing for different SQL Server editions
        ec2_windows = get_ec2_pricing()  # Windows only
        ec2_sql_web = get_ec2_pricing('Web')
        ec2_sql_standard = get_ec2_pricing('Standard') 
        ec2_sql_enterprise = get_ec2_pricing('Enterprise')
        
        # EBS and SSM pricing (simplified - can be enhanced with API calls)
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
        # Fallback pricing if API call fails or credentials not available
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
            'last_updated': 'Fallback Data'
        }

# Microsoft SQL Server Licensing Calculator (AWS License-Included Model)
def calculate_sql_server_licensing_aws(deployment_type, instance_type, num_instances, edition="Standard"):
    """Calculate SQL Server licensing costs using AWS License-Included pricing"""
    
    # Get appropriate pricing based on edition
    edition_key_map = {
        "Web": "ec2_sql_web",
        "Standard": "ec2_sql_standard", 
        "Enterprise": "ec2_sql_enterprise"
    }
    
    edition_key = edition_key_map.get(edition, "ec2_sql_standard")
    windows_rate = pricing_data['ec2_windows'].get(instance_type, 0.384)  # Fallback to m5.xlarge Windows rate
    sql_rate = pricing_data[edition_key].get(instance_type, windows_rate * 2)  # Fallback with 2x multiplier
    
    # Calculate the licensing component (SQL Server price - Windows price)
    licensing_hourly_rate = sql_rate - windows_rate
    licensing_monthly_cost = licensing_hourly_rate * 24 * 30
    
    if deployment_type == "AlwaysOn Cluster":
        # AlwaysOn requires licensing all nodes in the cluster (typically 3 nodes)
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

# Load AWS pricing
pricing_data = get_aws_pricing()

# Global certification mapping
skills_certifications = {
    'SQL Server DBA Expert': 'Microsoft Certified: Azure Database Administrator', 
    'Infrastructure Automation': 'Terraform Associate',
    'ITIL Service Manager': 'ITIL 4 Managing Professional'
}

# Global skills requirements calculation function  
def calculate_skills_requirements(clusters, automation_level, support_24x7):
    """Calculate required skills based on scaling parameters"""
    
    base_requirements = {
        'SQL Server DBA Expert': max(2, math.ceil(clusters / 15)),
        'Infrastructure Automation': max(1, math.ceil(clusters / 30)),
        'ITIL Service Manager': max(1, math.ceil(clusters / 50)),
    }
    
    automation_multiplier = 1.0 - (automation_level / 100 * 0.3)
    support_multiplier = 1.4 if support_24x7 else 1.0
    
    adjusted_requirements = {}
    for role, base_req in base_requirements.items():
        if role in ['SQL Server DBA Expert', 'ITIL Service Manager']:
            adjusted_req = math.ceil(base_req * support_multiplier * max(0.7, automation_multiplier))
        else:
            adjusted_req = math.ceil(base_req * support_multiplier * automation_multiplier)
        
        adjusted_requirements[role] = max(1, adjusted_req) if base_req > 0 else 0
    
    return adjusted_requirements

# Initialize comprehensive enterprise state
def initialize_enterprise_state():
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

# Enhanced automation components (COMPLETE list from original)
if 'automation_components' not in st.session_state:
    st.session_state.automation_components = {
        # Infrastructure & Cloud (Enhanced)
        'Infrastructure as Code': {
            'enabled': False, 'weight': 8, 'effort': 150, 'category': 'Infrastructure',
            'description': 'Terraform for VPC, subnets, security groups, EC2 instances',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'cost_savings': 15
        },
        'Multi-AZ High Availability': {
            'enabled': False, 'weight': 9, 'effort': 120, 'category': 'Infrastructure',
            'description': 'Automated failover across availability zones',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'cost_savings': 5
        },
        'Auto Scaling & Load Balancing': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Infrastructure',
            'description': 'Dynamic resource scaling based on demand',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'cost_savings': 25
        },
        'Network Security Automation': {
            'enabled': False, 'weight': 8, 'effort': 90, 'category': 'Infrastructure',
            'description': 'Automated security group and NACLs management',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'cost_savings': 10
        },
        
        # Database & Performance (Enhanced)
        'SQL AlwaysOn Automation': {
            'enabled': False, 'weight': 10, 'effort': 200, 'category': 'Database',
            'description': 'Automated SQL Server AlwaysOn configuration and management',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'cost_savings': 20
        },
        'Performance Optimization Engine': {
            'enabled': False, 'weight': 6, 'effort': 120, 'category': 'Database',
            'description': 'AI-driven query optimization and index management',
            'business_impact': 'Medium', 'technical_complexity': 'High', 'cost_savings': 15
        },
        'Database Lifecycle Management': {
            'enabled': False, 'weight': 7, 'effort': 150, 'category': 'Database',
            'description': 'Automated provisioning, scaling, and decommissioning',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'cost_savings': 18
        },
        
        # Security & Compliance (Enhanced)
        'Zero-Trust Security Model': {
            'enabled': False, 'weight': 9, 'effort': 180, 'category': 'Security',
            'description': 'Identity-based access controls with continuous verification',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'cost_savings': 8
        },
        'Automated Patch Management': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Security',
            'description': 'Orchestrated patching with rollback capabilities',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'cost_savings': 30
        },
        'Compliance Monitoring': {
            'enabled': False, 'weight': 7, 'effort': 100, 'category': 'Security',
            'description': 'Continuous compliance validation and reporting',
            'business_impact': 'Critical', 'technical_complexity': 'Medium', 'cost_savings': 12
        },
        'Data Loss Prevention': {
            'enabled': False, 'weight': 8, 'effort': 120, 'category': 'Security',
            'description': 'Automated data classification and protection',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'cost_savings': 10
        },
        
        # Operations & Monitoring (Enhanced)
        'AI-Powered Monitoring': {
            'enabled': False, 'weight': 8, 'effort': 140, 'category': 'Operations',
            'description': 'Machine learning-based anomaly detection and prediction',
            'business_impact': 'High', 'technical_complexity': 'High', 'cost_savings': 22
        },
        'Automated Incident Response': {
            'enabled': False, 'weight': 9, 'effort': 160, 'category': 'Operations',
            'description': 'Self-healing systems with escalation workflows',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'cost_savings': 35
        },
        'Service Orchestration': {
            'enabled': False, 'weight': 6, 'effort': 100, 'category': 'Operations',
            'description': 'Workflow automation across enterprise systems',
            'business_impact': 'Medium', 'technical_complexity': 'Medium', 'cost_savings': 15
        },
        
        # Backup & Recovery (Enhanced)
        'Cross-Region DR Automation': {
            'enabled': False, 'weight': 9, 'effort': 200, 'category': 'Backup',
            'description': 'Automated disaster recovery across geographic regions',
            'business_impact': 'Critical', 'technical_complexity': 'High', 'cost_savings': 12
        },
        'Point-in-Time Recovery': {
            'enabled': False, 'weight': 7, 'effort': 120, 'category': 'Backup',
            'description': 'Granular recovery with minimal data loss',
            'business_impact': 'High', 'technical_complexity': 'Medium', 'cost_savings': 8
        },
        
        # Governance & Integration
        'Enterprise Service Bus': {
            'enabled': False, 'weight': 6, 'effort': 180, 'category': 'Integration',
            'description': 'API gateway and service mesh integration',
            'business_impact': 'Medium', 'technical_complexity': 'High', 'cost_savings': 10
        },
        'Self-Service Portal': {
            'enabled': False, 'weight': 5, 'effort': 150, 'category': 'Portal',
            'description': 'Enterprise portal with RBAC and workflow approval',
            'business_impact': 'Medium', 'technical_complexity': 'Medium', 'cost_savings': 20
        }
    }

# Sidebar configuration
st.sidebar.header("Configuration Panel")

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

# Cost calculation functions
def calculate_infrastructure_costs(clusters, instance_type, instances_per_cluster, storage_tb, ebs_type, enable_patching, sql_edition):
    """Calculate comprehensive infrastructure costs including SQL Server licensing"""
    
    # Get pricing rates
    windows_rate = pricing_data['ec2_windows'].get(instance_type, 0.384)
    
    edition_key_map = {
        "Web": "ec2_sql_web",
        "Standard": "ec2_sql_standard", 
        "Enterprise": "ec2_sql_enterprise"
    }
    edition_key = edition_key_map.get(sql_edition, "ec2_sql_standard")
    sql_windows_rate = pricing_data[edition_key].get(instance_type, windows_rate * 2)
    
    total_instances = clusters * instances_per_cluster
    
    # EC2 costs (using SQL Server License-Included pricing)
    monthly_ec2_cost = sql_windows_rate * 24 * 30 * total_instances
    
    # EBS costs
    ebs_rate_per_gb = pricing_data['ebs'][ebs_type]
    storage_gb = storage_tb * 1024
    monthly_ebs_cost = ebs_rate_per_gb * storage_gb * total_instances
    
    # SSM Patch Management costs
    monthly_ssm_cost = 0
    if enable_patching:
        ssm_hourly_rate = pricing_data['ssm']['patch_manager']
        monthly_ssm_cost = ssm_hourly_rate * 24 * 30 * total_instances
    
    # Data transfer costs (estimate based on cluster communication)
    monthly_data_transfer = clusters * 25 if deployment_type == "AlwaysOn Cluster" else clusters * 10
    
    # Calculate SQL licensing component separately for visibility
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

def calculate_total_cost_of_ownership(clusters, timeframe_months, include_staffing=False, custom_monthly_staffing=0):
    """Calculate comprehensive TCO with optional staffing costs"""
    
    # Infrastructure costs (includes SQL licensing via AWS License-Included pricing)
    infra_costs = calculate_infrastructure_costs(
        clusters, instance_type, ec2_per_cluster, current_storage_tb, ebs_volume_type, enable_ssm_patching, sql_edition
    )
    
    # Staffing costs (only if explicitly requested)
    monthly_staffing_cost = custom_monthly_staffing if include_staffing else 0
    
    # Calculate monthly total
    monthly_total = infra_costs['total_monthly'] + monthly_staffing_cost
    
    # Total TCO over timeframe
    total_tco = monthly_total * timeframe_months
    
    return {
        'infrastructure': infra_costs,
        'staffing_monthly': monthly_staffing_cost,
        'monthly_total': monthly_total,
        'total_tco': total_tco,
        'tco_breakdown': {
            'EC2 Compute': infra_costs['ec2_compute_monthly'] * timeframe_months,
            'SQL Licensing (AWS)': infra_costs['sql_licensing_monthly'] * timeframe_months,
            'EBS Storage': infra_costs['ebs_monthly'] * timeframe_months,
            'SSM Patching': infra_costs['ssm_monthly'] * timeframe_months,
            'Data Transfer': infra_costs['data_transfer_monthly'] * timeframe_months,
            'Staffing': monthly_staffing_cost * timeframe_months if include_staffing else 0
        }
    }

# Calculate comprehensive enterprise metrics
def calculate_enterprise_metrics():
    """Calculate enterprise-grade operational metrics"""
    
    total_weight = sum(comp['weight'] for comp in st.session_state.automation_components.values())
    enabled_weight = sum(comp['weight'] for comp in st.session_state.automation_components.values() if comp['enabled'])
    automation_maturity = (enabled_weight / total_weight) * 100 if total_weight > 0 else 0
    
    total_cost_savings = sum(
        comp['cost_savings'] for comp in st.session_state.automation_components.values() 
        if comp['enabled']
    ) / len([c for c in st.session_state.automation_components.values() if c['enabled']]) if any(comp['enabled'] for comp in st.session_state.automation_components.values()) else 0
    
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
        'cost_savings_percentage': total_cost_savings,
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

# Cost calculations
current_tco = calculate_total_cost_of_ownership(current_clusters, timeframe)
target_tco = calculate_total_cost_of_ownership(target_clusters, timeframe)

# Executive Dashboard with Cost Metrics
st.markdown('<div class="section-header">Executive Dashboard & Financial Analysis</div>', unsafe_allow_html=True)

# Cost summary section
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="cost-summary">
        <h3>Total Cost of Ownership Analysis</h3>
        <h2>${target_tco['total_tco']:,.0f}</h2>
        <p>{timeframe}-month projection | {target_clusters} {deployment_type.lower()}s</p>
        <p>Monthly Operating Cost: ${target_tco['monthly_total']:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    potential_savings = target_tco['total_tco'] * (metrics['cost_savings_percentage'] / 100)
    optimized_tco = target_tco['total_tco'] - potential_savings
    st.markdown(f"""
    <div class="savings-highlight">
        <h3>Automation Optimization Potential</h3>
        <h2>${potential_savings:,.0f}</h2>
        <p>{metrics['cost_savings_percentage']:.1f}% cost reduction through automation</p>
        <p>Optimized TCO: ${optimized_tco:,.0f}</p>
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
<p><strong>Automation Impact:</strong> {metrics['automation_maturity']:.0f}% automation maturity reduces workforce requirements by up to 30%</p>
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
    st.dataframe(skills_df[['Role', 'Current Staff', 'Required for Target', 'Gap', 'Status', 'Certification Required']], width='stretch')
    
    with st.expander("Methodology: Resource Requirements Calculation"):
        st.markdown("""
        **Calculation Framework (Operations-Focused):**
        
        1. **Base Resource Requirements by Role:**
           - SQL Server DBA Expert: 1 FTE per 15 infrastructure clusters
           - Infrastructure Automation: 1 FTE per 30 infrastructure clusters  
           - ITIL Service Manager: 1 FTE per 50 infrastructure clusters
        
        2. **Automation Efficiency Factor:** Up to 30% reduction in staffing requirements with mature automation
        
        3. **Service Coverage Multiplier:** 40% increase for continuous operations (24x7) coverage
        
        4. **Role-Specific Adjustments:** Infrastructure automation roles benefit more from technology adoption than administrative and service management roles
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
        st.info(f"Automation framework reduces staffing requirements by approximately {metrics['automation_maturity']/100*30:.0f}%")

# Monthly Forecasting System
st.markdown("---")
st.markdown('<div class="subsection-header">Strategic Resource Planning Forecast</div>', unsafe_allow_html=True)

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
st.dataframe(breakdown_df, width='stretch')

# Hiring recommendations
st.markdown('<div class="subsection-header">Strategic Hiring Recommendations</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Priority 1: SQL Server DBA Expertise")
    dba_hires = sum(d['new_hires_needed'].get('SQL Server DBA Expert', 0) for d in forecast_data)
    st.write(f"**Total positions needed:** {dba_hires}")
    st.write("**Recommended timeline:** Immediate commencement")
    st.write("**Typical lead time:** 2-3 months")
    st.write("**Focus competencies:** SQL Server AlwaysOn architecture")

with col2:
    st.markdown("#### Priority 2: Infrastructure Automation")
    infra_hires = sum(d['new_hires_needed'].get('Infrastructure Automation', 0) for d in forecast_data)
    st.write(f"**Total positions needed:** {infra_hires}")
    st.write("**Recommended timeline:** Month 2-3")
    st.write("**Typical lead time:** 1-2 months")
    st.write("**Focus competencies:** Terraform, AWS automation")

with col3:
    st.markdown("#### Priority 3: ITIL Service Management")
    itil_hires = sum(d['new_hires_needed'].get('ITIL Service Manager', 0) for d in forecast_data)
    st.write(f"**Total positions needed:** {itil_hires}")
    st.write("**Recommended timeline:** Month 4-6")
    st.write("**Typical lead time:** 1-2 months") 
    st.write("**Focus competencies:** Service operations, incident management")

# Risk assessment for hiring plan
st.markdown("---")
st.markdown('<div class="subsection-header">Hiring Plan Risk Assessment</div>', unsafe_allow_html=True)

hiring_risks = []

if total_hires_needed > 10:
    hiring_risks.append({
        'risk': 'High-volume hiring may strain recruitment capacity and training resources',
        'impact': 'Delayed onboarding timelines, potential quality compromises',
        'mitigation': 'Engage external recruitment partners, implement structured onboarding program'
    })

if peak_monthly_hires > 3:
    hiring_risks.append({
        'risk': 'Peak hiring periods may overwhelm team integration processes',
        'impact': 'Reduced productivity during integration, cultural assimilation challenges',
        'mitigation': 'Stagger start dates, assign dedicated mentors, extend onboarding periods'
    })

skill_gaps = [role for role, gap in {
    'SQL Server DBA Expert': sum(d['new_hires_needed'].get('SQL Server DBA Expert', 0) for d in forecast_data),
    'Infrastructure Automation': sum(d['new_hires_needed'].get('Infrastructure Automation', 0) for d in forecast_data),
    'ITIL Service Manager': sum(d['new_hires_needed'].get('ITIL Service Manager', 0) for d in forecast_data)
}.items() if gap > 3]

if skill_gaps:
    hiring_risks.append({
        'risk': f'High demand for specialized roles: {", ".join(skill_gaps)}',
        'impact': 'Market scarcity, compensation inflation, extended recruitment cycles',
        'mitigation': 'Early recruitment initiation, internal development programs, contractor bridge solutions'
    })

if hiring_risks:
    for risk in hiring_risks:
        st.markdown(f"""
        <div class="risk-high">
            <strong>Risk:</strong> {risk['risk']}<br>
            <strong>Business Impact:</strong> {risk['impact']}<br>
            <strong>Mitigation Strategy:</strong> {risk['mitigation']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("Hiring plan appears manageable within standard organizational recruitment processes.")

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
                          f"**Technical Complexity:** {complexity_levels[comp_data['technical_complexity']]}")
                
                st.session_state.automation_components[comp_name]['enabled'] = enabled
            
            with col2:
                st.write(f"**Priority Weight:** {comp_data['weight']}%")
                st.write(f"**Implementation Effort:** {comp_data['effort']} hours")
                st.write(f"**Cost Savings:** {comp_data['cost_savings']}%")
            
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
    'Recovery Time Objective': {
        'our_score': rto_minutes,
        'industry_avg': 240,
        'industry_leader': 60,
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

# TCO Breakdown Chart
fig_tco = go.Figure(data=[
    go.Bar(
        name='Cost Components',
        x=list(target_tco['tco_breakdown'].keys()),
        y=list(target_tco['tco_breakdown'].values()),
        marker_color=['#1e40af', '#dc2626', '#059669', '#f59e0b', '#7c3aed']
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

# SQL Server Licensing Analysis (AWS License-Included Model)
st.markdown("### 📄 AWS SQL Server License-Included Analysis")

# Calculate licensing info using AWS model
aws_licensing_info = calculate_sql_server_licensing_aws(deployment_type, instance_type, target_clusters, sql_edition)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="licensing-alert">
        <h4>📋 AWS Licensing Summary</h4>
        <p><strong>Edition:</strong> SQL Server {aws_licensing_info['edition']}</p>
        <p><strong>Model:</strong> {aws_licensing_info['licensing_model']}</p>
        <p><strong>Hourly Rate:</strong> ${aws_licensing_info['hourly_rate_per_instance']:.3f}/instance</p>
        <p><strong>Deployment:</strong> {deployment_type}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("💰 Monthly Licensing", f"${aws_licensing_info['monthly_cost']:,.0f}")
    st.metric("📅 Annual Licensing", f"${aws_licensing_info['annual_cost']:,.0f}")

with col3:
    if deployment_type == "AlwaysOn Cluster":
        st.info("💡 AWS License-Included pricing automatically covers all nodes in AlwaysOn clusters. No separate licensing calculation needed.")
    else:
        st.info("💡 AWS License-Included pricing simplifies licensing - no core counting or CAL management required.")
    
    st.caption(f"**Pricing Model:** {aws_licensing_info['notes']}")

# AWS Pricing Information
st.markdown("---")
st.markdown("### 📊 AWS Pricing Details & Transparency")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💻 Current AWS Pricing")
    st.write(f"**Data Source:** {pricing_data['last_updated']}")
    st.write(f"**Instance Type:** {instance_type}")
    
    # Show pricing breakdown
    windows_rate = pricing_data['ec2_windows'].get(instance_type, 0)
    edition_key = {"Web": "ec2_sql_web", "Standard": "ec2_sql_standard", "Enterprise": "ec2_sql_enterprise"}[sql_edition]
    sql_rate = pricing_data[edition_key].get(instance_type, 0)
    licensing_rate = sql_rate - windows_rate
    
    st.write(f"**Windows Only:** ${windows_rate:.3f}/hour")
    st.write(f"**Windows + SQL {sql_edition}:** ${sql_rate:.3f}/hour")
    st.write(f"**SQL Licensing Component:** ${licensing_rate:.3f}/hour")
    
    st.write(f"**EBS {ebs_volume_type.upper()}:** ${pricing_data['ebs'][ebs_volume_type]:.3f}/GB/month")
    if enable_ssm_patching:
        st.write(f"**SSM Patch Mgmt:** ${pricing_data['ssm']['patch_manager']:.5f}/instance/hour")

with col2:
    st.markdown("#### 🎯 AWS License-Included Benefits")
    
    benefits = [
        "✅ No core counting complexity",
        "✅ No Client Access License (CAL) management", 
        "✅ Automatic compliance handling",
        "✅ Simplified billing and procurement",
        "✅ AWS enterprise pricing passed through",
        "✅ Regional pricing optimization",
        "✅ No license mobility paperwork"
    ]
    
    for benefit in benefits:
        st.write(benefit)
    
    st.markdown("**📈 Pricing Advantages:**")
    st.write("• Dynamic pricing reflects current AWS rates")
    st.write("• Volume discounts already applied")
    st.write("• No licensing true-up audits")

# ROI Analysis (Updated)
st.markdown("### 📈 Return on Investment Analysis")

# Calculate ROI based on automation benefits (infrastructure focus)
baseline_manual_cost = target_tco['total_tco']
automation_infrastructure_savings = baseline_manual_cost * (metrics['cost_savings_percentage'] / 100)
optimized_cost = baseline_manual_cost - automation_infrastructure_savings

# Implementation cost for automation (remove hardcoded hourly rate)
automation_implementation_hours = sum(comp['effort'] for comp in st.session_state.automation_components.values() if comp['enabled'])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Infrastructure Savings", f"${automation_infrastructure_savings:,.0f}")
    st.metric("⚙️ Implementation Hours", f"{automation_implementation_hours:,}")
    st.caption("Implementation cost depends on your hourly rates")

with col2:
    if automation_infrastructure_savings > 0:
        roi_percentage = (automation_infrastructure_savings / baseline_manual_cost * 100)
        st.metric("📊 Infrastructure ROI", f"{roi_percentage:.1f}%")
        
        # Payback in months (assuming savings are monthly)
        monthly_savings = automation_infrastructure_savings / timeframe
        st.metric("⏱️ Monthly Savings", f"${monthly_savings:,.0f}")
    else:
        st.metric("📊 Infrastructure ROI", "Enable automation components")

with col3:
    if automation_infrastructure_savings > baseline_manual_cost * 0.15:
        st.success("🎉 Excellent automation ROI potential")
    elif automation_infrastructure_savings > baseline_manual_cost * 0.05:
        st.info("✅ Good automation benefits")
    elif automation_infrastructure_savings > 0:
        st.warning("⚠️ Modest automation impact")
    else:
        st.error("❌ Enable automation components for ROI analysis")

# Executive Summary & Recommendations (RESTORED)
st.subheader("📊 Executive Summary & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Current Maturity Assessment")
    st.write(f"**Automation Maturity:** {metrics['automation_maturity']:.0f}% ({'Advanced' if metrics['automation_maturity'] >= 70 else 'Developing' if metrics['automation_maturity'] >= 40 else 'Initial'})")
    st.write(f"**ITIL Practice Coverage:** {metrics['itil_maturity']:.0f}% ({'Mature' if metrics['itil_maturity'] >= 70 else 'Developing'})")
    st.write(f"**Governance Framework:** {governance_maturity:.0f}% ({'Established' if governance_maturity >= 70 else 'Needs Development'})")
    st.write(f"**Total TCO:** ${target_tco['total_tco']:,.0f} over {timeframe} months")

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
    
    if target_tco['infrastructure']['sql_licensing_monthly'] > target_tco['infrastructure']['ec2_compute_monthly']:
        recommendations.append("Review SQL Server licensing strategy - licensing costs exceed compute infrastructure")
    
    if not recommendations:
        recommendations.append("✅ Continue execution of current strategy")
        recommendations.append("📈 Focus on operational excellence and continuous improvement")
    
    for rec in recommendations:
        st.write(f"• {rec}")

# Action items (RESTORED)
st.markdown("---")
st.markdown("### ✅ Immediate Action Items")

action_items = []

immediate_hires = [d for d in forecast_data[:3] if d['total_new_hires'] > 0]
if immediate_hires:
    action_items.append(f"🎯 Start recruitment for {immediate_hires[0]['total_new_hires']} positions in next 3 months")

if metrics['automation_maturity'] < 50:
    action_items.append("📚 Develop automation training program for existing team")

if current_clusters < 20 and target_clusters > 50:
    action_items.append("🗗️ Begin infrastructure automation setup to support scaling")

if total_hires_needed > 5:
    action_items.append("👥 Establish structured onboarding and mentorship program")

action_items.append("💰 Evaluate Reserved Instance pricing for long-term cost optimization")
action_items.append("📈 Establish monthly cost monitoring and optimization reviews")

for i, item in enumerate(action_items, 1):
    st.write(f"{i}. {item}")

# Certification Status (RESTORED)
st.markdown("---")
st.markdown("### 🏆 Enterprise Certification Status")

if (metrics['automation_maturity'] >= 70 and 
    metrics['itil_maturity'] >= 70 and 
    governance_maturity >= 70):
    st.success("🏆 **ENTERPRISE GRADE CERTIFIED** - This solution meets industry benchmark standards for enterprise SQL Server scaling")
elif (metrics['automation_maturity'] >= 50):
    st.warning("⚠️ **ENTERPRISE READY** - Solution has strong foundation, recommended improvements identified")
else:
    st.error("⛔ **DEVELOPMENT REQUIRED** - Significant gaps exist, not yet enterprise-grade")

# Configuration note
st.markdown("---")
st.markdown(f"""
### 🔧 Configuration & Setup

**Current Status:**
- **AWS Real-time Pricing:** {'✅ Available' if BOTO3_AVAILABLE else '❌ Unavailable (boto3 not installed)'}
- **Pricing Data Source:** {pricing_data['last_updated']}

#### Option 1: Enable Real-Time AWS Pricing (Recommended)

1. **Install boto3:** 
   ```bash
   pip install boto3
   ```

2. **Add AWS credentials to Streamlit secrets:**
   ```toml
   [aws]
   access_key_id = "your_aws_access_key"
   secret_access_key = "your_aws_secret_key"
   region = "us-east-1"
   ```

3. **Required AWS Permissions:**
   - `pricing:GetProducts` (for real-time pricing)
   - `pricing:DescribeServices` (for service information)

#### Option 2: Use Fallback Pricing (Current Setup)
The application works with representative pricing data when AWS integration is unavailable. Cost calculations remain accurate for planning purposes, though prices may not reflect current AWS rates.

#### Additional Dependencies for Full Features:
- `boto3` - AWS real-time pricing
- `plotly` - Interactive visualizations  
- `pandas` - Data analysis
- `numpy` - Numerical calculations
""")

# Footer
st.markdown("---")
st.markdown("*Enterprise SQL AlwaysOn AWS EC2 Scaling Planner v4.0 - Real-Time Pricing | Microsoft Licensing | TCO Analysis | ITIL 4 Aligned | Enterprise Governance Ready*")