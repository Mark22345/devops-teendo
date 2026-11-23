#!/usr/bin/env bash
# Füstteszt: ellenőrzi, hogy a telepített alkalmazás elindult és az üzleti funkciói működnek.
# Használat: bash scripts/smoke_test.sh [BASE_URL]
set -euo pipefail

BASE_URL="${1:-http://localhost:8080}"
echo "Füstteszt indul: $BASE_URL"

echo "1) Várakozás, amíg az alkalmazás elérhető lesz..."
for i in $(seq 1 30); do
  if curl -fsS "$BASE_URL/health" > /dev/null 2>&1; then
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "HIBA: az alkalmazás 60 másodperc alatt sem lett elérhető" >&2
    exit 1
  fi
  sleep 2
done
curl -fsS "$BASE_URL/health"; echo

echo "2) Webes felület betöltése..."
page=$(curl -fsS "$BASE_URL/")
grep -q "Teendőlista" <<< "$page"

echo "3) Teendő létrehozása..."
created=$(curl -fsS -X POST -H 'Content-Type: application/json' \
  -d '{"title":"Füstteszt feladat","priority":"high"}' "$BASE_URL/api/todos")
echo "$created"
id=$(echo "$created" | jq -r '.id')

echo "4) Listázás..."
curl -fsS "$BASE_URL/api/todos" | jq -e --argjson id "$id" 'map(select(.id == $id)) | length == 1'

echo "5) Késznek jelölés..."
curl -fsS -X PATCH -H 'Content-Type: application/json' -d '{"done":true}' \
  "$BASE_URL/api/todos/$id" | jq -e '.done == true'

echo "6) Statisztika..."
curl -fsS "$BASE_URL/api/stats" | jq -e '.done >= 1'

echo "7) Törlés..."
code=$(curl -sS -o /dev/null -w '%{http_code}' -X DELETE "$BASE_URL/api/todos/$id")
[ "$code" = "204" ]

echo "8) Hibakezelés (üres cím -> 400)..."
code=$(curl -sS -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' \
  -d '{"title":""}' "$BASE_URL/api/todos")
[ "$code" = "400" ]

echo "SIKER: az alkalmazás fut és az üzleti funkciók elérhetők."
