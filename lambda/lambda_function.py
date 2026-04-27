import json
import os
import urllib.parse
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    records = event.get("Records", [])
    messages = []

    for record in records:
        if "s3" not in record:
            continue

        bucket = record["s3"]["bucket"]["name"]
        raw_key = record["s3"]["object"]["key"]
        key = urllib.parse.unquote_plus(raw_key)
        size = record["s3"]["object"].get("size", 0)
        event_time = record.get("eventTime", "")

        allowed_exts = (".jpg", ".jpeg", ".png", ".pdf", ".webp")
        if not key.lower().endswith(allowed_exts):
            print(f"Skipped due to extension: {key}")
            continue

        messages.append(
            f"🧾 有新單據上傳\n"
            f"Test from DAWEI!!!\n"
            f"• Bucket: `{bucket}`\n"
            f"• 檔名: `{key}`\n"
            f"• 大小: `{size}` bytes\n"
            f"• 時間: `{event_time}`"
        )

    if not messages:
        print("No matching files. Nothing will be sent to Discord.")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "No matching files."})
        }

    payload = json.dumps({
        "content": "\n\n".join(messages)
    }).encode("utf-8")

    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            print(f"Discord response status={resp.status}")
            print(f"Discord response body={body}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"Discord HTTPError status={e.code}")
        print(f"Discord HTTPError body={error_body}")
        raise

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Discord notification sent"})
    }