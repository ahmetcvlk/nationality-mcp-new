#!/usr/bin/env python3
"""
Nationalize MCP Server Integration Test

Bu script, gerçek API ile entegrasyon testi yapar.
"""

import asyncio
from server import handle_call_tool, handle_list_tools

# Basit mock request class
class MockCallToolRequest:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

async def test_real_api():
    """Gerçek API ile test"""
    print("🔍 Gerçek API ile test ediliyor...")
    
    try:
        # Tools listesini test et
        tools_result = await handle_list_tools()
        print(f"✅ {len(tools_result.tools)} tool bulundu")
        
        # Gerçek API çağrısı
        request = MockCallToolRequest(
            name="nationalize",
            arguments={"name": "Ahmet"}
        )
        
        result = await handle_call_tool(request)
        
        print("📊 API Yanıtı:")
        print(result.content[0].text)
        print("✅ Gerçek API testi başarılı")
        
    except Exception as e:
        print(f"❌ Test başarısız: {str(e)}")
        return False
    
    return True

async def test_invalid_name():
    """Geçersiz isim testi"""
    print("\n🔍 Geçersiz isim testi...")
    
    try:
        request = MockCallToolRequest(
            name="nationalize",
            arguments={"name": ""}
        )
        
        await handle_call_tool(request)
        print("❌ Hata bekleniyor")
        return False
        
    except ValueError as e:
        print(f"✅ Beklenen hata: {str(e)}")
        return True
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {str(e)}")
        return False

async def main():
    """Ana test fonksiyonu"""
    print("🚀 Nationalize MCP Server Integration Test\n")
    
    tests = [
        ("Gerçek API Testi", test_real_api),
        ("Geçersiz İsim Testi", test_invalid_name)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"📋 {test_name}")
        try:
            success = await test_func()
            if success:
                passed += 1
                print("✅ Başarılı\n")
            else:
                print("❌ Başarısız\n")
        except Exception as e:
            print(f"❌ Test hatası: {str(e)}\n")
    
    print(f"📊 Sonuç: {passed}/{total} test başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı!")
    else:
        print("⚠️ Bazı testler başarısız!")

if __name__ == "__main__":
    asyncio.run(main())
