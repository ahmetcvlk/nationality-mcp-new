[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/ahmetcvlk-nationality-mcp-new-badge.png)](https://mseep.ai/app/ahmetcvlk-nationality-mcp-new)

# Nationalize.io MCP Server

Bu MCP (Model Context Protocol) server, [Nationalize.io API](https://nationalize.io)'sini kullanarak verilen isimlere göre milliyet tahmini yapar.

## Özellikler

- **nationalize** tool'u: İsim alıp milliyet tahmini döndürür
- Async HTTP istekleri
- Hata yönetimi ve validasyon
- Olasılık bazlı sıralama
- Türkçe kullanıcı arayüzü

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. MCP server'ı çalıştırın:
```bash
python server.py
```

## Kullanım

### nationalize Tool

Verilen isme göre milliyet tahmini yapar.

**Parametreler:**
- `name` (string, gerekli): Milliyet tahmini yapılacak isim

**Örnek kullanım:**
```json
{
  "name": "nationalize",
  "arguments": {
    "name": "Ahmet"
  }
}
```

**Örnek çıktı:**
```
'Ahmet' ismi için milliyet tahminleri:

1. TR: %89.2
2. AZ: %5.1
3. KZ: %3.2
4. UZ: %2.5

En olası milliyet: TR (%89.2)
```

## API Hakkında

Bu server, [Nationalize.io](https://nationalize.io) API'sini kullanır. API, makine öğrenmesi algoritmaları kullanarak isimlere göre milliyet tahmini yapar.

### API Özellikleri:
- Ücretsiz kullanım (günlük limit var)
- 70+ ülke desteği
- Olasılık bazlı tahminler
- Hızlı yanıt süresi

## Hata Yönetimi

Server aşağıdaki hata durumlarını handle eder:
- Geçersiz parametreler
- API bağlantı hataları
- Zaman aşımı
- Geçersiz JSON yanıtları
- Beklenmeyen API yanıtları

## MCP Client Konfigürasyonu

MCP client'ınızda bu server'ı kullanmak için `mcp_config.json` dosyasını kullanabilirsiniz:

```json
{
  "mcpServers": {
    "nationalize": {
      "command": "python",
      "args": ["server.py"],
      "cwd": ".",
      "env": {}
    }
  }
}
```

## Geliştirme

### Test Etme

Server'ı test etmek için:

1. **Entegrasyon testi**: `python integration_test.py`
2. **Manuel test**: `python manual_test.py`
3. **Unit testler**: `python test_server.py`

### Loglama

Server, `INFO` seviyesinde loglama yapar. Hata durumlarında detaylı log mesajları üretir.

## Lisans

Bu proje MIT lisansı altında yayınlanmıştır.
