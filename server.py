#!/usr/bin/env python3
"""
Nationalize.io MCP Server

Bu MCP server, Nationalize.io API'sini kullanarak verilen isimlere göre milliyet tahmini yapar.
"""

import asyncio
import json
import logging
from typing import Any, Sequence

import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)
from pydantic import BaseModel, Field

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
NATIONALIZE_API_URL = "https://api.nationalize.io"

class NationalityPrediction(BaseModel):
    """Milliyet tahmini modeli"""
    country_id: str = Field(description="Ülke kodu (örn: TR, US, DE)")
    probability: float = Field(description="Tahmin olasılığı (0-1 arası)")

class NationalizeResponse(BaseModel):
    """Nationalize API yanıt modeli"""
    name: str = Field(description="Sorgulanan isim")
    country: list[NationalityPrediction] = Field(description="Milliyet tahminleri listesi")

# MCP Server instance
server = Server("nationalize-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """Mevcut araçları listele"""
    return ListToolsResult(
        tools=[
            Tool(
                name="nationalize",
                description="Verilen isme göre milliyet tahmini yapar. Nationalize.io API'sini kullanır.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Milliyet tahmini yapılacak isim",
                            "minLength": 1
                        }
                    },
                    "required": ["name"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Araç çağrılarını işle"""

    if request.name != "nationalize":
        raise ValueError(f"Bilinmeyen araç: {request.name}")

    # Parametreleri al ve validate et
    if not request.arguments or "name" not in request.arguments:
        raise ValueError("'name' parametresi gerekli")

    name = request.arguments["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("'name' parametresi boş olmayan bir string olmalı")

    name = name.strip()

    try:
        # Nationalize.io API'sine istek at
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{NATIONALIZE_API_URL}/",
                params={"name": name},
                timeout=10.0
            )
            response.raise_for_status()

            data = response.json()

            # API yanıtını validate et
            if "name" not in data or "country" not in data:
                raise ValueError("API'den beklenmeyen yanıt formatı")

            # Yanıtı parse et
            nationality_response = NationalizeResponse(**data)

            # Sonuçları formatla
            if not nationality_response.country:
                result_text = f"'{name}' ismi için milliyet tahmini bulunamadı."
            else:
                result_text = f"'{name}' ismi için milliyet tahminleri:\n\n"

                # Tahminleri olasılığa göre sırala
                sorted_predictions = sorted(
                    nationality_response.country,
                    key=lambda x: x.probability,
                    reverse=True
                )

                for i, prediction in enumerate(sorted_predictions, 1):
                    percentage = prediction.probability * 100
                    result_text += f"{i}. {prediction.country_id}: %{percentage:.1f}\n"

                # En yüksek olasılıklı tahmini vurgula
                if sorted_predictions:
                    best_prediction = sorted_predictions[0]
                    result_text += f"\nEn olası milliyet: {best_prediction.country_id} (%{best_prediction.probability * 100:.1f})"

            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=result_text
                    )
                ]
            )

    except httpx.TimeoutException:
        raise ValueError("API isteği zaman aşımına uğradı")
    except httpx.HTTPStatusError as e:
        raise ValueError(f"API hatası: {e.response.status_code}")
    except httpx.RequestError as e:
        raise ValueError(f"Bağlantı hatası: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError("API'den geçersiz JSON yanıtı")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}")
        raise ValueError(f"İşlem sırasında hata oluştu: {str(e)}")

async def main():
    """Ana fonksiyon - MCP server'ı başlat"""
    logger.info("Nationalize MCP Server başlatılıyor...")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="nationalize-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(
                        tools_changed=False,
                        prompts_changed=False,
                        resources_changed=False,
                    ),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
