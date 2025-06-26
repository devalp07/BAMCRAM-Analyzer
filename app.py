import streamlit as st
import subprocess
import tempfile
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import requests
from io import BytesIO
import zipfile
import shutil

# Set Streamlit page config
st.set_page_config(
    page_title="BAMCRAMalyzer - Advanced BAM Analysis Tool", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧬"
)

# Load and encode the background image
def get_base64_image(image_url):
    try:
        response = requests.get(image_url)
        return base64.b64encode(response.content).decode()
    except:
        return None

# ✅ Use your desired image URL here
bg_image_url = "https://img.freepik.com/free-photo/3d-render-medical-background-with-abstract-virus-cells-dna-strands_1048-14041.jpg?semt=ais_items_boosted&w=740"
bg_image_base64 = get_base64_image(bg_image_url)

# Inject custom CSS with better contrast
st.markdown(f"""
<style>
    /* 🔹 Main text visibility */
    .main .block-container, .main .block-container * {{
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
    }}

    /* 🔹 Darker background for better contrast */
    .main .block-container {{
        background-color: rgba(0, 30, 80, 0.9) !important;
    }}

    /* 🔹 Button styling */
    .stButton>button,
    .stDownloadButton>button,
    div[data-testid="stDownloadButton"] button,
    button[kind="download"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }}

    /* 🔹 File uploader styling */
    div[data-testid="stFileUploader"] div[role="button"] {{
        background-color: rgba(0, 60, 120, 0.7) !important;
        border: 2px dashed rgba(255,255,255,0.7) !important;
    }}

    /* 🔹 Background image */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image_base64 if bg_image_base64 else ''}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }}

    /* 🔹 Tables and DataFrames */
    .stDataFrame, .stTable {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
    }}

    /* 🔹 Plotly charts */
    .js-plotly-plot .plotly {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
    }}

    /* 🔹 Metric cards */
    .metric-card {{
        background: linear-gradient(135deg, rgba(0, 100, 200, 0.9), rgba(0, 60, 120, 0.9));
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    /* 🔹 Improved Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem !important;
        padding: 0.5rem !important;
        background-color: rgba(0, 40, 80, 0.7) !important;
        border-radius: 12px !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 3rem !important;
        padding: 0 1.5rem !important;
        color: rgba(255,255,255,0.7) !important;
        background-color: rgba(0, 60, 120, 0.5) !important;
        border-radius: 8px !important;
        margin: 0 !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: white !important;
        background-color: rgba(0, 80, 160, 0.7) !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: white !important;
        background: linear-gradient(135deg, #0052cc, #0066ff) !important;
        font-weight: bold !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        transform: scale(1.02) !important;
    }}

    .stTabs [aria-selected="true"]:hover {{
        background: linear-gradient(135deg, #0066ff, #0088ff) !important;
    }}

    /* Tab content container */
    .stTabs [role="tabpanel"] {{
        padding: 1.5rem 1rem !important;
        background-color: rgba(0, 30, 60, 0.7) !important;
        border-radius: 0 0 12px 12px !important;
        margin-top: -0.5rem !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-top: none !important;
    }}

    /* Add some spacing between tabs and content */
    div[data-testid="stTabs"] {{
        margin-bottom: 2rem !important;
    }}

    /* 🔹 Expanders */
    .stExpander {{
        background-color: rgba(0, 40, 80, 0.7) !important;
    }}

    /* 🔹 Text input */
    .stTextInput input {{
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
    }}

    /* 🔹 Custom Info Box Styling */
    div[data-testid="stNotification"] {{
        background: linear-gradient(135deg, rgba(0, 60, 120, 0.9), rgba(0, 40, 80, 0.9)) !important;
        border-left: 4px solid #4CAF50 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(5px);
    }}
    
    div[data-testid="stNotification"] p {{
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        font-size: 0.95rem !important;
    }}
    
    div[data-testid="stNotification"] svg {{
        color: #4CAF50 !important;
        filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.3));
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar with About and Information
with st.sidebar:
    st.markdown("## 🧬 About BAM/CRAM Analyzer")
    st.markdown("""
    **BAM/CRAM Analyzer** is a comprehensive bioinformatics tool designed for analyzing BAM (Binary Alignment Map) and CRAM files with ease and precision.
    
    ### 🔬 Key Features:
    - **Quality Control Analysis** using QualiMap (BAM only)
    - **Alignment Statistics** via Samtools
    - **Interactive Visualizations** with Plotly
    - **Chromosome Coverage Analysis**
    - **Real-time Processing**

    ### 📊 What You'll Get:
    - Detailed alignment metrics
    - Coverage statistics (BAM only)
    - Quality score distributions (BAM only)
    - Insert size analysis (BAM only)
    - GC content analysis (BAM only)
    - Mapping quality plots (BAM only)

    ### 🛠️ Tools Used:
    - **Samtools**: For BAM/CRAM file processing
    - **QualiMap**: For BAM quality assessment
    - **Plotly**: For interactive charts
    - **Pandas**: For data analysis

    ### 📋 Supported Formats:
    - BAM files (Binary Alignment Map)
    - CRAM files (Compressed Reference-oriented Alignment Map)
    - FASTA reference files for CRAM analysis
    - Indexed files preferred for faster processing

    ---

    ### 💡 Tips:
    - Ensure your BAM/CRAM file is properly formatted
    - For CRAM analysis, upload a reference genome
    - Larger files may take longer to process
    - For full QC analysis, use BAM files
    - Results are temporary and not stored
    """)

    st.markdown("---")
    st.markdown("**Version:** 2.1")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    st.markdown("""
    **Author:** Deval Pareek  
    MSc Bioinformatics, 1st Year  

    **Under the Guidance of:**  
    Mr. Akshay Zawar & Miss Shrinka Datta  
    *GeneSpectrum Life Sciences LLP*  

    Mr. Dattatraya Desai  
    *(Faculty Mentor)*  
    Teaching Faculty, Bioinformatics Centre, SPPU  

    **Duration:** May–June 2025
    """)

# Main header with attractive styling
st.markdown("""
<div style='text-align: center; padding: 3rem 0;'>
    <div style='padding: 3rem 2rem; background: linear-gradient(135deg, rgba(116, 185, 255, 0.9), rgba(9, 132, 227, 0.9)); 
                border-radius: 20px; color: white; margin: 2rem auto; max-width: 800px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.3);'
                class='glow'>
        <h1 style='font-size: 3rem; font-weight: bold; margin-bottom: 1rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>
            🧬 BAM/CRAM Analyzer 
        </h1>
        <p style='font-size: 1.5rem; color: #f1f1f1; margin-top: 1rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
            Professional BAM & CRAM File Quality Control Platform
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Welcome section with instructions
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(212,175,55,0.95) 0%, rgba(218,165,32,0.9) 50%, rgba(184,134,11,0.85) 100%);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 0 15px rgba(218,165,32,0.6), 0 0 30px rgba(255,215,0,0.3);
            text-align: center;
            border: 1.5px solid rgba(255, 215, 0, 0.4);
        '>
            <h3 style='color: white; margin-bottom: 1rem; font-size: 1.8rem;
                    text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>
                🚀 Get Started
            </h3>
            <p style='color: rgba(255, 255, 255, 0.95); font-size: 1.1rem; margin: 0;'>
                Upload your <strong>BAM</strong> or <strong>CRAM</strong> file below to begin
                comprehensive quality analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Enhanced upload box
