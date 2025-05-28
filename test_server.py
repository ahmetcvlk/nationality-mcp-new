#!/usr/bin/env python3
"""
Nationalize MCP Server Test Script

Bu script, MCP server'ın temel fonksiyonalitesini test eder.
"""

import asyncio
import json
import sys
from unittest.mock import AsyncMock, patch

import httpx

# Test için server modülünü import et
from server import handle_call_tool, handle_list_tools

# Basit mock request class
class MockCallToolRequest:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

async def test_list_tools():
    """Tools listesini test et"""
    print("🔍 Tools listesi test ediliyor...")

    result = await handle_list_tools()

    assert len(result.tools) == 1
    assert result.tools[0].name == "nationalize"
    assert "milliyet tahmini" in result.tools[0].description

    print("✅ Tools listesi testi başarılı")

async def test_nationalize_tool_success():
    """Başarılı nationalize tool çağrısını test et"""
    print("🔍 Başarılı nationalize tool çağrısı test ediliyor...")

    # Mock API yanıtı
    mock_response_data = {
        "name": "Ahmet",
        "country": [
            {"country_id": "TR", "probability": 0.892},
            {"country_id": "AZ", "probability": 0.051},
            {"country_id": "KZ", "probability": 0.032}
        ]
    }

    # HTTP client'ı mock'la
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = AsyncMock()

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

        # Tool'u çağır
        request = MockCallToolRequest(
            name="nationalize",
            arguments={"name": "Ahmet"}
        )

        result = await handle_call_tool(request)

        # Sonucu kontrol et
        assert len(result.content) == 1
        assert result.content[0].type == "text"
        assert "Ahmet" in result.content[0].text
        assert "TR: %89.2" in result.content[0].text
        assert "En olası milliyet: TR" in result.content[0].text

    print("✅ Başarılı nationalize tool çağrısı testi başarılı")

async def test_nationalize_tool_invalid_name():
    """Geçersiz isim ile tool çağrısını test et"""
    print("🔍 Geçersiz isim ile tool çağrısı test ediliyor...")

    # Boş isim
    request = MockCallToolRequest(
        name="nationalize",
        arguments={"name": ""}
    )

    try:
        await handle_call_tool(request)
        assert False, "Hata bekleniyor"
    except ValueError as e:
        assert "boş olmayan" in str(e)

    # İsim parametresi yok
    request = MockCallToolRequest(
        name="nationalize",
        arguments={}
    )

    try:
        await handle_call_tool(request)
        assert False, "Hata bekleniyor"
    except ValueError as e:
        assert "gerekli" in str(e)

    print("✅ Geçersiz isim ile tool çağrısı testi başarılı")

async def test_nationalize_tool_api_error():
    """API hata durumunu test et"""
    print("🔍 API hata durumu test ediliyor...")

    # HTTP hatasını mock'la
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.HTTPStatusError(
            "API Error", request=None, response=AsyncMock(status_code=500)
        )

        request = MockCallToolRequest(
            name="nationalize",
            arguments={"name": "Test"}
        )

        try:
            await handle_call_tool(request)
            assert False, "Hata bekleniyor"
        except ValueError as e:
            assert "API hatası" in str(e)

    print("✅ API hata durumu testi başarılı")

async def test_nationalize_tool_no_results():
    """Sonuç bulunamayan durumu test et"""
    print("🔍 Sonuç bulunamayan durum test ediliyor...")

    # Boş sonuç mock'la
    mock_response_data = {
        "name": "XYZ123",
        "country": []
    }

    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = AsyncMock()

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

        request = MockCallToolRequest(
            name="nationalize",
            arguments={"name": "XYZ123"}
        )

        result = await handle_call_tool(request)

        assert "bulunamadı" in result.content[0].text

    print("✅ Sonuç bulunamayan durum testi başarılı")

async def main():
    """Tüm testleri çalıştır"""
    print("🚀 Nationalize MCP Server testleri başlatılıyor...\n")

    tests = [
        test_list_tools,
        test_nationalize_tool_success,
        test_nationalize_tool_invalid_name,
        test_nationalize_tool_api_error,
        test_nationalize_tool_no_results
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            await test()
            passed += 1
            print()
        except Exception as e:
            print(f"❌ Test başarısız: {test.__name__}")
            print(f"   Hata: {str(e)}\n")
            failed += 1

    print(f"📊 Test Sonuçları:")
    print(f"   ✅ Başarılı: {passed}")
    print(f"   ❌ Başarısız: {failed}")
    print(f"   📈 Toplam: {passed + failed}")

    if failed == 0:
        print("\n🎉 Tüm testler başarılı!")
        return 0
    else:
        print(f"\n⚠️  {failed} test başarısız!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
