# Hero banner'ı yeniden üretmek

```bash
# 1) Fotoğraftan ASCII portre (koyu tema: parlak = yoğun, açık tema: ters)
python ascii.py <foto.png> 52 30 > ascii.txt
python ascii.py <foto.png> 52 30 invert > ascii_light.txt

# 2) SVG'leri üret (out/ altına calm + bold, koyu + açık)
python hero.py ascii.txt out

# 3) Profilde kullanılan "bold" sürümü kopyala
cp out/hero-bold-dark.svg  ../assets/hero-dark.svg
cp out/hero-bold-light.svg ../assets/hero-light.svg
```

Terminal satırları `hero.py` içindeki `TERM` listesinde. Gereksinim: Pillow.
