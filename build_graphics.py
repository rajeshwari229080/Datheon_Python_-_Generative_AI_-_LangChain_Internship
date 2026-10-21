"""
Generates high-definition, light-themed vector graphics (SVG) and high-res PNG
assets for GitHub README.md, central documentation, and LinkedIn showcase post.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)


def create_hero_svg():
    """Generates a modern light-theme hero banner SVG (1200x440)."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 440" width="100%" height="440">
  <defs>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC" />
      <stop offset="50%" stop-color="#EFF6FF" />
      <stop offset="100%" stop-color="#F5F3FF" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4F46E5" />
      <stop offset="50%" stop-color="#7C3AED" />
      <stop offset="100%" stop-color="#2563EB" />
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.06" />
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="1200" height="440" rx="20" fill="url(#heroBg)" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Subtle Grid Lines -->
  <g opacity="0.4" stroke="#CBD5E1" stroke-width="0.75" stroke-dasharray="3,3">
    <line x1="80" y1="0" x2="80" y2="440" />
    <line x1="280" y1="0" x2="280" y2="440" />
    <line x1="480" y1="0" x2="480" y2="440" />
    <line x1="680" y1="0" x2="680" y2="440" />
    <line x1="880" y1="0" x2="880" y2="440" />
    <line x1="1080" y1="0" x2="1080" y2="440" />
    <line x1="0" y1="80" x2="1200" y2="80" />
    <line x1="0" y1="200" x2="1200" y2="200" />
    <line x1="0" y1="320" x2="1200" y2="320" />
  </g>

  <!-- Top Status Pill -->
  <g transform="translate(60, 48)">
    <rect width="360" height="34" rx="17" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.2" filter="url(#cardShadow)" />
    <circle cx="20" cy="17" r="5" fill="#10B981" />
    <text x="34" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#4338CA" letter-spacing="0.5">APEX-AI SUITE • PRODUCTION VERIFIED</text>
  </g>

  <!-- Main Headline -->
  <text x="60" y="135" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="40" font-weight="800" fill="#0F172A" letter-spacing="-0.8">
    Generative AI &amp; LangChain Architecture
  </text>
  <text x="60" y="172" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="600" fill="#4F46E5">
    Enterprise-Grade Four-Pillar AI System
  </text>

  <!-- Subtitle Paragraph -->
  <text x="60" y="210" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="400" fill="#475569">
    A complete AI engineering implementation delivering robust JSON extractors, grounded document RAG,
  </text>
  <text x="60" y="232" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="400" fill="#475569">
    sandboxed autonomous ReAct agents, and interactive streaming chatbots with dual live &amp; deterministic offline modes.
  </text>

  <!-- Tech Badges -->
  <g transform="translate(60, 270)">
    <!-- Badge 1: Python -->
    <rect x="0" y="0" width="110" height="34" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)"/>
    <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#1E293B">🐍 Python 3.12</text>

    <!-- Badge 2: Pydantic v2 -->
    <rect x="122" y="0" width="125" height="34" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)"/>
    <text x="136" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#059669">⚡ Pydantic v2</text>

    <!-- Badge 3: FastAPI -->
    <rect x="259" y="0" width="105" height="34" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)"/>
    <text x="273" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#0284C7">🚀 FastAPI</text>

    <!-- Badge 4: Streamlit -->
    <rect x="376" y="0" width="115" height="34" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)"/>
    <text x="390" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#DC2626">🎈 Streamlit</text>

    <!-- Badge 5: LangChain -->
    <rect x="503" y="0" width="115" height="34" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)"/>
    <text x="517" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#7C3AED">🦜 LangChain</text>

    <!-- Badge 6: 32/32 Tests -->
    <rect x="630" y="0" width="150" height="34" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.2" filter="url(#cardShadow)"/>
    <text x="644" y="22" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#065F46">✅ 32/32 Tests Pass</text>
  </g>

  <!-- Metric Counter Cards on Right -->
  <g transform="translate(860, 48)">
    <!-- Metric Box 1 -->
    <rect x="0" y="0" width="280" height="100" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)" />
    <text x="24" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#64748B">AUTOMATED TEST SUITE</text>
    <text x="24" y="76" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="32" font-weight="800" fill="#059669">100%</text>
    <text x="120" y="74" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600" fill="#0F172A">32 Passed Across 4 Suites</text>

    <!-- Metric Box 2 -->
    <rect x="0" y="118" width="280" height="100" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)" />
    <text x="24" y="156" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#64748B">RAG GROUNDING CONFIDENCE</text>
    <text x="24" y="194" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="32" font-weight="800" fill="#4F46E5">0.45</text>
    <text x="110" y="192" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600" fill="#0F172A">Strict Abstention Gating</text>

    <!-- Metric Box 3 -->
    <rect x="0" y="236" width="280" height="100" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)" />
    <text x="24" y="274" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#64748B">AGENT SECURITY SANDBOX</text>
    <text x="24" y="312" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="32" font-weight="800" fill="#7C3AED">AST</text>
    <text x="100" y="310" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="600" fill="#0F172A">Zero Eval / Path Jailed</text>
  </g>

  <!-- Bottom Accent Stripe -->
  <rect x="0" y="434" width="1200" height="6" rx="3" fill="url(#accentGrad)" />
