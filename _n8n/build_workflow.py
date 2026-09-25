#!/usr/bin/env python3
"""Builds vana-whatsapp-funnel.json (importable into n8n) from funnel-logic.js.
Run from the repo root: python3 _n8n/build_workflow.py"""
import json, os, uuid
HERE = os.path.dirname(os.path.abspath(__file__))
logic = open(os.path.join(HERE, "funnel-logic.js"), encoding="utf-8").read()

SAMPLE = r"""// Sends one fake incoming message through the funnel so you can check the Leads sheet fills in.
// Replies will fail (the number is fake) — that's expected; the lead row should still appear.
const now = Math.floor(Date.now() / 1000);
return [{ json: { entry: [{ changes: [{ value: {
  messaging_product: 'whatsapp',
  metadata: { phone_number_id: 'TEST' },
  contacts: [{ profile: { name: 'Test Guest' }, wa_id: '910000000000' }],
  messages: [{ from: '910000000000', id: 'wamid.test' + now, timestamp: String(now), type: 'text',
               text: { body: "Hi, what's the price for a deep tissue massage?" } }],
} }] }] } }];"""

def node(name, type_, version, pos, params, **extra):
    n = {"parameters": params, "id": str(uuid.uuid5(uuid.NAMESPACE_URL, "vana/" + name)), "name": name,
         "type": type_, "typeVersion": version, "position": pos}
    n.update(extra)
    return n

nodes = [
    node("WhatsApp Trigger", "n8n-nodes-base.whatsAppTrigger", 1, [0, 0], {"updates": ["messages"]}),
    node("Test: sample message", "n8n-nodes-base.manualTrigger", 1, [0, 220], {}),
    node("Sample payload", "n8n-nodes-base.code", 2, [220, 220], {"jsCode": SAMPLE}),
    node("Decide replies & lead", "n8n-nodes-base.code", 2, [460, 0], {"jsCode": logic}),
    node("Reply or lead?", "n8n-nodes-base.if", 2, [700, 0], {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
            "conditions": [{"id": str(uuid.uuid5(uuid.NAMESPACE_URL, "vana/cond")), "leftValue": "={{ $json.kind }}",
                            "rightValue": "reply", "operator": {"type": "string", "operation": "equals"}}],
            "combinator": "and"},
        "options": {}}),
    node("Send WhatsApp reply", "n8n-nodes-base.httpRequest", 4.2, [960, -100], {
        "method": "POST",
        "url": "=https://graph.facebook.com/v21.0/{{ $json.phone_number_id }}/messages",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify($json.payload) }}",
        "options": {"batching": {"batch": {"batchSize": 1, "batchInterval": 700}}}},
        onError="continueRegularOutput",
        notes="Sends one message at a time, in order. Credential: Header Auth with Name = Authorization, Value = Bearer <your permanent WhatsApp token>."),
    node("Lead columns only", "n8n-nodes-base.code", 2, [960, 100], {
        "jsCode": "return $input.all().map(i => { const { kind, ...row } = i.json; return { json: row }; });"}),
    node("Save lead to sheet", "n8n-nodes-base.googleSheets", 4.5, [1200, 100], {
        "operation": "appendOrUpdate",
        "documentId": {"__rl": True, "value": "", "mode": "url"},
        "sheetName": {"__rl": True, "value": "Leads", "mode": "name"},
        "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": ["phone"], "schema": []},
        "options": {"cellFormat": "RAW"}},
        notes="Paste your Leads sheet URL in Document. Matches on the phone column; only writes the columns it owns, so status and notes you type are never overwritten."),
]
conn = lambda *targets: {"main": [[{"node": t, "type": "main", "index": 0} for t in grp] for grp in targets]}
connections = {
    "WhatsApp Trigger": conn(["Decide replies & lead"]),
    "Test: sample message": conn(["Sample payload"]),
    "Sample payload": conn(["Decide replies & lead"]),
    "Decide replies & lead": conn(["Reply or lead?"]),
    "Reply or lead?": conn(["Send WhatsApp reply"], ["Lead columns only"]),
    "Lead columns only": conn(["Save lead to sheet"]),
}
wf = {"name": "VĀNA — WhatsApp auto-reply & lead funnel", "nodes": nodes, "connections": connections,
      "settings": {"executionOrder": "v1", "timezone": "Asia/Kolkata"}, "pinData": {}}
out = os.path.join(HERE, "vana-whatsapp-funnel.json")
json.dump(wf, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out)
