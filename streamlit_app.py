"""Gemini-to-Claude Data Transfer Webapp.

A Streamlit application that fetches data from Google Gemini
and transfers it to Anthropic Claude for further processing.
"""

import streamlit as st

from gemini_client import configure_gemini, generate_content
from claude_client import (
    CLAUDE_MODELS,
    create_client,
    send_to_claude,
    transfer_with_context,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Gemini → Claude Transfer",
    page_icon="🔄",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar – API keys & model selection
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🔑 API Configuration")

    gemini_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Get your key at https://aistudio.google.com/apikey",
    )
    claude_key = st.text_input(
        "Anthropic Claude API Key",
        type="password",
        help="Get your key at https://console.anthropic.com/settings/keys",
    )

    st.divider()
    st.header("🤖 Model Selection")

    gemini_model = st.text_input(
        "Gemini Model",
        value="gemini-2.0-flash",
        help="e.g. gemini-2.0-flash, gemini-2.5-pro",
    )
    claude_model = st.selectbox(
        "Claude Model",
        options=CLAUDE_MODELS,
        index=1,
        help="Select the Claude model to receive the data",
    )

    st.divider()
    st.header("⚙️ Settings")
    max_tokens = st.slider(
        "Claude Max Tokens",
        min_value=256,
        max_value=8192,
        value=4096,
        step=256,
    )

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.title("🔄 Gemini → Claude Data Transfer")
st.write(
    "Send a prompt to **Google Gemini**, review the response, "
    "then transfer it to **Anthropic Claude** for further processing."
)

# Tabs for different workflows
tab_transfer, tab_direct, tab_history = st.tabs(
    ["📤 Transfer", "💬 Direct Compare", "📋 History"]
)

# ---- Session state initialisation ----------------------------------------
if "transfer_history" not in st.session_state:
    st.session_state.transfer_history = []

# ========================== TAB 1 – Transfer ==============================
with tab_transfer:
    st.subheader("Step 1 – Query Gemini")
    gemini_prompt = st.text_area(
        "Prompt for Gemini",
        height=120,
        placeholder="Enter the prompt you want to send to Gemini…",
        key="gemini_prompt",
    )

    col_gemini_btn, _ = st.columns([1, 3])
    with col_gemini_btn:
        run_gemini = st.button("🚀 Send to Gemini", use_container_width=True)

    # ---- Gemini call ------------------------------------------------------
    if run_gemini:
        if not gemini_key:
            st.error("Please enter your Gemini API key in the sidebar.")
        elif not gemini_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Waiting for Gemini…"):
                try:
                    configure_gemini(gemini_key)
                    result = generate_content(gemini_model, gemini_prompt)
                    st.session_state["gemini_response"] = result
                except Exception as exc:
                    st.error(f"Gemini error: {exc}")

    # ---- Show Gemini response ---------------------------------------------
    gemini_response = st.session_state.get("gemini_response", "")
    if gemini_response:
        st.subheader("Gemini Response")
        st.markdown(gemini_response)

        st.divider()
        st.subheader("Step 2 – Transfer to Claude")

        transfer_instruction = st.text_area(
            "Instructions for Claude",
            height=100,
            value="Analyze, refine, and improve the following response. "
            "Fix any inaccuracies and add any missing information.",
            key="transfer_instruction",
            help="Tell Claude what to do with the Gemini data.",
        )

        col_claude_btn, _ = st.columns([1, 3])
        with col_claude_btn:
            run_claude = st.button(
                "🔄 Transfer to Claude", use_container_width=True
            )

        if run_claude:
            if not claude_key:
                st.error("Please enter your Claude API key in the sidebar.")
            else:
                with st.spinner("Transferring to Claude…"):
                    try:
                        client = create_client(claude_key)
                        claude_response = transfer_with_context(
                            client=client,
                            model=claude_model,
                            gemini_prompt=gemini_prompt,
                            gemini_response=gemini_response,
                            transfer_instruction=transfer_instruction,
                            max_tokens=max_tokens,
                        )
                        st.session_state["claude_response"] = claude_response

                        # Save to history
                        st.session_state.transfer_history.append(
                            {
                                "prompt": gemini_prompt,
                                "gemini": gemini_response,
                                "instruction": transfer_instruction,
                                "claude": claude_response,
                            }
                        )
                    except Exception as exc:
                        st.error(f"Claude error: {exc}")

    # ---- Show Claude response ---------------------------------------------
    claude_resp = st.session_state.get("claude_response", "")
    if claude_resp:
        st.subheader("Claude Response")
        st.markdown(claude_resp)

        # Side-by-side comparison
        st.divider()
        st.subheader("📊 Side-by-Side Comparison")
        col_g, col_c = st.columns(2)
        with col_g:
            st.markdown("**Gemini**")
            st.info(gemini_response)
        with col_c:
            st.markdown("**Claude**")
            st.success(claude_resp)

# ====================== TAB 2 – Direct Compare ============================
with tab_direct:
    st.subheader("Send the same prompt to both models")

    compare_prompt = st.text_area(
        "Prompt",
        height=120,
        placeholder="Enter a prompt to send to both Gemini and Claude…",
        key="compare_prompt",
    )

    col_compare_btn, _ = st.columns([1, 3])
    with col_compare_btn:
        run_compare = st.button("⚡ Run Both", use_container_width=True)

    if run_compare:
        if not gemini_key or not claude_key:
            st.error("Both API keys are required for comparison.")
        elif not compare_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("### Gemini")
                with st.spinner("Querying Gemini…"):
                    try:
                        configure_gemini(gemini_key)
                        g_resp = generate_content(gemini_model, compare_prompt)
                        st.markdown(g_resp)
                    except Exception as exc:
                        g_resp = ""
                        st.error(f"Gemini error: {exc}")

            with col_right:
                st.markdown("### Claude")
                with st.spinner("Querying Claude…"):
                    try:
                        client = create_client(claude_key)
                        c_resp = send_to_claude(
                            client=client,
                            model=claude_model,
                            system_prompt="",
                            user_message=compare_prompt,
                            max_tokens=max_tokens,
                        )
                        st.markdown(c_resp)
                    except Exception as exc:
                        c_resp = ""
                        st.error(f"Claude error: {exc}")

            if g_resp and c_resp:
                st.session_state.transfer_history.append(
                    {
                        "prompt": compare_prompt,
                        "gemini": g_resp,
                        "instruction": "(direct comparison)",
                        "claude": c_resp,
                    }
                )

# ======================== TAB 3 – History ==================================
with tab_history:
    st.subheader("Transfer History")

    if not st.session_state.transfer_history:
        st.info("No transfers yet. Use the Transfer or Direct Compare tab.")
    else:
        for idx, entry in enumerate(
            reversed(st.session_state.transfer_history), 1
        ):
            with st.expander(
                f"#{idx} — {entry['prompt'][:80]}…"
                if len(entry["prompt"]) > 80
                else f"#{idx} — {entry['prompt']}"
            ):
                st.markdown(f"**Prompt:** {entry['prompt']}")
                st.markdown(f"**Instruction:** {entry['instruction']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Gemini**")
                    st.info(entry["gemini"])
                with col_b:
                    st.markdown("**Claude**")
                    st.success(entry["claude"])

        if st.button("🗑️ Clear History"):
            st.session_state.transfer_history = []
            st.rerun()