</svg>'''
    filepath = os.path.join(ASSETS_DIR, "hero_light.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Created: {filepath}")


def create_tasks_svg():
    """Generates the 4-Task Architecture Overview SVG (1200x520) in Light Theme."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="100%" height="520">
  <defs>
    <linearGradient id="gridBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="100%" stop-color="#F8FAFC" />
    </linearGradient>
    <filter id="taskShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.05" />
    </filter>
  </defs>

  <rect width="1200" height="520" rx="16" fill="url(#gridBg)" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Section Header -->
  <g transform="translate(60, 40)">
    <text x="0" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="800" fill="#0F172A">Four Production-Grade AI Engineering Pillars</text>
    <text x="0" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="400" fill="#64748B">Modular architectures built with deterministic fail-safes and enterprise testing standards.</text>
  </g>

  <!-- 4 Columns Container -->
  <!-- CARD 1: Task 1 -->
  <g transform="translate(60, 120)">
    <rect width="250" height="340" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#taskShadow)" />
    <rect width="250" height="6" rx="3" fill="#3B82F6" />
    <g transform="translate(20, 28)">
      <rect width="36" height="36" rx="8" fill="#EFF6FF" />
      <text x="18" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" text-anchor="middle">📄</text>
      <text x="46" y="23" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#2563EB">TASK 01</text>
      <text x="0" y="62" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Structured JSON</text>
      <text x="0" y="84" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">LLM Pipeline</text>

      <text x="0" y="118" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#475569">
        Extracts complex financial invoices &amp; resumes into validated Pydantic v2 schemas.
      </text>

      <!-- Key bullets -->
      <g transform="translate(0, 170)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">
        <text x="0" y="0">• Pydantic v2 Validation</text>
        <text x="0" y="22">• Multi-Pass JSON Healer</text>
        <text x="0" y="44">• FastAPI UI &amp; CLI Runner</text>
        <text x="0" y="66">• 11 Automated Pytests</text>
      </g>
    </g>
  </g>

  <!-- CARD 2: Task 2 -->
  <g transform="translate(335, 120)">
    <rect width="250" height="340" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#taskShadow)" />
    <rect width="250" height="6" rx="3" fill="#10B981" />
    <g transform="translate(20, 28)">
      <rect width="36" height="36" rx="8" fill="#ECFDF5" />
      <text x="18" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" text-anchor="middle">📚</text>
      <text x="46" y="23" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#059669">TASK 02</text>
      <text x="0" y="62" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Grounded RAG</text>
      <text x="0" y="84" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Document Q&amp;A</text>

      <text x="0" y="118" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#475569">
        Parses text and PDF policies with semantic chunking, dual vector store, &amp; citations.
      </text>

      <!-- Key bullets -->
      <g transform="translate(0, 170)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">
        <text x="0" y="0">• Recursive Semantic Chunker</text>
        <text x="0" y="22">• Cosine Vector Retrieval</text>
        <text x="0" y="44">• Zero-Hallucination Guard</text>
        <text x="0" y="66">• 5 Comprehensive Tests</text>
      </g>
    </g>
  </g>

  <!-- CARD 3: Task 3 -->
  <g transform="translate(610, 120)">
    <rect width="250" height="340" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#taskShadow)" />
    <rect width="250" height="6" rx="3" fill="#8B5CF6" />
    <g transform="translate(20, 28)">
      <rect width="36" height="36" rx="8" fill="#F5F3FF" />
      <text x="18" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" text-anchor="middle">🤖</text>
      <text x="46" y="23" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#7C3AED">TASK 03</text>
      <text x="0" y="62" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Autonomous ReAct</text>
      <text x="0" y="84" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Multi-Tool Agent</text>

      <text x="0" y="118" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#475569">
        Reasoning loop orchestrating calculator, jailed file reader, and web search tools.
      </text>

      <!-- Key bullets -->
      <g transform="translate(0, 170)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">
        <text x="0" y="0">• AST Calculator (No Eval)</text>
        <text x="0" y="22">• Jailed Workspace Security</text>
        <text x="0" y="44">• Execution Trace Logging</text>
        <text x="0" y="66">• 9 Security Tests Pass</text>
      </g>
    </g>
  </g>

  <!-- CARD 4: Task 4 -->
  <g transform="translate(885, 120)">
    <rect width="250" height="340" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2" filter="url(#taskShadow)" />
    <rect width="250" height="6" rx="3" fill="#EF4444" />
    <g transform="translate(20, 28)">
      <rect width="36" height="36" rx="8" fill="#FEF2F2" />
      <text x="18" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" text-anchor="middle">💬</text>
      <text x="46" y="23" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#DC2626">TASK 04</text>
      <text x="0" y="62" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Interactive Full-Stack</text>
      <text x="0" y="84" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#0F172A">Streamlit Bot</text>

      <text x="0" y="118" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#475569">
        Conversational interface with token streaming, persona presets, &amp; RAG adapters.
      </text>

      <!-- Key bullets -->
      <g transform="translate(0, 170)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">
        <text x="0" y="0">• Real-Time Token Stream</text>
        <text x="0" y="22">• Session State Isolation</text>
        <text x="0" y="44">• Markdown / JSON Export</text>
        <text x="0" y="66">• 7 Unit &amp; Adapter Tests</text>
      </g>
    </g>
  </g>
</svg>'''
    filepath = os.path.join(ASSETS_DIR, "tasks_overview_light.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Created: {filepath}")


