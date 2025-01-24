

**add platform**
```bash
cat > /tmp/zstack.json <<EOF
{
    "title": "zstack135",
    "provider": "zstack",
    "access_key": "KTx4ZPfGE6w3BWw4N2Y8",
    "secret_key": "FPESCkWd5tuEIrEggic7gW6snozgiG3ujSpTtAPN",
    "admin_project": "VDI云桌面",
    "url": "http://192.222.1.135:8080"
}
EOF
python3 run.py add-platform "/tmp/zstack.json"
```

**list platform**
```bash
python3 run.py list-platforms | jq
[
  {
    "id": "0558495498c24cbb9bca37148d23aa4d",
    "title": "zstack135",
    "provider": "zstack",
    "enabled": true,
    "extra": {},
    "state": "online",
    "polling_interval": 1800,
    "owned_by": "8f85798792b8466fa570aef1186c61d4",
    "created_by": "8f85798792b8466fa570aef1186c61d4",
    "url": "http://192.222.1.135:8080",
    "access_key": "KTx4ZPfGE6w3BWw4N2Y8",
    "secret_key": "FPESCkWd5tuEIrEggic7gW6snozgiG3ujSpTtAPN",
    "admin_project": "VDI云桌面"
  }
]
```

**list clouds**
```bash
python3 run.py list-clouds "0558495498c24cbb9bca37148d23aa4d" | jq
```

**list machines**
```bash
python3 run.py list-machines "0558495498c24cbb9bca37148d23aa4d" "5930adc2052142b788c100082cd9bb4d" | jq
```
