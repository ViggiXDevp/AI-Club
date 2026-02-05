import subprocess
import json
import sys

def send_mcp_request(proc, request):
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())

def test_mcp():
    print("👤 Testing MCP Server...")
    
    # Start server
    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    # 1. DISCOVERY
    print("🔍 1. DISCOVERY...")
    tools_resp = send_mcp_request(proc, {"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    print(f"   Tools: {len(tools_resp['result']['tools'])} found")
    
    resource_resp = send_mcp_request(proc, {"jsonrpc": "2.0", "method": "resources/list", "id": 2})
    print(f"   Resources: {len(resource_resp['result']['resources'])} found")
    
    # 2. RESOURCE
    print("📄 2. RESOURCE...")
    config_resp = send_mcp_request(proc, {
        "jsonrpc": "2.0", 
        "method": "resource/read", 
        "params": {"uri": "config://operations"},
        "id": 3
    })
    print(f"   Config: {json.dumps(config_resp['result'], indent=2)}")
    
    # 3. TOOL CALL
    print("🧮 3. TOOL CALL...")
    tool_resp = send_mcp_request(proc, {
        "jsonrpc": "2.0",
        "method": "tool/call",
        "params": {
            "name": "calculate",
            "arguments": {"operation": "multiply", "a": 15, "b": 3}
        },
        "id": 4
    })
    print(f"✅ RESULT: {json.dumps(tool_resp['result'], indent=2)}")
    
    proc.terminate()
    print("🎉 SUCCESS - All MCP features working!")

if __name__ == "__main__":
    test_mcp()