def create_pipeline_svg():
    """Generates an end-to-end Pipeline Architecture SVG (1200x380) in Light Theme."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="100%" height="380">
  <defs>
    <linearGradient id="pipeBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC" />
      <stop offset="100%" stop-color="#EFF6FF" />
    </linearGradient>
    <filter id="pShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.06" />
    </filter>
  </defs>

  <rect width="1200" height="380" rx="16" fill="url(#pipeBg)" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Title -->
  <text x="60" y="50" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="800" fill="#0F172A">End-to-End Execution &amp; Integration Flow</text>
  <text x="60" y="74" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="400" fill="#64748B">How raw unstructured data flows through schema validation, retrieval grounding, and multi-agent loops.</text>

  <!-- Step 1: Input Document -->
  <g transform="translate(60, 110)">
    <rect width="220" height="200" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" filter="url(#pShadow)" />
    <rect width="220" height="5" rx="2.5" fill="#3B82F6" />
    <text x="20" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#2563EB">STEP 1 • INPUT INGESTION</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#0F172A">Raw Text &amp; PDF</text>
    <text x="20" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Financial Invoices</text>
    <text x="20" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Engineering Resumes</text>
    <text x="20" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Corporate Travel Policy</text>
    <rect x="20" y="152" width="180" height="26" rx="6" fill="#EFF6FF" />
    <text x="110" y="169" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#1D4ED8" text-anchor="middle">PDF &amp; Text Parsers</text>
  </g>

  <!-- Arrow 1 -->
  <path d="M 295 210 L 335 210 M 325 204 L 335 210 L 325 216" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />

  <!-- Step 2: Extraction & Vector Index -->
  <g transform="translate(350, 110)">
    <rect width="220" height="200" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" filter="url(#pShadow)" />
    <rect width="220" height="5" rx="2.5" fill="#10B981" />
    <text x="20" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#059669">STEP 2 • CHUNKING &amp; SCHEMAS</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#0F172A">Pydantic &amp; Vector</text>
    <text x="20" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Multi-Pass JSON Healer</text>
    <text x="20" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Recursive 500-char Chunker</text>
    <text x="20" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Cosine Vector Space</text>
    <rect x="20" y="152" width="180" height="26" rx="6" fill="#ECFDF5" />
    <text x="110" y="169" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#047857" text-anchor="middle">Validated Models</text>
  </g>

  <!-- Arrow 2 -->
  <path d="M 585 210 L 625 210 M 615 204 L 625 210 L 615 216" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />

  <!-- Step 3: ReAct Reasoning Loop -->
  <g transform="translate(640, 110)">
    <rect width="220" height="200" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" filter="url(#pShadow)" />
    <rect width="220" height="5" rx="2.5" fill="#8B5CF6" />
    <text x="20" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#7C3AED">STEP 3 • AGENT REASONING</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#0F172A">Sandboxed ReAct</text>
    <text x="20" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">AST Restricted Calculator</text>
    <text x="20" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Jailed Path File Reader</text>
    <text x="20" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">DuckDuckGo Search</text>
    <rect x="20" y="152" width="180" height="26" rx="6" fill="#F5F3FF" />
    <text x="110" y="169" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#6D28D9" text-anchor="middle">Execution Trace Guard</text>
  </g>

  <!-- Arrow 3 -->
  <path d="M 875 210 L 915 210 M 905 204 L 915 210 L 905 216" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />

  <!-- Step 4: Streamlit & Portal Interface -->
  <g transform="translate(930, 110)">
    <rect width="210" height="200" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" filter="url(#pShadow)" />
    <rect width="210" height="5" rx="2.5" fill="#EF4444" />
    <text x="20" y="36" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#DC2626">STEP 4 • CLIENT PORTAL</text>
    <text x="20" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="700" fill="#0F172A">SaaS &amp; Streamlit</text>
    <text x="20" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Token Stream Generator</text>
    <text x="20" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Session State Manager</text>
    <text x="20" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Central index.html Dashboard</text>
    <rect x="20" y="152" width="170" height="26" rx="6" fill="#FEF2F2" />
    <text x="105" y="169" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#B91C1C" text-anchor="middle">Interactive Portal</text>
  </g>
</svg>'''
    filepath = os.path.join(ASSETS_DIR, "pipeline_architecture_light.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Created: {filepath}")


def create_linkedin_svg():
    """Generates the dedicated LinkedIn showcase graphic in SVG format (1200x675)."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="100%" height="675">
  <defs>
    <linearGradient id="linkedBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC" />
      <stop offset="60%" stop-color="#F1F5F9" />
      <stop offset="100%" stop-color="#E2E8F0" />
    </linearGradient>
    <linearGradient id="linkedBanner" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3B82F6" />
      <stop offset="50%" stop-color="#6366F1" />
      <stop offset="100%" stop-color="#8B5CF6" />
    </linearGradient>
    <filter id="lShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="#0F172A" flood-opacity="0.08" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="675" fill="url(#linkedBg)" />

  <!-- Top Accent Bar -->
  <rect width="1200" height="10" fill="url(#linkedBanner)" />

  <!-- Main Card Container -->
  <rect x="50" y="45" width="1100" height="585" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2" filter="url(#lShadow)" />

  <!-- Header Header -->
  <g transform="translate(90, 85)">
    <!-- Brand Pill -->
    <rect width="260" height="32" rx="16" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.2" />
    <circle cx="16" cy="16" r="4.5" fill="#4F46E5" />
    <text x="28" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#4338CA" letter-spacing="0.5">PROJECT SHOWCASE • GENAI</text>

    <!-- Main Title -->
    <text x="0" y="75" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="34" font-weight="800" fill="#0F172A" letter-spacing="-0.5">
      ApexAI Engineering Suite
    </text>
    <text x="0" y="105" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="600" fill="#4F46E5">
      Production Generative AI &amp; Autonomous Multi-Tool Systems
    </text>
    <text x="0" y="135" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="400" fill="#64748B">
      Full-stack architecture featuring Pydantic JSON extraction, grounded RAG, AST-safe agents, and Streamlit.
    </text>
  </g>

  <!-- Right Badges -->
  <g transform="translate(860, 85)">
    <rect width="250" height="95" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2" />
    <text x="20" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#64748B">VERIFIED COVERAGE</text>
    <text x="20" y="70" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="30" font-weight="800" fill="#059669">32 / 32</text>
    <text x="135" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="600" fill="#0F172A">Tests Passing Cleanly</text>
  </g>

  <!-- 4 Feature Mini-Cards -->
  <!-- Card 1 -->
  <g transform="translate(90, 255)">
    <rect width="240" height="230" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2" />
    <rect width="240" height="4" rx="2" fill="#3B82F6" />
    <g transform="translate(18, 24)">
      <text x="0" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20">📑</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#2563EB">TASK 1</text>
      <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Structured JSON</text>
      <text x="0" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Self-healing parser</text>
      <text x="0" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Pydantic v2 schemas</text>
      <text x="0" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Invoices &amp; Resumes</text>
      <rect x="0" y="120" width="120" height="24" rx="6" fill="#DBEAFE" />
      <text x="60" y="136" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#1D4ED8" text-anchor="middle">FastAPI + CLI</text>
    </g>
  </g>

  <!-- Card 2 -->
  <g transform="translate(355, 255)">
    <rect width="240" height="230" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2" />
    <rect width="240" height="4" rx="2" fill="#10B981" />
    <g transform="translate(18, 24)">
      <text x="0" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20">📖</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#059669">TASK 2</text>
      <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Grounded RAG</text>
      <text x="0" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">PDF &amp; Text Parsing</text>
      <text x="0" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Cosine Vector Search</text>
      <text x="0" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Strict Abstention Rule</text>
      <rect x="0" y="120" width="130" height="24" rx="6" fill="#D1FAE5" />
      <text x="65" y="136" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#047857" text-anchor="middle">Zero Hallucination</text>
    </g>
  </g>

  <!-- Card 3 -->
  <g transform="translate(620, 255)">
    <rect width="240" height="230" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2" />
    <rect width="240" height="4" rx="2" fill="#8B5CF6" />
    <g transform="translate(18, 24)">
      <text x="0" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20">⚙️</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#7C3AED">TASK 3</text>
      <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#0F172A">ReAct AI Agent</text>
      <text x="0" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">AST Math (No Eval)</text>
      <text x="0" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Jailed Path Security</text>
      <text x="0" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">DuckDuckGo Search</text>
      <rect x="0" y="120" width="130" height="24" rx="6" fill="#EDE9FE" />
      <text x="65" y="136" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#6D28D9" text-anchor="middle">Autonomous Safe</text>
    </g>
  </g>

  <!-- Card 4 -->
  <g transform="translate(885, 255)">
    <rect width="240" height="230" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2" />
    <rect width="240" height="4" rx="2" fill="#EF4444" />
    <g transform="translate(18, 24)">
      <text x="0" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20">💬</text>
      <text x="32" y="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#DC2626">TASK 4</text>
      <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="700" fill="#0F172A">Streamlit Bot</text>
      <text x="0" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Real-Time Streaming</text>
      <text x="0" y="80" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Session Isolation</text>
      <text x="0" y="96" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" fill="#64748B">Persona System</text>
      <rect x="0" y="120" width="130" height="24" rx="6" fill="#FEE2E2" />
      <text x="65" y="136" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#B91C1C" text-anchor="middle">Full-Stack Chat</text>
    </g>
  </g>

  <!-- Footer Banner -->
  <g transform="translate(90, 520)">
    <rect width="1020" height="55" rx="10" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1" />
    <text x="24" y="33" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="#1E293B">GitHub Repository:</text>
    <text x="170" y="33" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="500" fill="#4F46E5">github.com/rajeshwari229080/Python-Generative-AI-LangChain-Internship</text>
    <rect x="880" y="12" width="116" height="30" rx="6" fill="#4F46E5" />
    <text x="938" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">EXPLORE CODE</text>
  </g>
</svg>'''
    filepath = os.path.join(ASSETS_DIR, "linkedin_post.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Created: {filepath}")


def create_png_showcase():
    """Renders a high-resolution, light-themed PNG showcase using PIL."""
    w, h = 1200, 675
    img = Image.new("RGB", (w, h), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Gradient-like top accent bar
    for x in range(w):
        r = int(59 + (139 - 59) * (x / w))
        g = int(130 + (92 - 130) * (x / w))
        b = int(246 + (246 - 246) * (x / w))
        draw.line([(x, 0), (x, 10)], fill=(r, g, b))

    # Inner White Canvas Card
    draw.rounded_rectangle([(40, 35), (1160, 640)], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

    # Use default or basic fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_sub = ImageFont.truetype("arialbd.ttf", 18)
        font_body = ImageFont.truetype("arial.ttf", 14)
        font_pill = ImageFont.truetype("arialbd.ttf", 12)
        font_card_title = ImageFont.truetype("arialbd.ttf", 16)
        font_card_sub = ImageFont.truetype("arial.ttf", 12)
        font_stat_num = ImageFont.truetype("arialbd.ttf", 28)
    except Exception:
        font_title = font_sub = font_body = font_pill = font_card_title = font_card_sub = font_stat_num = ImageFont.load_default()

    # Pill
    draw.rounded_rectangle([(70, 65), (320, 95)], radius=14, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw.ellipse([(85, 76), (93, 84)], fill=(79, 70, 229))
    draw.text((102, 73), "APEX-AI • SYSTEM SHOWCASE", fill=(67, 56, 202), font=font_pill)

    # Titles
    draw.text((70, 115), "ApexAI Engineering Operations Suite", fill=(15, 23, 42), font=font_title)
    draw.text((70, 158), "Production Generative AI, RAG & Autonomous Multi-Tool Systems", fill=(79, 70, 229), font=font_sub)
    draw.text((70, 190), "End-to-end Python 3.12 architecture with Pydantic v2 validation, AST sandbox, and Streamlit.", fill=(100, 116, 139), font=font_body)

    # Right Stat Badge
    draw.rounded_rectangle([(870, 65), (1130, 160)], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((890, 80), "AUTOMATED TEST SUITE", fill=(100, 116, 139), font=font_pill)
    draw.text((890, 105), "32 / 32", fill=(5, 150, 105), font=font_stat_num)
    draw.text((1000, 112), "100% Passing", fill=(15, 23, 42), font=font_sub)

    # 4 Cards
    cards_data = [
        {"num": "TASK 1", "title": "Structured JSON", "color": (59, 130, 246), "items": ["Pydantic v2 schemas", "Multi-pass healer", "Invoices & Resumes", "FastAPI + CLI"]},
        {"num": "TASK 2", "title": "Grounded RAG", "color": (16, 185, 129), "items": ["PDF & text ingestion", "Cosine similarity", "Page-level citations", "Strict abstention"]},
        {"num": "TASK 3", "title": "ReAct Agent", "color": (139, 92, 246), "items": ["AST math (no eval)", "Jailed file reader", "DuckDuckGo search", "Trace audit log"]},
        {"num": "TASK 4", "title": "Streamlit Bot", "color": (239, 68, 68), "items": ["Real-time streaming", "Session isolation", "Persona switching", "Markdown export"]},
    ]

    card_w = 245
    card_gap = 20
    start_x = 70
    start_y = 240

    for i, c in enumerate(cards_data):
        cx = start_x + i * (card_w + card_gap)
        draw.rounded_rectangle([(cx, start_y), (cx + card_w, start_y + 270)], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        # Top color bar
        draw.rounded_rectangle([(cx, start_y), (cx + card_w, start_y + 6)], radius=3, fill=c["color"])
        # Task Pill
        draw.text((cx + 18, start_y + 22), c["num"], fill=c["color"], font=font_pill)
        draw.text((cx + 18, start_y + 44), c["title"], fill=(15, 23, 42), font=font_card_title)

        y_offset = start_y + 85
        for item in c["items"]:
            draw.text((cx + 18, y_offset), f"• {item}", fill=(71, 85, 105), font=font_card_sub)
            y_offset += 24

        # Pill at bottom
        draw.rounded_rectangle([(cx + 18, start_y + 215), (cx + card_w - 18, start_y + 245)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        draw.text((cx + 30, start_y + 223), "Production Ready", fill=(30, 41, 59), font=font_pill)

    # Bottom link ribbon
    draw.rounded_rectangle([(70, 545), (1130, 605)], radius=10, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((90, 568), "GitHub Repository: https://github.com/rajeshwari229080/Python-Generative-AI-LangChain-Internship", fill=(15, 23, 42), font=font_sub)

    # Save to root as image.png and in assets/
    root_png = os.path.join(BASE_DIR, "image.png")
    assets_png = os.path.join(ASSETS_DIR, "linkedin_post.png")
    img.save(root_png, format="PNG")
    img.save(assets_png, format="PNG")
    print(f"Created: {root_png}")
    print(f"Created: {assets_png}")


if __name__ == "__main__":
    create_hero_svg()
    create_tasks_svg()
    create_pipeline_svg()
    create_linkedin_svg()
    create_png_showcase()
