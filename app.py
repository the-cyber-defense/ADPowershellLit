import streamlit as st
import subprocess
import os
import tempfile

st.set_page_config(page_title="PowerShell Toolkit", layout="wide")
st.title("💻 PowerShell Toolkit for Admins")

TOOLS = {
    "Microsoft Teams Utility": "Teams.ps1",
    "SharePoint Migration Tool (SPMT)": "SPMT.ps1",
    "SharePoint Online (SPO)": "SPO.ps1",
    "Sync Agent": "SyncAgent.ps1"
}

tool = st.selectbox("Select PowerShell Script", list(TOOLS.keys()))
custom_args = st.text_input("Optional: Add script arguments (e.g., -SiteUrl https://...)")

uploaded_config = st.file_uploader("Upload Config File (optional)", type=["json", "pfx"])

if st.button("Run Script"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ps1") as tmp_script:
        script_path = TOOLS[tool]
        tmp_script.write(open(script_path, 'rb').read())
        tmp_script_path = tmp_script.name

    cmd = ["pwsh", "-ExecutionPolicy", "Bypass", "-File", tmp_script_path]

    if custom_args:
        cmd += custom_args.split()

    if uploaded_config:
        config_path = os.path.join(tempfile.gettempdir(), uploaded_config.name)
        with open(config_path, "wb") as f:
            f.write(uploaded_config.read())
        st.write(f"📄 Config file saved to: `{config_path}`")

    st.write("⚙️ Running script...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    st.subheader("📄 Output:")
    st.code(result.stdout, language='powershell')

    if result.stderr:
        st.subheader("❌ Errors:")
        st.error(result.stderr)
    else:
        st.success("✅ Script executed successfully.")
