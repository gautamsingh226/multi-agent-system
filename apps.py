"""
Multi-Agent Research Assistant - Streamlit Application
A professional web interface for AI-powered research using multiple specialized agents.

Usage:
    streamlit run app.py

Author: Your Name
Version: 1.0
"""

import streamlit as st
import time
from typing import Dict, Any, Optional
from datetime import datetime
import json
import pickle
import hashlib
from pathlib import Path
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-repo",
        "Report a bug": "https://github.com/your-repo/issues",
        "About": "Multi-Agent RAG Research System v1.0"
    }
)


# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .header-container {
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 50%, #fce7f3 100%);
        color: #4338ca;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .header-container h1 {
        font-size: 1.5rem !important;
        margin-bottom: 0.2rem !important;
        color: #4338ca;
    }
    
    .header-container p {
        font-size: 0.85rem;
        color: #6366f1;
        margin: 0;
    }
    
    .suggestion-chip {
        display: inline-block;
        background: linear-gradient(135deg, #e0e7ff, #f3e8ff);
        color: #4338ca;
        border: 1px solid #c7d2fe;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .suggestion-chip:hover {
        background: linear-gradient(135deg, #c7d2fe, #e9d5ff);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(99,102,241,0.2);
    }
    
    .history-item {
        background: #f8f9fa;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.4rem;
        font-size: 0.82rem;
        border-left: 3px solid #a5b4fc;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        background: #e0e7ff;
        border-left-color: #6366f1;
    }
    
    .history-time {
        font-size: 0.7rem;
        color: #9ca3af;
    }
    
    .step-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .step-container:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .step-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .step-content {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .report-container {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .feedback-container {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe6e0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin-top: 1.5rem;
        font-size: 0.95rem;
    }
    
    .success-badge {
        display: inline-block;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-left: 0.5rem;
        box-shadow: 0 3px 10px rgba(40, 167, 69, 0.3);
    }
    
    .error-badge {
        display: inline-block;
        background: linear-gradient(135deg, #dc3545 0%, #ff6b6b 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-left: 0.5rem;
        box-shadow: 0 3px 10px rgba(220, 53, 69, 0.3);
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

class ResearchCache:
    """Handle caching of research results."""
    
    def __init__(self, cache_dir: str = ".research_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, topic: str) -> str:
        """Generate cache key from topic."""
        return hashlib.md5(topic.encode()).hexdigest()
    
    def save(self, topic: str, state: Dict[str, Any]) -> None:
        """Save research results to cache."""
        try:
            cache_key = self.get_cache_key(topic)
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            with open(cache_file, 'wb') as f:
                pickle.dump({
                    'topic': topic,
                    'state': state,
                    'timestamp': datetime.now().isoformat()
                }, f)
        except Exception as e:
            st.warning(f"Cache save failed: {str(e)}")
    
    def load(self, topic: str) -> Optional[Dict[str, Any]]:
        """Load research results from cache."""
        try:
            cache_key = self.get_cache_key(topic)
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    return data
        except Exception as e:
            st.warning(f"Cache load failed: {str(e)}")
        return None
    
    def clear(self) -> None:
        """Clear all cache."""
        try:
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
        except Exception as e:
            st.warning(f"Cache clear failed: {str(e)}")


@st.cache_resource
def get_cache():
    """Get cache instance (cached by Streamlit)."""
    return ResearchCache()


# ============================================================================
# MAIN PIPELINE FUNCTION
# ============================================================================

def run_research_pipeline(topic: str, use_cache: bool = True) -> Dict[str, Any]:
    """
    Run the complete research pipeline with caching support.
    
    Steps:
        1. Search Agent - Find information
        2. Reader Agent - Scrape content
        3. Writer Chain - Generate report
        4. Critic Chain - Evaluate quality
    """
    cache = get_cache()
    
    # Check cache first
    if use_cache:
        cached_result = cache.load(topic)
        if cached_result:
            st.info("✨ Using cached results from previous research")
            return cached_result['state']
    
    state = {}
    
    # ========== STEP 1: Search Agent ==========
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown("### Step 1: 🔍 Search Agent")
    search_col1, search_col2 = st.columns([3, 1])
    
    search_placeholder = search_col1.empty()
    with search_col2:
        search_status = st.empty()
    
    with st.spinner("Searching for recent and reliable information..."):
        try:
            search_agent = build_search_agent()
            search_results = search_agent.invoke({
                "messages": [("user", f"find recent and reliable information on the topic: {topic}")],
            })
            state["search_results"] = search_results['messages'][-1].content
            state["step1_success"] = True
            state["step1_error"] = None
            state["step1_time"] = datetime.now().isoformat()
        except Exception as e:
            state["step1_success"] = False
            state["step1_error"] = str(e)
            state["search_results"] = None
    
    with search_placeholder.container():
        if state["step1_success"]:
            search_status.markdown(
                '<span class="success-badge">✓ Completed</span>',
                unsafe_allow_html=True
            )
            with st.expander("📄 View Search Results", expanded=True):
                st.markdown(state["search_results"][:2000] + "...")
                st.caption(f"Full results length: {len(state['search_results'])} characters")
        else:
            search_status.markdown(
                '<span class="error-badge">✗ Error</span>',
                unsafe_allow_html=True
            )
            st.error(f"Search Agent Error: {state['step1_error']}")
            st.markdown("</div>", unsafe_allow_html=True)
            return state
    
    st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(0.3)
    
    # ========== STEP 2: Reader Agent ==========
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown("### Step 2: 📖 Reader Agent")
    reader_col1, reader_col2 = st.columns([3, 1])
    
    reader_placeholder = reader_col1.empty()
    with reader_col2:
        reader_status = st.empty()
    
    with st.spinner("Scraping top resources for deeper content..."):
        try:
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800] if state['search_results'] else 'No search results'}"
                )]
            })
            state["scraped_content"] = reader_result['messages'][-1].content
            state["step2_success"] = True
            state["step2_error"] = None
            state["step2_time"] = datetime.now().isoformat()
        except Exception as e:
            state["step2_success"] = False
            state["step2_error"] = str(e)
            state["scraped_content"] = None
    
    with reader_placeholder.container():
        if state["step2_success"]:
            reader_status.markdown(
                '<span class="success-badge">✓ Completed</span>',
                unsafe_allow_html=True
            )
            with st.expander("📄 View Scraped Content", expanded=True):
                st.markdown(state["scraped_content"][:2000] + "...")
                st.caption(f"Full content length: {len(state['scraped_content'])} characters")
        else:
            reader_status.markdown(
                '<span class="error-badge">✗ Error</span>',
                unsafe_allow_html=True
            )
            st.error(f"Reader Agent Error: {state['step2_error']}")
            st.markdown("</div>", unsafe_allow_html=True)
            return state
    
    st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(0.3)
    
    # ========== STEP 3: Writer Chain ==========
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown("### Step 3: ✍️ Writer Chain")
    writer_col1, writer_col2 = st.columns([3, 1])
    
    writer_placeholder = writer_col1.empty()
    with writer_col2:
        writer_status = st.empty()
    
    with st.spinner("Generating comprehensive research report..."):
        try:
            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            state["step3_success"] = True
            state["step3_error"] = None
            state["step3_time"] = datetime.now().isoformat()
        except Exception as e:
            state["step3_success"] = False
            state["step3_error"] = str(e)
            state["report"] = None
    
    with writer_placeholder.container():
        if state["step3_success"]:
            writer_status.markdown(
                '<span class="success-badge">✓ Completed</span>',
                unsafe_allow_html=True
            )
            with st.expander("📄 View Draft Report", expanded=False):
                st.markdown(state["report"][:2000] + "...")
        else:
            writer_status.markdown(
                '<span class="error-badge">✗ Error</span>',
                unsafe_allow_html=True
            )
            st.error(f"Writer Chain Error: {state['step3_error']}")
            st.markdown("</div>", unsafe_allow_html=True)
            return state
    
    st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(0.3)
    
    # ========== STEP 4: Critic Chain ==========
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    st.markdown("### Step 4: 👨‍⚖️ Critic Chain")
    critic_col1, critic_col2 = st.columns([3, 1])
    
    critic_placeholder = critic_col1.empty()
    with critic_col2:
        critic_status = st.empty()
    
    with st.spinner("Evaluating report quality and accuracy..."):
        try:
            state["feedback"] = critic_chain.invoke({
                "report": state["report"]
            })
            state["step4_success"] = True
            state["step4_error"] = None
            state["step4_time"] = datetime.now().isoformat()
        except Exception as e:
            state["step4_success"] = False
            state["step4_error"] = str(e)
            state["feedback"] = None
    
    with critic_placeholder.container():
        if state["step4_success"]:
            critic_status.markdown(
                '<span class="success-badge">✓ Completed</span>',
                unsafe_allow_html=True
            )
            with st.expander("📋 View Critic Feedback", expanded=True):
                st.markdown(state["feedback"][:2000] + "...")
        else:
            critic_status.markdown(
                '<span class="error-badge">✗ Error</span>',
                unsafe_allow_html=True
            )
            st.error(f"Critic Chain Error: {state['step4_error']}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Cache the results
    if use_cache and state.get("step3_success"):
        cache.save(topic, state)
    
    return state


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_final_report(state: Dict[str, Any], topic: str):
    """Display the final research report with formatted output."""
    if state.get("step3_success") and state.get("report"):
        st.markdown("---")
        
        # Report Header
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"### 📊 Final Research Report")
        with col2:
            st.markdown(f"**Topic:** {topic}")
        with col3:
            st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        
        # Main Report
        st.markdown('<div class="report-container">', unsafe_allow_html=True)
        st.markdown(state["report"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Critic Feedback
        if state.get("step4_success") and state.get("feedback"):
            st.markdown('<div class="feedback-container">', unsafe_allow_html=True)
            st.markdown("### ⭐ Critic's Assessment")
            st.markdown("---")
            st.markdown(state["feedback"])
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Download Options
        st.markdown("---")
        st.markdown("### 📥 Download & Export")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            report_text = f"""
RESEARCH REPORT: {topic}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*80}

{state['report']}

{'='*80}
CRITIC FEEDBACK:
{state.get('feedback', 'No feedback available')}
"""
            st.download_button(
                label="📄 TXT",
                data=report_text,
                file_name=f"report_{topic.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📝 Markdown",
                data=state["report"],
                file_name=f"report_{topic.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col3:
            report_json = {
                "topic": topic,
                "generated_at": datetime.now().isoformat(),
                "report": state["report"],
                "feedback": state.get("feedback", ""),
                "search_results_length": len(state.get("search_results", "")),
                "content_length": len(state.get("scraped_content", ""))
            }
            st.download_button(
                label="📊 JSON",
                data=json.dumps(report_json, indent=2),
                file_name=f"report_{topic.replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col4:
            with st.popover("⚙️ More"):
                if st.button("🔄 New Search"):
                    st.session_state.regenerate = True


def display_sidebar():
    """Display sidebar with instructions, search history, and settings."""
    with st.sidebar:
        # --- Search History Section ---
        st.markdown("## 🕘 Search History")
        
        # Initialize search history in session state
        if "search_history" not in st.session_state:
            st.session_state.search_history = []
        
        if st.session_state.search_history:
            for i, item in enumerate(reversed(st.session_state.search_history)):
                col_h1, col_h2 = st.columns([4, 1])
                with col_h1:
                    if st.button(f"🔍 {item['topic'][:35]}{'...' if len(item['topic']) > 35 else ''}",
                                 key=f"hist_{i}", use_container_width=True):
                        st.session_state.pending_query = item['topic']
                        st.session_state.current_result = None
                        st.rerun()
                with col_h2:
                    st.markdown(f'<span class="history-time">{item["time"]}</span>',
                                unsafe_allow_html=True)
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.search_history = []
                st.session_state.current_result = None
                st.rerun()
        else:
            st.caption("No searches yet. Start researching!")
        
        st.markdown("---")
        
        # --- Quick Guide ---
        st.markdown("## 🎯 Quick Guide")
        st.markdown("""
        1. Enter a research topic
        2. Press **Enter** or click **Generate**
        3. Watch agents work in real-time
        4. Download results in multiple formats
        """)
        
        st.markdown("---")
        st.markdown("## ⚙️ Settings")
        
        use_cache = st.checkbox("Use cached results", value=True, 
                               help="Speed up repeated searches")
        
        auto_expand = st.checkbox("Auto-expand results", value=False,
                                 help="Show all sections expanded")
        
        st.markdown("---")
        st.markdown("## 📊 System Info")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Agents", "4", "Active")
        with col2:
            st.metric("Cache", "Enabled", "Ready")
        
        st.markdown("---")
        
        if st.button("🧹 Clear Cache", use_container_width=True):
            get_cache().clear()
            st.success("Cache cleared!")
        
        st.markdown("---")
        st.markdown("""
        ### 📚 System Overview
        Multi-Agent RAG System with 4 specialized agents:
        - 🔍 **Search Agent** - Finds information
        - 📖 **Reader Agent** - Scrapes content
        - ✍️ **Writer Chain** - Generates reports
        - 👨‍⚖️ **Critic Chain** - Evaluates quality
        """)
        
        st.markdown("---")
        st.markdown("""
        ### 📝 About
        **Version**: 1.0
        **Built with**: Streamlit, LangChain, Python
        """)
        
        return use_cache, auto_expand


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function."""
    
    # Header
    st.markdown("""
        <div class="header-container">
            <h1>🔬 Multi-Agent Research Assistant</h1>
            <p>AI-Powered Research Pipeline with Intelligent Agents</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = ""
    if "search_history" not in st.session_state:
        st.session_state.search_history = []
    if "current_result" not in st.session_state:
        st.session_state.current_result = None
    
    # Transfer pending query from suggestion or history click to the search input before rendering
    if st.session_state.pending_query:
        st.session_state.search_query = st.session_state.pending_query
        st.session_state.pending_query = ""
    
    # Sidebar
    use_cache, auto_expand = display_sidebar()
    
    # Main content
    st.markdown("---")
    
    # Search Form: enables pressing Enter to trigger search
    with st.form("search_form", border=False):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            research_topic = st.text_input(
                "🎯 Enter your research topic:",
                placeholder="e.g., 'Quantum Computing Applications', 'ESG in Tech', etc.",
                label_visibility="collapsed",
                key="search_query"
            )
        
        with col2:
            generate_btn = st.form_submit_button(
                "🚀 Generate",
                use_container_width=True, 
                type="primary"
            )
    
    # Suggestion chips below the search bar
    st.markdown("<p style='font-size:0.85rem; color:#6b7280; margin-top:-0.3rem; margin-bottom:0.4rem;'>💡 <b>Suggestions (click to fill search bar):</b></p>", unsafe_allow_html=True)
    suggestions = [
        "Quantum Computing Applications",
        "AI in Healthcare 2026",
        "Climate Change Solutions",
        "Blockchain in Finance",
        "Space Exploration Updates",
        "Cybersecurity Trends",
    ]
    
    st.markdown("<div style='margin-bottom:1rem;'>", unsafe_allow_html=True)
    suggestion_cols = st.columns(len(suggestions))
    for idx, suggestion in enumerate(suggestions):
        with suggestion_cols[idx]:
            if st.button(suggestion, key=f"sug_{idx}", use_container_width=True):
                st.session_state.pending_query = suggestion
                st.session_state.current_result = None
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process pipeline
    topic_to_search = research_topic.strip() if research_topic else ""
    
    if generate_btn and topic_to_search:
        # Add to search history if not identical to the most recent entry
        if not st.session_state.search_history or st.session_state.search_history[-1].get("topic") != topic_to_search:
            st.session_state.search_history.append({
                "topic": topic_to_search,
                "time": datetime.now().strftime("%H:%M")
            })
            # Keep only the last 20 items
            st.session_state.search_history = st.session_state.search_history[-20:]
        
        st.markdown("---")
        st.markdown("## 📊 Pipeline Execution")
        st.info("🚀 Starting research pipeline...")
        
        state = run_research_pipeline(topic_to_search, use_cache=use_cache)
        st.session_state.current_result = {"state": state, "topic": topic_to_search}
        
        if state.get("step3_success"):
            display_final_report(state, topic_to_search)
        else:
            st.error("❌ Pipeline execution failed. Check the errors above.")
    
    elif generate_btn and not topic_to_search:
        st.warning("⚠️ Please enter a research topic")
    
    elif st.session_state.get("current_result"):
        # Display existing report if page reruns (e.g., after downloading report or interacting with controls)
        cached_res = st.session_state.current_result
        if cached_res.get("state", {}).get("step3_success"):
            display_final_report(cached_res["state"], cached_res["topic"])
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #999; padding: 1rem 0; font-size: 0.9rem;">
            <p>🚀 Multi-Agent RAG Research System | Powered by Streamlit & LangChain</p>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()