st.markdown("""
    <div style='background-color: rgba(0, 82, 204, 0.7); padding: 1.5rem; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.2); text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);'>
        <h3 style='color: white; margin-bottom: 0.8rem; font-size: 1.6rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>📤 Upload Your BAM or CRAM File</h3>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1rem;'>For CRAM files, please also upload a reference genome for full analysis</p>
    </div>
    """, unsafe_allow_html=True)

# File uploader that accepts BAM and CRAM files
uploaded_file = st.file_uploader("Upload BAM or CRAM file", type=["bam", "cram"])
uploaded_reference = st.file_uploader("Upload Reference FASTA file (required for CRAM)", type=["fa", "fna", "fasta"])

def parse_all_qualimap_graphs(report_dir):
    """Parse all QualiMap graph data files into DataFrames"""
    results = {}
    raw_data_dir = os.path.join(report_dir, "raw_data_qualimapReport")
    
    if not os.path.exists(raw_data_dir):
        st.warning(f"QualiMap raw data directory not found: {raw_data_dir}")
        return results
    
    file_parsers = {
        'coverage_across_reference': lambda parts: {'Position': float(parts[0]), 'Coverage': float(parts[1])},
        'coverage_histogram': lambda parts: {'Coverage': float(parts[0]), 'Frequency': float(parts[1])},
        'duplication_rate_histogram': lambda parts: {'Duplication Rate': float(parts[0]), 'Count': float(parts[1])},
        'genome_fraction_coverage': lambda parts: {'Coverage': float(parts[0]), 'Genome Fraction': float(parts[1])},
        'homopolymer_indels': lambda parts: {'Type of indel': parts[0], 'Number of indels': int(parts[1])},
        'insert_size_across_reference': lambda parts: {'Position': float(parts[0]), 'Insert Size': float(parts[1])},
        'insert_size_histogram': lambda parts: {'Insert Size': float(parts[0]), 'Count': float(parts[1])},
        'mapped_reads_gc-content_distribution': lambda parts: {'GC Content (%)': float(parts[0]), 'Sample': float(parts[1])},
        'mapped_reads_nucleotide_content': lambda parts: {
            'Position (bp)': float(parts[0]),
            'A': float(parts[1]), 'C': float(parts[2]),
            'G': float(parts[3]), 'T': float(parts[4]),
            'N': float(parts[5])},
        'mapping_quality_across_reference': lambda parts: {'Position': float(parts[0]), 'Mapping Quality': float(parts[1])},
        'mapping_quality_histogram': lambda parts: {'Mapping Quality': float(parts[0]), 'Count': float(parts[1])}
    }
    
    for name, parser in file_parsers.items():
        file_path = os.path.join(raw_data_dir, f"{name}.txt")
        if os.path.exists(file_path):
            try:
                data = []
                with open(file_path, 'r') as f:
                    for line in f:
                        if not line.startswith('#'):
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                try:
                                    data.append(parser(parts))
                                except ValueError:
                                    continue
                results[name] = pd.DataFrame(data)
            except Exception as e:
                st.error(f"Error parsing {name}: {str(e)}")
    
    return results

