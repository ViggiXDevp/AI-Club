import sys
import json

def handle_request(data):
    method = data.get("method")
    
    if method == "tools/list":
        return {"tools": [{"name": "calculate", "description": "Math calculator"}]}
    elif method == "resources/list":
        return {"resources": [{"uri": "config://operations"}]}
    elif method == "resource/read":
        if data.get("params", {}).get("uri") == "config://operations":
            return {"supported": ["add", "subtract", "multiply", "divide"]}
    elif method == "tool/call":
        params = data.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if name == "calculate":
            op = arguments.get("operation")
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            
            if op == "add": result = a + b
            elif op == "subtract": result = a - b
            elif op == "multiply": result = a * b
            elif op == "divide":
                if b == 0: return {"error": "Division by zero"}
                result = a / b
            else: return {"error": "Invalid operation"}
            
            return {"result": result, "expression": f"{a} {op} {b} = {result}"}
    
    return {"error": "Unknown method"}

# FIXED MAIN LOOP - handles empty lines
while True:
    line = sys.stdin.readline().rstrip('\n')
    if not line:
        continue
        
    try:
        request = json.loads(line)
        response = {
            "jsonrpc": "2.0", 
            "id": request.get("id", 0),
            "result": handle_request(request)
        }
        sys.stdout.write(json.dumps(response) + '\n')
        sys.stdout.flush()
    except json.JSONDecodeError:
        continue
    except Exception as e:
        sys.stdout.write(json.dumps({
            "jsonrpc": "2.0", 
            "id": 0, 
            "error": {"message": str(e)}
        }) + '\n')
        sys.stdout.flush()
