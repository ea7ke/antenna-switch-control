#!/bin/bash
echo "Content-type: text/plain"
echo ""

echo "REQUEST_METHOD=$REQUEST_METHOD"
echo "CONTENT_LENGTH=$CONTENT_LENGTH"

if [ "$REQUEST_METHOD" = "POST" ]; then
  read -n "$CONTENT_LENGTH" POST_DATA
  echo "POST_DATA=$POST_DATA"
fi