def create_all_plots(qualimap_results):
    """Create plots from QualiMap results"""
    plots = {}
    plot_configs = {
        'coverage_across_reference': {
            'type': 'line', 'x': 'Position', 'y': 'Coverage',
            'title': "Coverage Across Reference", 'color': '#00CC96'
        },
        'coverage_histogram': {
            'type': 'line', 'x': 'Coverage', 'y': 'Frequency', 'log_y': True,
            'title': "Coverage Distribution", 'color': '#00CC96'
        },
        'duplication_rate_histogram': {
            'type': 'bar', 'x': 'Duplication Rate', 'y': 'Count',
            'title': "Duplication Rate Distribution"
        },
        'genome_fraction_coverage': {
            'type': 'line', 'x': 'Coverage', 'y': 'Genome Fraction',
            'title': "Genome Fraction Coverage", 'color': '#B6E880'
        },
        'homopolymer_indels': {
            'type': 'bar', 'x': 'Type of indel', 'y': 'Number of indels',
            'title': "Homopolymer Indels", 'color': 'Type of indel'
        },
        'insert_size_across_reference': {
            'type': 'line', 'x': 'Position', 'y': 'Insert Size',
            'title': "Insert Size Across Reference", 'color': '#636EFA'
        },
        'insert_size_histogram': {
            'type': 'bar', 'x': 'Insert Size', 'y': 'Count',
            'title': "Insert Size Distribution"
        },
        'mapped_reads_gc-content_distribution': {
            'type': 'line', 'x': 'GC Content (%)', 'y': 'Sample',
            'title': "GC Content Distribution", 'color': '#AB63FA'
        },
        'mapped_reads_nucleotide_content': {
            'type': 'stacked', 'x': 'Position (bp)',
            'cols': ['A', 'C', 'G', 'T', 'N'],
            'title': "Nucleotide Content", 
            'colors': ['#636EFA', '#00CC96', '#AB63FA', '#EF553B', '#FFA15A']
        },
        'mapping_quality_across_reference': {
            'type': 'line', 'x': 'Position', 'y': 'Mapping Quality',
            'title': "Mapping Quality Across Reference", 'color': '#EF553B'
        },
        'mapping_quality_histogram': {
            'type': 'bar', 'x': 'Mapping Quality', 'y': 'Count',
            'title': "Mapping Quality Distribution"
        }
    }
    
    for name, config in plot_configs.items():
        if name in qualimap_results and not qualimap_results[name].empty:
            df = qualimap_results[name]
            if config['type'] == 'line':
                fig = px.line(df, x=config['x'], y=config['y'], title=config['title'])
                fig.update_traces(line=dict(width=2, color=config.get('color')))
            elif config['type'] == 'bar':
                fig = px.bar(df, x=config['x'], y=config['y'], title=config['title'],
                            color=config.get('color', config['x']))
            elif config['type'] == 'stacked':
                fig = go.Figure()
                for col, color in zip(config['cols'], config['colors']):
                    fig.add_trace(go.Scatter(
                        x=df[config['x']], y=df[col], name=col,
                        line=dict(color=color), stackgroup='one'))
                fig.update_layout(title=config['title'])
            
            plots[name] = apply_plot_style(fig)
    
    return plots

def parse_samtools_stats(stats_file):
    """Parse samtools stats output into a dictionary of DataFrames"""
    stats = {}
    current_section = None
    data_lines = []
    headers = []
    
    def safe_int_convert(value):
        """Safely convert value to integer, handling special cases"""
        try:
            return int(value)
        except ValueError:
            # Handle ranges like "[1-1]" by taking the first number
            if value.startswith('[') and '-' in value and value.endswith(']'):
                return int(value.split('-')[0].strip('['))
            return 0  # Default value if conversion fails
    
    def safe_float_convert(value):
        """Safely convert value to float"""
        try:
            return float(value)
        except ValueError:
            return 0.0  # Default value if conversion fails
    
    with open(stats_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            if line.startswith('SN'):
                # Summary numbers section
                line = line.split('#')[0].strip()
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'SN' not in stats:
                        stats['SN'] = []
                    stats['SN'].append({
                        'Metric': parts[1].strip(':'),
                        'Value': parts[2].strip()
                    })
            elif line.startswith('FFQ'):
                # First fragment qualities
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'FFQ' not in stats:
                        stats['FFQ'] = []
                    stats['FFQ'].append({
                        'Cycle': safe_int_convert(parts[1]),
                        'Quality': safe_float_convert(parts[2])
                    })
            elif line.startswith('LFQ'):
                # Last fragment qualities
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'LFQ' not in stats:
                        stats['LFQ'] = []
                    stats['LFQ'].append({
                        'Cycle': safe_int_convert(parts[1]),
                        'Quality': safe_float_convert(parts[2])
                    })
            elif line.startswith('GCF'):
                # GC content of first fragments
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'GCF' not in stats:
                        stats['GCF'] = []
                    stats['GCF'].append({
                        'GC%': safe_float_convert(parts[1]),
                        'Count': safe_int_convert(parts[2])
                    })
            elif line.startswith('GCL'):
                # GC content of last fragments
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'GCL' not in stats:
                        stats['GCL'] = []
                    stats['GCL'].append({
                        'GC%': safe_float_convert(parts[1]),
                        'Count': safe_int_convert(parts[2])
                    })
            elif line.startswith('IS'):
                # Insert sizes
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'IS' not in stats:
                        stats['IS'] = []
                    stats['IS'].append({
                        'Insert Size': safe_int_convert(parts[1]),
                        'Count': safe_int_convert(parts[2])
                    })
            elif line.startswith('RL'):
                # Read lengths
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'RL' not in stats:
                        stats['RL'] = []
                    stats['RL'].append({
                        'Length': safe_int_convert(parts[1]),
                        'Count': safe_int_convert(parts[2])
                    })
            elif line.startswith('COV'):
                # Coverage distribution
                parts = line.split('\t')
                if len(parts) >= 3:
                    if 'COV' not in stats:
                        stats['COV'] = []
                    stats['COV'].append({
                        'Coverage': safe_int_convert(parts[1]),
                        'Count': safe_int_convert(parts[2])
                    })
    
    # Convert lists to DataFrames
    for key in stats:
        stats[key] = pd.DataFrame(stats[key])
    
    return stats

def create_samtools_plots(stats):
    """Create plots from samtools stats"""
    plots = {}
    
    # Summary metrics
    if 'SN' in stats:
        df = stats['SN']
        # Filter for key metrics
        key_metrics = ['raw total sequences', 'reads mapped', 'reads mapped and paired', 
                      'reads properly paired', 'average length', 'average quality',
                      'insert size average', 'insert size standard deviation',
                      'inward oriented pairs', 'outward oriented pairs',
                      'pairs with other orientation', 'pairs on different chromosomes']
        
        filtered_df = df[df['Metric'].isin(key_metrics)]
        
        # Convert values to numeric where possible
        filtered_df['Value'] = pd.to_numeric(filtered_df['Value'], errors='coerce')
        filtered_df = filtered_df.dropna()
        
        if not filtered_df.empty:
            fig = px.bar(filtered_df, x='Metric', y='Value', title="Key Alignment Metrics")
            plots['summary_metrics'] = apply_plot_style(fig)
    
    # First and last fragment qualities
    if 'FFQ' in stats and 'LFQ' in stats:
        ffq = stats['FFQ']
        lfq = stats['LFQ']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ffq['Cycle'], y=ffq['Quality'],
            name='First Fragment',
            line=dict(color='#636EFA')
        ))
        fig.add_trace(go.Scatter(
            x=lfq['Cycle'], y=lfq['Quality'],
            name='Last Fragment',
            line=dict(color='#EF553B')
        ))
        fig.update_layout(
            title='Read Quality by Cycle',
            xaxis_title='Cycle',
            yaxis_title='Quality Score'
        )
        plots['read_quality'] = apply_plot_style(fig)
    
    # GC content
    if 'GCF' in stats and 'GCL' in stats:
        gcf = stats['GCF']
        gcl = stats['GCL']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=gcf['GC%'], y=gcf['Count'],
            name='First Fragment',
            line=dict(color='#00CC96')
        ))
        fig.add_trace(go.Scatter(
            x=gcl['GC%'], y=gcl['Count'],
            name='Last Fragment',
            line=dict(color='#AB63FA')
        ))
        fig.update_layout(
            title='GC Content Distribution',
            xaxis_title='GC %',
            yaxis_title='Count'
        )
        plots['gc_content'] = apply_plot_style(fig)
    
    # Insert size
    if 'IS' in stats:
        df = stats['IS']
        fig = px.line(df, x='Insert Size', y='Count', title="Insert Size Distribution")
        plots['insert_size'] = apply_plot_style(fig)
    
    # Read length
    if 'RL' in stats:
        df = stats['RL']
        fig = px.line(df, x='Length', y='Count', title="Read Length Distribution")
        plots['read_length'] = apply_plot_style(fig)
    
    # Coverage
    if 'COV' in stats:
        df = stats['COV']
        fig = px.area(
            df, x='Coverage', y='Count', title="Coverage Distribution (Area Plot)", line_shape='spline'
        )
        plots['coverage'] = apply_plot_style(fig)
    
    return plots

