#!/usr/bin/env python3
"""
Manuel test scripti - Farklı isimlerle test et
"""

import asyncio
from server import handle_call_tool

class MockCallToolRequest:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

async def test_name(name):
    """Verilen ismi test et"""
    print(f"\n🔍 '{name}' ismi test ediliyor...")
    
    try:
        request = MockCallToolRequest(
            name="nationalize",
            arguments={"name": name}
        )
        
        result = await handle_call_tool(request)
        print("📊 Sonuç:")
        print(result.content[0].text)
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")

async def main():
    """Farklı isimlerle test et"""
    print("🚀 Nationalize MCP Server Manuel Test")
    
    test_names = [
        "Ahmet",
        "Maria", 
        "John",
        "Yuki",
        "Mohammed",
        "Anna",
        "Pierre",
        "Chen"
    ]
    
    for name in test_names:
        await test_name(name)
        await asyncio.sleep(0.5)  # API rate limit için bekle

if __name__ == "__main__":
    asyncio.run(main())