def apply_plot_style(fig):
    """Apply consistent styling with bold dark fonts for white background apps"""
    fig.update_layout(
        paper_bgcolor='white',  # White background for paper
        plot_bgcolor='rgba(240,240,240,0.9)',  # Light gray plot area
        font=dict(
            color='#222222',          # Very dark gray text (almost black)
            family='Arial Black',     # Bold font family
            size=14
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',  # Light grid lines
            title_font=dict(size=14, color='#222222', family='Arial Black'),
            tickfont=dict(size=13, color='#222222', family='Arial Black')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            title_font=dict(size=14, color='#222222', family='Arial Black'),
            tickfont=dict(size=13, color='#222222', family='Arial Black')
        ),
        hovermode='x unified',
        margin=dict(l=50, r=50, b=50, t=70)
    )
    return fig

def create_download_zip(temp_dir, files_to_zip, zip_name):
    """Create a zip file from multiple files in a temporary directory"""
    zip_path = os.path.join(temp_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_info in files_to_zip:
            file_path = file_info['path']
            arcname = file_info.get('arcname', os.path.basename(file_path))
            zipf.write(file_path, arcname)
    return zip_path

def save_plotly_figure(fig, path, format='html'):
    """Save plotly figure in multiple formats"""
    if format == 'html':
        fig.write_html(path)
    elif format == 'png':
        fig.write_image(path)
    elif format == 'svg':
        fig.write_image(path, format='svg')
    elif format == 'pdf':
        fig.write_image(path, format='pdf')

if uploaded_file:
    is_cram = uploaded_file.name.lower().endswith('.cram')
    is_bam = uploaded_file.name.lower().endswith('.bam')

    # Stylish Upload Confirmation
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(0, 184, 148, 0.9), rgba(0, 160, 133, 0.9)); 
                padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.2);'>
        <h4 style='color: white; margin: 0;'>✅ File Uploaded Successfully!</h4>
        <p style='margin: 0.5rem 0 0 0;'>Processing: <strong>{uploaded_file.name}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        reference_path = None

        # Save files
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
            
        if uploaded_reference:
            reference_path = os.path.join(tmpdir, uploaded_reference.name)
            with open(reference_path, "wb") as f:
                f.write(uploaded_reference.read())
            
        # Run flagstat for both BAM and CRAM
        with st.spinner("🔍 Running samtools flagstat..."):
            try:
                flagstat_result = subprocess.run(
                    ["samtools", "flagstat", file_path],
                    capture_output=True, text=True, check=True
                )
                flagstat_text = flagstat_result.stdout
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Failed to run samtools flagstat: {e.stderr}")
                st.stop()
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.stop()

        # 🚀 For CRAM: Enhanced analysis with samtools stats when reference is provided
        if is_cram:
            if uploaded_reference:
                st.success("🎉 CRAM Analysis with Reference Complete!")
                
                # Run samtools stats
                with st.spinner("🧬 Running samtools stats (this may take a few minutes)..."):
                    try:
                        stats_file = os.path.join(tmpdir, "samtools_stats.txt")
                        
                        # Run samtools stats with reference
                        result = subprocess.run([
                            "samtools", "stats",
                            "-r", reference_path,
                            file_path
                        ], capture_output=True, text=True)
                        
                        # Save stats to file
                        with open(stats_file, 'w') as f:
                            f.write(result.stdout)
                            
                        # Parse stats
                        stats = parse_samtools_stats(stats_file)
                        stats_plots = create_samtools_plots(stats)
                        
                    except Exception as e:
                        st.error(f"❌ samtools stats failed with error: {str(e)}")
                        stats = {}
                        stats_plots = {}
                        
                # Display results in tabs
                tab1, tab2 = st.tabs(["📊 Alignment Statistics", "📈 Visualizations"])
                
                with tab1:
                    st.markdown("""
                    <div style="background-color: rgba(0, 0, 0, 0.6); padding: 15px; border-radius: 10px;">
                        <h3 style="color: white;">📊 CRAM File Alignment Statistics</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Parse flagstat metrics
                    metrics_data = []
                    for line in flagstat_text.splitlines():
                        if line.strip():
                            parts = line.split('+')
                            if len(parts) == 2:
                                count = int(parts[0].strip())
                                desc = parts[1].split('(')[0].strip()
                                metrics_data.append({"metric": desc, "count": count})

                    # Create metric cards
                    if metrics_data:
                        cols = st.columns(3)
                        for i, metric in enumerate(metrics_data):
                            with cols[i % 3]:
                                st.markdown(f"""
                                <div class='metric-card glow'>
                                    <h4 style='color: white; margin: 0; font-size: 0.9rem;'>{metric['metric']}</h4>
                                    <h2 style='color: white; margin: 0.5rem 0 0 0;'>{metric['count']:,}</h2>
                                </div>
                                """, unsafe_allow_html=True)
                                
                    # Show samtools stats summary
                    if 'SN' in stats:
                        st.markdown("""
                        <div style="background-color: rgba(0, 0, 0, 0.6); padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h3 style="color: white;">📋 Samtools Stats Summary</h3>
                        </div>
                        """, unsafe_allow_html=True)

                        # Convert the list of dicts into a DataFrame (if not already)
                        all_stats_df = pd.DataFrame(stats['SN'])

                        # Show the full dataframe
                        st.dataframe(all_stats_df, use_container_width=True)
                        
                        # Download button for stats
                        st.markdown("### 📥 Download Statistics")
                        csv = all_stats_df.to_csv(index=False)
                        st.download_button(
                            label="📊 Download Stats (CSV)",
                            data=csv,
                            file_name="cram_stats_summary.csv",
                            mime="text/csv"
                        )
                
                with tab2:
                    st.markdown("""
                    <div style="background-color: rgba(0, 0, 0, 0.6); padding: 15px; border-radius: 10px;">
                        <h3 style="color: white;">📈 Samtools Stats Visualizations</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display all available plots
                    for plot_name, fig in stats_plots.items():
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Download buttons for each plot
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                label=f"📥 {plot_name} (HTML)",
                                data=fig.to_html(),
                                file_name=f"{plot_name}.html",
                                mime="text/html"
                            )
                        with col2:
                            st.download_button(
                                label=f"📥 {plot_name} (PNG)",
                                data=fig.to_image(format="png"),
                                file_name=f"{plot_name}.png",
                                mime="image/png"
                            )
                        with col3:
                            st.download_button(
                                label=f"📥 {plot_name} (PDF)",
                                data=fig.to_image(format="pdf"),
                                file_name=f"{plot_name}.pdf",
                                mime="application/pdf"
                            )
                    
                    st.markdown("---")
                    st.markdown("### 📦 Download All Results")
                    
                    # Prepare files for zip
                    files_to_zip = []
                    
                    # Add flagstat
                    flagstat_path = os.path.join(tmpdir, "flagstat.txt")
                    with open(flagstat_path, "w") as f:
                        f.write(flagstat_text)
                    files_to_zip.append({"path": flagstat_path, "arcname": "flagstat.txt"})
                    
                    # Add stats
                    for stat_name, df in stats.items():
                        stat_path = os.path.join(tmpdir, f"{stat_name}.csv")
                        df.to_csv(stat_path, index=False)
                        files_to_zip.append({"path": stat_path, "arcname": f"stats/{stat_name}.csv"})
                    
                    # Add plots in multiple formats
                    for plot_name, fig in stats_plots.items():
                        # HTML
                        html_path = os.path.join(tmpdir, f"{plot_name}.html")
                        fig.write_html(html_path)
                        files_to_zip.append({"path": html_path, "arcname": f"plots/html/{plot_name}.html"})
                        
                        # PNG
                        png_path = os.path.join(tmpdir, f"{plot_name}.png")
                        fig.write_image(png_path)
                        files_to_zip.append({"path": png_path, "arcname": f"plots/png/{plot_name}.png"})
                        
                        # PDF
                        pdf_path = os.path.join(tmpdir, f"{plot_name}.pdf")
                        fig.write_image(pdf_path, format="pdf")
                        files_to_zip.append({"path": pdf_path, "arcname": f"plots/pdf/{plot_name}.pdf"})
                    
                    # Create zip file
                    zip_path = os.path.join(tmpdir, "cram_analysis_results.zip")
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for file_info in files_to_zip:
                            zipf.write(file_info['path'], file_info['arcname'])
                    
                    # Download button for zip
                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="📦 Download All Results (ZIP)",
                            data=f,
                            file_name=f"cram_analysis_{datetime.now().strftime('%Y%m%d')}.zip",
                            mime="application/zip"
                        )

            else:  # No reference provided for CRAM
                st.success("🎉 Basic CRAM Analysis Complete!")
                st.warning("⚠️ For full CRAM analysis including coverage metrics, please upload a reference genome")
                
                # Display results in a single tab
                tab = st.tabs(["📊 Alignment Statistics"])[0]
                
                with tab:
                    st.markdown("""
                    <div style="background-color: rgba(0, 0, 0, 0.6); padding: 15px; border-radius: 10px;">
                        <h3 style="color: white;">📊 CRAM File Alignment Statistics</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Parse flagstat metrics
                    metrics_data = []
                    for line in flagstat_text.splitlines():
                        if line.strip():
                            parts = line.split('+')
                            if len(parts) == 2:
                                count = int(parts[0].strip())
                                desc = parts[1].split('(')[0].strip()
                                metrics_data.append({"metric": desc, "count": count})

                    # Create metric cards
                    if metrics_data:
                        cols = st.columns(3)
                        for i, metric in enumerate(metrics_data):
                            with cols[i % 3]:
                                st.markdown(f"""
                                <div class='metric-card glow'>
                                    <h4 style='color: white; margin: 0; font-size: 0.9rem;'>{metric['metric']}</h4>
                                    <h2 style='color: white; margin: 0.5rem 0 0 0;'>{metric['count']:,}</h2>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Download button for flagstat
                    st.markdown("### 📥 Download Results")
                    st.download_button(
                        label="📊 Download Flagstat Results (CSV)",
                        data=pd.DataFrame(metrics_data).to_csv(index=False),
                        file_name="cram_flagstat_results.csv",
                        mime="text/csv"
                    )

        # 🚀 For BAM: Full analysis
        elif is_bam:
            try:
                # First ensure BAM is indexed
                with st.spinner("📇 Indexing BAM file..."):
                    try:
                        subprocess.run(["samtools", "index", file_path], check=True)
                    except subprocess.CalledProcessError as e:
                        st.error(f"❌ Failed to index BAM: {e.stderr}")
                        st.stop()

                # Qualimap analysis
                with st.spinner("🧬 Running QualiMap (this may take several minutes)..."):
                    out_dir = os.path.join(tmpdir, "qualimap_out")
                    os.makedirs(out_dir, exist_ok=True)

                    subprocess.run([
                        "qualimap", "bamqc",
                        "-bam", file_path,
                        "-outdir", out_dir,
                        "--java-mem-size=8G"
                    ], check=True)     
                
                    qualimap_results = parse_all_qualimap_graphs(out_dir)
                    plots = create_all_plots(qualimap_results)
                    
                # idxstats
                with st.spinner("📈 Running samtools idxstats..."):
                    idxstats_result = subprocess.run(
                        ["samtools", "idxstats", file_path],
                        capture_output=True, text=True, check=True
                    )
                    idxstat_text = idxstats_result.stdout
                
                # Samtools stats
                with st.spinner("🧬 Running samtools stats (this may take a few minutes)..."):
                    try:
                        stats_file = os.path.join(tmpdir, "samtools_stats.txt")
                        
                        # Run samtools stats
                        result = subprocess.run([
                            "samtools", "stats",
                            file_path
                        ], capture_output=True, text=True)
                        
                        # Save stats to file
                        with open(stats_file, 'w') as f:
                            f.write(result.stdout)
                            
                        # Parse stats
                        stats = parse_samtools_stats(stats_file)
                        stats_plots = create_samtools_plots(stats)
                        
                    except Exception as e:
                        st.error(f"❌ samtools stats failed with error: {str(e)}")
                        stats = {}
                        stats_plots = {}
                        
                # Display results in multiple tabs
                st.success("🎉 BAM Analysis Complete!")
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Statistics", 
                    "🧬 Chromosomes", 
                    "📈 Visualizations", 
                    "📋 Summary Report"
                ])
                
                # --- Tab 1: Enhanced Statistics ---
                with tab1:
                    st.markdown("""
                    <div style="background-color: rgba(0, 0, 0, 0.6); padding: 15px; border-radius: 10px;">
                                    <h3 style="color: white;">📊 Comprehensive Alignment Statistics</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Parse flagstat metrics
                    metrics_data = []
                    for line in flagstat_text.splitlines():
                        if line.strip():
                            parts = line.split('+')
                            if len(parts) == 2:
                                count = int(parts[0].strip())
                                desc = parts[1].split('(')[0].strip()
                                metrics_data.append({"metric": desc, "count": count})

                    # Create metric cards
                    if metrics_data:
                        cols = st.columns(3)
                        for i, metric in enumerate(metrics_data):
                            with cols[i % 3]:
                                st.markdown(f"""
                                <div class='metric-card glow'>
                                    <h4 style='color: white; margin: 0; font-size: 0.9rem;'>{metric['metric']}</h4>
                                    <h2 style='color: white; margin: 0.5rem 0 0 0;'>{metric['count']:,}</h2>
                                </div>
                                """, unsafe_allow_html=True)

                    # Samtools stats summary
                    if 'SN' in stats:
                        st.markdown("""
                        <div style="background-color: rgba(0, 0, 0, 0.6); padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h3 style="color: white;">📋 Samtools Stats Summary</h3>
                        </div>
                        """, unsafe_allow_html=True)

                        all_stats_df = pd.DataFrame(stats['SN'])
                        st.dataframe(all_stats_df, use_container_width=True)
                        
                        # Download button for stats
                        st.markdown("### 📥 Download Statistics")
                        csv = all_stats_df.to_csv(index=False)
                        st.download_button(
                            label="📊 Download Stats (CSV)",
                            data=csv,
                            file_name="bam_stats_summary.csv",
                            mime="text/csv"
                        )
                
                # --- Tab 2: Enhanced Chromosome Analysis ---
                with tab2:            
                    st.markdown("""
                    <h2 style='color: white; border-bottom: 2px solid rgba(255, 255, 255, 0.3);background-color: rgba(0, 0, 0, 0.6); padding-bottom: 10px;'>
                        🧬 Chromosome Distribution Analysis
                    </h2>
                    """, unsafe_allow_html=True)
                    
                    chr_data = []
                    for line in idxstat_text.splitlines():
                        if line.strip():
                            parts = line.split('\t')
                            if len(parts) >= 4:
                                chr_data.append({
                                    "Chromosome": parts[0],
                                    "Length": int(parts[1]),
                                    "Mapped": int(parts[2]),
                                    "Unmapped": int(parts[3])
                                })

                    if chr_data:
                        df = pd.DataFrame(chr_data)
                        df['Total_Reads'] = df['Mapped'] + df['Unmapped']
                        df['Coverage_Depth'] = df['Mapped'] / df['Length']
                        df['Mapping_Rate'] = (df['Mapped'] / df['Total_Reads']) * 100

                        # Top chromosomes analysis
                        top_df = df.nlargest(10, 'Mapped')

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("""
                                <h2 style='color: white; border-bottom: 2px solid rgba(255, 255, 255, 0.3); padding: 8px 0;'>
                                    🏆 Top 10 Chromosomes by Mapped Reads
                                </h2>
                            """, unsafe_allow_html=True)
                            st.dataframe(
                                top_df[['Chromosome', 'Mapped', 'Coverage_Depth', 'Mapping_Rate']].round(4),
                                use_container_width=True
                            )

                        with col2:
                            fig_bar = px.bar(
                                top_df, 
                                x='Chromosome', 
                                y='Mapped',
                                title="Mapped Reads by Chromosome (Top 10)",
                                color='Coverage_Depth',
                                color_continuous_scale='viridis'
                            )
                            fig_bar.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white'),
                                xaxis=dict(tickfont=dict(color='white'), title_font=dict(color='white')),
                                yaxis=dict(tickfont=dict(color='white'), title_font=dict(color='white')),
                                title={'font': {'color': 'white', 'size': 20}},
                                xaxis_tickangle=-45
                            )
                            st.plotly_chart(fig_bar, use_container_width=True)
                            
                            # Complete data table
                            st.markdown("""
                                <h2 style='color: white; border-bottom: 2px solid rgba(255, 255, 255, 0.3); padding: 8px 0;'>
                                    📋 Complete Chromosome Statistics
                                </h2>
                            """, unsafe_allow_html=True)
                            st.dataframe(
                                df.sort_values('Mapped', ascending=False).round(4),
                                use_container_width=True
                            )
                        
                        # Download button for chromosome data
                        st.markdown("### 📥 Download Chromosome Data")
                        st.download_button(
                            label="📊 Download Chromosome Stats (CSV)",
                            data=df.to_csv(index=False),
                            file_name="chromosome_stats.csv",
                            mime="text/csv"
                        )

                # --- Tab 3: Enhanced Visualizations ---
                with tab3:
                    st.markdown("""
                    <h2 style='color: white; border-bottom: 2px solid rgba(255, 255, 255, 0.3); padding-bottom: 10px;'>
                        📈 Interactive Quality Control Visualizations
                    </h2>
                    """, unsafe_allow_html=True)
                    
                    # Display all available plots
                    for plot_name, fig in plots.items():
                        st.plotly_chart(apply_plot_style(fig), use_container_width=True)
                        
                        # Download buttons for each plot
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                label=f"📥 {plot_name} (HTML)",
                                data=fig.to_html(),
                                file_name=f"{plot_name}.html",
                                mime="text/html"
                            )
                        with col2:
                            st.download_button(
                                label=f"📥 {plot_name} (PNG)",
                                data=fig.to_image(format="png"),
                                file_name=f"{plot_name}.png",
                                mime="image/png"
                            )
                        with col3:
                            st.download_button(
                                label=f"📥 {plot_name} (PDF)",
                                data=fig.to_image(format="pdf"),
                                file_name=f"{plot_name}.pdf",
                                mime="application/pdf"
                            )

                # --- Tab 4: Summary Report ---
                with tab4:
                    st.markdown("""
                    <h2 style='color: white; border-bottom: 2px solid rgba(255, 255, 255, 0.3); padding-bottom: 10px;'>
                        📋 Analysis Summary Report
                    </h2>
                    """, unsafe_allow_html=True)

                    # Generate summary statistics
                    if chr_data:
                        total_mapped = df['Mapped'].sum()
                        total_unmapped = df['Unmapped'].sum()
                        total_reads = total_mapped + total_unmapped
                        mapping_rate = (total_mapped / total_reads * 100) if total_reads > 0 else 0
                        
                        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
                        
                        with summary_col1:
                            st.markdown(f"""
                            <div class='metric-card glow'>
                                <h4 style='color: white; margin: 0;'>Total Reads</h4>
                                <h2 style='color: white; margin: 0.5rem 0 0 0;'>{total_reads:,}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with summary_col2:
                            st.markdown(f"""
                            <div class='metric-card glow'>
                                <h4 style='color: white; margin: 0;'>Mapped Reads</h4>
                                <h2 style='color: white; margin: 0.5rem 0 0 0;'>{total_mapped:,}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with summary_col3:
                            st.markdown(f"""
                            <div class='metric-card glow'>
                                <h4 style='color: white; margin: 0;'>Unmapped Reads</h4>
                                <h2 style='color: white; margin: 0.5rem 0 0 0;'>{total_unmapped:,}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with summary_col4:
                            st.markdown(f"""
                            <div class='metric-card glow'>
                                <h4 style='color: white; margin: 0;'>Mapping Rate</h4>
                                <h2 style='color: white; margin: 0.5rem 0 0 0;'>{mapping_rate:.2f}%</h2>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Analysis timestamp
                    st.markdown(f"""
                    <div style='background: rgba(0, 82, 204, 0.7); padding: 1.5rem; border-radius: 10px; 
                                margin: 2rem 0; border-left: 4px solid rgba(255, 255, 255, 0.5);
                                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);'>
                        <h4 style='margin: 0; color: white;'>📅 Analysis Information</h4>
                        <p style='margin: 0.5rem 0 0 0; color: rgba(255, 255, 255, 0.9);'>
                            <strong>File:</strong> {uploaded_file.name}<br>
                            <strong>Analysis Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                            <strong>Tools Used:</strong> Samtools, QualiMap, Plotly
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### 📦 Download All Results")
                    
                    # Prepare files for zip
                    files_to_zip = []
                    
                    # Add flagstat
                    flagstat_path = os.path.join(tmpdir, "flagstat.txt")
                    with open(flagstat_path, "w") as f:
                        f.write(flagstat_text)
                    files_to_zip.append({"path": flagstat_path, "arcname": "flagstat.txt"})
                    
                    # Add idxstats
                    if chr_data:
                        idxstats_path = os.path.join(tmpdir, "chromosome_stats.csv")
                        df.to_csv(idxstats_path, index=False)
                        files_to_zip.append({"path": idxstats_path, "arcname": "chromosome_stats.csv"})
                    
                    # Add stats
                    for stat_name, df in stats.items():
                        stat_path = os.path.join(tmpdir, f"{stat_name}.csv")
                        df.to_csv(stat_path, index=False)
                        files_to_zip.append({"path": stat_path, "arcname": f"stats/{stat_name}.csv"})
                    
                    # Add qualimap plots in multiple formats
                    for plot_name, fig in plots.items():
                        # HTML
                        html_path = os.path.join(tmpdir, f"{plot_name}.html")
                        fig.write_html(html_path)
                        files_to_zip.append({"path": html_path, "arcname": f"plots/html/{plot_name}.html"})
                        
                        # PNG
                        png_path = os.path.join(tmpdir, f"{plot_name}.png")
                        fig.write_image(png_path)
                        files_to_zip.append({"path": png_path, "arcname": f"plots/png/{plot_name}.png"})
                        
                        # PDF
                        pdf_path = os.path.join(tmpdir, f"{plot_name}.pdf")
                        fig.write_image(pdf_path, format="pdf")
                        files_to_zip.append({"path": pdf_path, "arcname": f"plots/pdf/{plot_name}.pdf"})
                    
                    # Add samtools stats plots
                    for plot_name, fig in stats_plots.items():
                        # HTML
                        html_path = os.path.join(tmpdir, f"samtools_{plot_name}.html")
                        fig.write_html(html_path)
                        files_to_zip.append({"path": html_path, "arcname": f"plots/samtools/html/{plot_name}.html"})
                        
                        # PNG
                        png_path = os.path.join(tmpdir, f"samtools_{plot_name}.png")
                        fig.write_image(png_path)
                        files_to_zip.append({"path": png_path, "arcname": f"plots/samtools/png/{plot_name}.png"})
                        
                        # PDF
                        pdf_path = os.path.join(tmpdir, f"samtools_{plot_name}.pdf")
                        fig.write_image(pdf_path, format="pdf")
                        files_to_zip.append({"path": pdf_path, "arcname": f"plots/samtools/pdf/{plot_name}.pdf"})
                    
                    # Create zip file
                    zip_path = os.path.join(tmpdir, "bam_analysis_results.zip")
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for file_info in files_to_zip:
                            zipf.write(file_info['path'], file_info['arcname'])
                    
                    # Download button for zip
                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="📦 Download All Results (ZIP)",
                            data=f,
                            file_name=f"bam_analysis_{datetime.now().strftime('%Y%m%d')}.zip",
                            mime="application/zip"
                        )

            except subprocess.CalledProcessError as e:
                st.error(f"❌ Command execution failed: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error occurred: {e}")

else:
    # Welcome message when no file is uploaded
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0; background: linear-gradient(135deg, rgba(116, 185, 255, 0.9), rgba(9, 132, 227, 0.9)); 
                border-radius: 15px; color: white; margin: 2rem 0; border: 1px solid rgba(255, 255, 255, 0.3);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);' class='glow'>
        <h2 style='color: white; margin-bottom: 1rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>👆 Ready to Analyze Your BAM/CRAM File?</h2>
        <p style='font-size: 1.1rem; margin: 0; color: rgba(255, 255, 255, 0.9);'>
            Upload your BAM or CRAM file above to unlock comprehensive analysis<br>
            For CRAM files, please also upload a reference genome for full analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("""
    <h2 style='color: white; text-align: center; margin-bottom: 2rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>
        🌟 Comprehensive BAM & CRAM Analysis
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center; 
                    border: 1px solid rgba(255, 255, 255, 0.2); height: 100%;' class='glow'>
            <h3 style='color: white; margin-bottom: 1rem;'>⚡ Dual Format Support</h3>
            <p style='color: rgba(255, 255, 255, 0.9);'>Works with both BAM and CRAM files, with appropriate analysis for each format</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center;
                    border: 1px solid rgba(255, 255, 255, 0.2); height: 100%;' class='glow'>
            <h3 style='color: white; margin-bottom: 1rem;'>📊 Full QC for BAM</h3>
            <p style='color: rgba(255, 255, 255, 0.9);'>Complete quality control analysis including coverage, GC content, and more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center;
                    border: 1px solid rgba(255, 255, 255, 0.2); height: 100%;' class='glow'>
            <h3 style='color: white; margin-bottom: 1rem;'>🔬 Enhanced CRAM with Reference</h3>
            <p style='color: rgba(255, 255, 255, 0.9);'>Full samtools stats analysis when reference genome is provided</p>
        </div>
        """, unsafe_allow_html=True)


